from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets 	
from rest_framework.authentication import BasicAuthentication
from app.middlewares import CsrfExemptSessionAuthentication
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
	authentication_classes =  (CsrfExemptSessionAuthentication, BasicAuthentication)
	def get_queryset(self):
		qs = super().get_queryset()
		
		if self.request.user.is_superuser:
				return qs
		
		return qs.filter(user=self.request.user)

class RoomViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	authentication_classes =  (CsrfExemptSessionAuthentication, BasicAuthentication)
	def get_queryset(self):
		qs = super().get_queryset()
		
		if self.request.user.is_superuser:
				return qs
		
		return qs.filter(user=self.request.user)

class DutyScheduleViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = DutySchedule.objects.all()
	serializer_class = DutyScheduleSerializer
	authentication_classes =  (CsrfExemptSessionAuthentication, BasicAuthentication)
	def get_queryset(self):
		qs = super().get_queryset()
		
		if self.request.user.is_superuser:
				return qs
		
		return qs.filter(user=self.request.user)

class StaffViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = Staff.objects.all()
	serializer_class = StaffSerializer
	authentication_classes =  (CsrfExemptSessionAuthentication, BasicAuthentication)
	def get_queryset(self):
		qs = super().get_queryset()
		
		if self.request.user.is_superuser:
				return qs
		
		return qs.filter(user=self.request.user)

class RepairRequestsViewset(
	mixins.CreateModelMixin,
	mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	mixins.ListModelMixin,
	GenericViewSet):
	queryset = RepairRequests.objects.all()
	serializer_class = RepairRequestsSerializer
	authentication_classes =  (CsrfExemptSessionAuthentication, BasicAuthentication)
	def get_queryset(self):
		qs = super().get_queryset()
		
		if self.request.user.is_superuser:
				return qs
		
		return qs.filter(user=self.request.user)