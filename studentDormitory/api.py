from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests
from studentDormitory.serializers import StudentSerializer, RoomSerializer, DutyScheduleSerializer, StaffSerializer, RepairRequestsSerializer

class StudentViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

class RoomViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

class DutyScheduleViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = DutySchedule.objects.all()
	serializer_class = DutyScheduleSerializer

class StaffViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = Staff.objects.all()
	serializer_class = StaffSerializer

class RepairRequestsViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = RepairRequests.objects.all()
	serializer_class = RepairRequestsSerializer