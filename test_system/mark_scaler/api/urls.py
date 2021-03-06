from .views import ScalerAPIView, ScalerRudView
from django.urls import re_path, path

app_name = 'api-scaler'

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', ScalerRudView.as_view(), name='scaler-rud'),
    path(r'', ScalerAPIView.as_view(), name='scaler-create'),
]
