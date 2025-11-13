from django.urls import path
from .views import StaffProfileView

urlpatterns = [
    path('me/', StaffProfileView.as_view(), name='me'),
]
