from rest_framework import serializers
from .models import Task, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']




class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
    queryset=CustomUser.objects.all(), source='assigned_to', write_only=True, required=False
    )


class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'assigned_to', 'assigned_to_id', 'due_date', 'status', 'completion_report', 'worked_hours', 'created_at', 'updated_at']
    read_only_fields = ['created_at', 'updated_at']




class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']


    def validate(self, data):
        status = data.get('status')
        if status == Task.COMPLETED:
            # completion_report and worked_hours are required
            if not data.get('completion_report'):
                raise serializers.ValidationError({'completion_report': 'This field is required when marking task as Completed.'})
            if data.get('worked_hours') in (None, ''):
                raise serializers.ValidationError({'worked_hours': 'This field is required when marking task as Completed.'})
        return data