from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Task, CustomUser
from .serializers import TaskSerializer, TaskUpdateSerializer
from .permissions import IsAdminOrSuperAdmin, IsSuperAdmin, IsOwner
from django.shortcuts import get_object_or_404


# GET /api/tasks/ -> tasks assigned to logged-in user
class UserTasksListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


def get_queryset(self):
    return Task.objects.filter(assigned_to=self.request.user)




# PUT /api/tasks/<id>/ -> update task status
class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    lookup_url_kwarg = 'pk'


def get_object(self):
    obj = super().get_object()
    # users can only update their own tasks (unless Admin/SuperAdmin)
    if self.request.user.role == 'USER' and obj.assigned_to_id != self.request.user.id:
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied('You can only update your own tasks.')
    return obj


def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(TaskSerializer(instance).data)




# GET /api/tasks/<id>/report/ -> Admins/SuperAdmins can view completion report for completed tasks
class TaskReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]


def get(self, request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.status != Task.COMPLETED:
        return Response({'detail': 'Report available only for completed tasks.'}, status=status.HTTP_400_BAD_REQUEST)
    data = {
    'id': task.id,
    'title': task.title,
    'assigned_to': task.assigned_to.username,
    'completion_report': task.completion_report,
    'worked_hours': str(task.worked_hours),
    'completed_at': task.updated_at,
    }
    return Response(data)