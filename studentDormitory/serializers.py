from rest_framework import serializers
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests
from datetime import datetime

class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ["id", "number"]

class StudentSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True, source="room")

    class Meta:
        model = Student
        fields = ["id", "name", "group", "room", "room_id"]


class DutyScheduleSerializer(serializers.ModelSerializer):
	student = StudentSerializer(read_only=True)
	student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, source="student")

	class Meta:
		model = DutySchedule
		fields = ["id", "date", "student", "student_id"]

class StaffSerializer(serializers.ModelSerializer):
	class Meta:
		model = Staff
		fields = ["id", "name", "post"]

class RepairRequestsSerializer(serializers.ModelSerializer):
	room = RoomSerializer(read_only=True)
	room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True, source="room")
	staff = StaffSerializer(read_only=True)
	staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), write_only=True, source="staff")

	class Meta:
		model = RepairRequests
		fields = ["id", "date", "description", "status", "room", "room_id", "staff", "staff_id"]