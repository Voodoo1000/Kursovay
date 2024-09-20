from django.contrib import admin

from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "group", "room"]

@admin.register(Room)
class GroupAdmin(admin.ModelAdmin):
	list_display = ["id", "number"]

@admin.register(DutySchedule)
class GroupAdmin(admin.ModelAdmin):
	list_display = ["id", "date", "student"]

@admin.register(Staff)
class GroupAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "post"]

@admin.register(RepairRequests)
class GroupAdmin(admin.ModelAdmin):
	list_display = ["date", "description", "status", "room", "staff"]