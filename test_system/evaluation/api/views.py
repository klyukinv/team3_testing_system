from rest_framework import generics
from user_pref.models import UserPreferences, Preference
from django.db.models import Q, F
from .serializers import MarkStudentSerializer, MarksSerializer
from .permissions import IsStudent, IsTeacherOrAdmin, EmptyPermission
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import NotAcceptable
from evaluation.models import Mark, SpeakingLevel, TestLevel
from mark_scaler.models import Scaler
from student_answer.models import StudentAnswer
from test_question.models import TestQuestion
from django.http import HttpResponse
from rest_framework.response import Response
from speaking_queue.models import TeacherSpeaking
from room.models import Room
from rest_framework.views import APIView
from rest_framework import status
from random import sample
import xlsxwriter
from io import BytesIO
from django.http import StreamingHttpResponse
from django.contrib.auth.models import User


class MarkAPIView(generics.ListAPIView, generics.CreateAPIView):
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return MarkStudentSerializer
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return MarksSerializer
        return MarkStudentSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return [IsStudent()]
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return [IsTeacherOrAdmin()]
        return [EmptyPermission()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                sa = Mark.objects.filter(user=self.request.user)
                return sa
            elif qs[0].user_preference == Preference.TEACHER or qs[0].user_preference == Preference.ADMIN:
                return Mark.objects.all()


class MarkRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.ADMIN or qs[0].user_preference == Preference.TEACHER:
                return MarksSerializer
            if qs[0].user_preference == Preference.STUDENT:
                return MarkStudentSerializer
        return MarkStudentSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return [IsStudent()]
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return [IsTeacherOrAdmin()]
        return [EmptyPermission()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                sa = Mark.objects.filter(user=self.request.user)
                return sa
            elif qs[0].user_preference == Preference.TEACHER or qs[0].user_preference == Preference.ADMIN:
                sa = Mark.objects.all()
                return sa

    def put(self, request, *args, **kwargs):
        pref = UserPreferences.objects.filter(user=self.request.user)[0]
        if pref.user_preference == Preference.STUDENT:
            instance = self.get_object()
            position = 0
            if instance.room is None or instance.room.pk != int(request.data['room']):
                try:
                    old_room = instance.room
                    if old_room is not None and old_room.amount_stud > 0:
                        Room.objects.filter(pk=old_room.pk).update(amount_stud=old_room.amount_stud - 1)
                        Mark.objects.filter(room=old_room).exclude(position__lte=instance.position) \
                            .update(position=F('position') - 1)
                    if request.data['room'] is not None:
                        room = Room.objects.get(pk=request.data['room'])
                        Room.objects.filter(pk=room.pk).update(amount_stud=room.amount_stud + 1)
                        position = room.amount_stud + 1
                    serializer = self.get_serializer(instance, data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    Mark.objects.filter(pk=instance.pk).update(position=position)
                    response = serializer.data
                    response['position'] = position
                    return Response(response)
                except Room.DoesNotExist:
                    pass
            else:
                raise NotAcceptable('Already in this queue')
        elif pref.user_preference == Preference.ADMIN or pref.user_preference == Preference.TEACHER:
            instance = self.get_object()
            if not instance.removed and request.data['removed']:
                StudentAnswer.objects.filter(user=instance.user, answer=32767). \
                    update(answer=-1)
            if instance.position != -1 and request.data['position'] == -1:
                try:
                    Mark.objects.filter(room=instance.room.pk).exclude(position__lte=instance.position) \
                        .update(position=F('position') - 1)
                    Room.objects.filter(pk=instance.room.pk).update(amount_stud=F('amount_stud') - 1)
                except Room.DoesNotExist:
                    pass
                except AttributeError:
                    pass
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)


class CountMarksView(generics.ListAPIView):
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.filter(user=self.request.user)
            if qs[0].user_preference == Preference.ADMIN or qs[0].user_preference == Preference.TEACHER:
                return MarksSerializer
            if qs[0].user_preference == Preference.STUDENT:
                return MarkStudentSerializer
        return MarkStudentSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return [EmptyPermission()]
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return [IsTeacherOrAdmin()]
        return [EmptyPermission()]

    @staticmethod
    def evaluate(test_mark, mark):
        bounds = Scaler.objects.all()
        if test_mark == 0:
            min_level = None
            min_bound = 1000
            for bound in bounds:
                if bound.lower < min_bound:
                    min_bound = bound.lower
                    min_level = bound.level
            return TestLevel.get_value(min_level)
        for bound in bounds:
            if bound.lower <= test_mark <= bound.upper:
                Mark.objects.filter(pk=mark.pk).update(test_level=TestLevel.get_enum(bound.level).name)
                return TestLevel.get_value(bound.level)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            pref = UserPreferences.objects.get(user=self.request.user)
            if pref.user_preference == Preference.STUDENT:
                raise PermissionDenied
            elif pref.user_preference == Preference.TEACHER or pref.user_preference == Preference.ADMIN:
                marks = Mark.objects.all()
                try:
                    for mark in marks:
                        answers = StudentAnswer.objects.filter(user=mark.user)
                        count = 0
                        if len(answers) > 0:
                            for ans in answers:
                                question = TestQuestion.objects.get(pk=ans.question.pk)
                                if question.answ_correct == ans.answer:
                                    count += 1
                        if mark.test_level != TestLevel.A1.name:
                            t_mark = TestLevel.get_value(mark.test_level)
                        else:
                            t_mark = self.evaluate(count, mark)
                        Mark.objects.filter(pk=mark.pk).update(test_mark=count)
                        sp_mark = 1
                        if mark.speaking_mark:
                            sp_mark = SpeakingLevel.get_value(mark.speaking_mark)
                        Mark.objects.filter(pk=mark.pk).update(level=TestLevel.rev_vals()[int(round((sp_mark + t_mark) / 2))])
                    return Mark.objects.all()
                except AttributeError:
                    return HttpResponse('Unknown error', status=500)


class StudentsByRoom(generics.ListAPIView):
    def get_permissions(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return [EmptyPermission()]
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return [IsTeacherOrAdmin()]
        return [EmptyPermission()]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.filter(user=self.request.user)
            if qs[0].user_preference == Preference.ADMIN or qs[0].user_preference == Preference.TEACHER:
                return MarksSerializer
            if qs[0].user_preference == Preference.STUDENT:
                return MarkStudentSerializer
        return MarkStudentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            pref = UserPreferences.objects.filter(user=self.request.user)[0]
            if pref.user_preference == Preference.TEACHER or pref.user_preference == Preference.ADMIN:
                teacher = TeacherSpeaking.objects.filter(teacher=self.request.user)
                if len(teacher) > 0:
                    return Mark.objects.filter(room=teacher[0].room)
            return Mark.objects.none()
        return Mark.objects.none()


def get_student_list(major: str, groups: int, students: int) -> list:
    if (groups is None) and (students is None):
        raise ValueError(f"{major}: Group or student per group count should be passed in request body")

    marks = list(Mark.objects.filter(Q(major=major)))
    marks_count = len(marks)

    if (groups is not None) and (students is not None):
        groups = int(groups)
        students = int(students)
        if groups * students < marks_count:
            groups = None

    if groups is None:
        groups = marks_count // students + 1 * (marks_count % students != 0)

    if students is None:
        students = marks_count // groups + 1 * (marks_count % groups != 0)

    students -= 1
    if students == 0:
        students = 1

    marks = list(map(lambda x: (TestLevel.vals()[x.level], x.level, x.test_mark == 0 and
                                x.speaking_mark == 'A1m' and x.level == 'A1', x.first_name,
                                x.second_name, x.fathers_name), marks))

    pv = list(filter(lambda x: x[2] == False, marks))  # Probably visited
    pnv = list(filter(lambda x: x[2] == True, marks))

    pv.sort(reverse=True)
    pnv = sample(pnv, len(pnv))

    pvst = len(pv) // groups + 1 * (len(pv) % groups != 0)  # Students per group
    if pvst == 0:
        pvst = 1
    pnvst = len(pnv) // groups + 1 * (len(pnv) % groups != 0)
    if pnvst == 0:
        pnvst = 1

    gpv = [pv[i:i + pvst] for i in range(0, len(pv), pvst)]  # Grouped
    lgpv = len(gpv)
    for i in range(groups - lgpv):
        gpv.append([])

    gpnv = [pnv[i:i + pnvst] for i in range(0, len(pnv), pnvst)]
    lgpnv = len(gpnv)
    for i in range(groups - lgpnv):
        gpnv.append([])

    g = [gpv[i] + gpnv[i] for i in range(groups)]  # Merge groups

    print(g)

    return tuple(map(lambda x: tuple(map(lambda y: (y[4], y[3], y[5], y[1]), x)), g))


class GroupListView(APIView):

    @staticmethod
    def result_text(level, name, surname):
        return "Dear " + name + " " + surname + "!\n According to the test results your English language " \
                                                "proficiency level is " + level + ".\n\nBest regards,\nHSE administration."

    def get_permissions(self):
        if self.request.user.is_authenticated:
            pref = UserPreferences.objects.filter(user=self.request.user)
            if pref[0].user_preference == Preference.STUDENT:
                return [EmptyPermission()]
            elif pref[0].user_preference == Preference.ADMIN or pref[0].user_preference == Preference.TEACHER:
                return [IsTeacherOrAdmin()]
        else:
            return [EmptyPermission()]

    def get(self, request):
        groupsSE = self.request.GET.get("groupsSE")
        groupsAMI = self.request.GET.get("groupsAMI")
        studentsSE = self.request.GET.get("studentsSE")
        studentsAMI = self.request.GET.get("studentsAMI")

        se = []
        ami = []
        try:
            se = get_student_list('SE', groupsSE, studentsSE)
            ami = get_student_list('AMI', groupsAMI, studentsAMI)
        except Exception as e:
            return Response({"status": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # create workbook with worksheet
        output = BytesIO()
        book = xlsxwriter.Workbook(output)

        for major in (se, ami):
            if major == se:
                sheet = book.add_worksheet('SE')
            else:
                sheet = book.add_worksheet('AMI')
            # fill worksheet
            row = 0
            for group in major:
                for student in group:
                    for i in range(len(student)):
                        sheet.write(row, i, student[i])
                    row += 1
                row += 1

        book.close()  # close book and save it in "output"
        output.seek(0)  # seek stream on begin to retrieve all data from it

        # send emails with results
        unsent = Mark.objects.filter(email_received=False)
        for student in unsent:
            student.user.email_user("Results of the entry test",
                                    self.result_text(student.level, student.user.first_name, student.user.last_name))
        Mark.objects.filter(email_received=False).update(email_received=True)
        # send "output" object to stream with mimetype and filename
        response = StreamingHttpResponse(
            output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Student_list.xlsx'
        return response
