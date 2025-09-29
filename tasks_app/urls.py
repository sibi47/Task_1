from django.urls import path
from .views import UserTasksListAPIView, TaskUpdateAPIView, TaskReportAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('tasks/', UserTasksListAPIView.as_view(), name='user_tasks'),
    path('tasks/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_update'),
    path('tasks/<int:pk>/report/', TaskReportAPIView.as_view(), name='task_report'),
    ]