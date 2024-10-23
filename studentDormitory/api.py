from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from app.middlewares import CsrfExemptSessionAuthentication
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests
from studentDormitory.serializers import StudentSerializer, RoomSerializer, DutyScheduleSerializer, StaffSerializer, RepairRequestsSerializer
from django.db.models import Avg, Count, Max, Min

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
	
	class StatsSerializer(serializers.Serializer):
		count = serializers.IntegerField()
		avg = serializers.FloatField()
		max = serializers.IntegerField()
		min = serializers.IntegerField()

	@action(detail=False, methods=["GET"], url_path="stats")
	def get_stats(self, *args, **kwargs):
		stats = Student.objects.aggregate(
			count = Count("*"),
			avg = Avg("id"),
			max = Max("id"),
			min = Min("id"),
		)

		serializer = self.StatsSerializer(instance = stats)

		return Response(serializer.data)

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
	
	class StatsSerializer(serializers.Serializer):
		count = serializers.IntegerField()
		avg = serializers.FloatField()
		max = serializers.IntegerField()
		min = serializers.IntegerField()

	@action(detail=False, methods=["GET"], url_path="stats")
	def get_stats(self, *args, **kwargs):
		stats = Room.objects.aggregate(
			count = Count("*"),
			avg = Avg("id"),
			max = Max("id"),
			min = Min("id"),
		)

		serializer = self.StatsSerializer(instance = stats)

		return Response(serializer.data)

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
	
	class StatsSerializer(serializers.Serializer):
		count = serializers.IntegerField()
		avg = serializers.FloatField()
		max = serializers.IntegerField()
		min = serializers.IntegerField()

	@action(detail=False, methods=["GET"], url_path="stats")
	def get_stats(self, *args, **kwargs):
		stats = DutySchedule.objects.aggregate(
			count = Count("*"),
			avg = Avg("id"),
			max = Max("id"),
			min = Min("id"),
		)

		serializer = self.StatsSerializer(instance = stats)

		return Response(serializer.data)

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
	
	class StatsSerializer(serializers.Serializer):
		count = serializers.IntegerField()
		avg = serializers.FloatField()
		max = serializers.IntegerField()
		min = serializers.IntegerField()

	@action(detail=False, methods=["GET"], url_path="stats")
	def get_stats(self, *args, **kwargs):
		stats = Staff.objects.aggregate(
			count = Count("*"),
			avg = Avg("id"),
			max = Max("id"),
			min = Min("id"),
		)

		serializer = self.StatsSerializer(instance = stats)

		return Response(serializer.data)

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
	
	class StatsSerializer(serializers.Serializer):
		count = serializers.IntegerField()
		avg = serializers.FloatField()
		max = serializers.IntegerField()
		min = serializers.IntegerField()

	@action(detail=False, methods=["GET"], url_path="stats")
	def get_stats(self, *args, **kwargs):
		stats = RepairRequests.objects.aggregate(
			count = Count("*"),
			avg = Avg("id"),
			max = Max("id"),
			min = Min("id"),
		)

		serializer = self.StatsSerializer(instance = stats)

		return Response(serializer.data)