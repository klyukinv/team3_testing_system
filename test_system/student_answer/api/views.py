from rest_framework import generics
from student_answer.models import StudentAnswer
from .serializers import StudentAnswerSerializer, StudentAnswerSerializerEmpty, StudentAnswerAPISerializer
from django.db.models import Q
from .permissions import IsStudent, IsTeacherOrAdmin, EmptyPermission, IsStudentWithPut
from user_pref.models import UserPreferences, Preference
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from test_system import base_path
from rest_framework.decorators import api_view


class StudentAnswerAPIView(generics.ListAPIView, generics.CreateAPIView):
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return StudentAnswerAPISerializer
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return StudentAnswerSerializer
        return StudentAnswerSerializerEmpty

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
            qs = UserPreferences.objects.filter(user=self.request.user)
            if qs[0].user_preference == Preference.STUDENT:
                sa = StudentAnswer.objects.filter(user=self.request.user, answer=32767)
                return sa
            elif qs[0].user_preference == Preference.TEACHER or qs[0].user_preference == Preference.ADMIN:
                return StudentAnswer.objects.all()


class StudentAnswerRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT or \
                    qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return StudentAnswerSerializer
        return StudentAnswerSerializerEmpty

    def get_permissions(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                return [IsStudentWithPut()]
            elif qs[0].user_preference == Preference.ADMIN or \
                    qs[0].user_preference == Preference.TEACHER:
                return [IsTeacherOrAdmin()]
        return [EmptyPermission()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = UserPreferences.objects.all()
            qs = qs.filter(Q(user=self.request.user))
            if qs[0].user_preference == Preference.STUDENT:
                sa = StudentAnswer.objects.filter(user=self.request.user)
                return sa
            elif qs[0].user_preference == Preference.TEACHER or qs[0].user_preference == Preference.ADMIN:
                sa = StudentAnswer.objects.all()
                return sa


@login_required
def redirect(request):
    qs = UserPreferences.objects.filter(user=request.user)
    if qs[0].user_preference == Preference.STUDENT:
        return render(request, 'tmp_test_system.html', {})
    else:
        return HttpResponseRedirect(base_path.BASE_PATH + 'test_editor/')


@api_view(['POST'])
def finish_test(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            qs = UserPreferences.objects.filter(user=request.user)
            if len(qs) > 0:
                if qs[0].user_preference == Preference.STUDENT:
                    StudentAnswer.objects.filter(user=request.user, answer=32767).\
                        update(answer=-1)
        return HttpResponse(status=200)
