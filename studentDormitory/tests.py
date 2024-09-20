from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from datetime import datetime

from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests


# Create your tests here.
class StudentsViewsetTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_get_list(self):
		rm = baker.make("studentDormitory.Room")
		student = baker.make("Student", room=rm)

		r = self.client.get('/api/students/')
		data = r.json()
		print(data)

		# Проверка имени студента
		assert student.name == data[0]['name']
		# Проверка ID студента
		assert student.id == data[0]['id']
		# Проверка комнаты (id и number)
		assert student.room.id == data[0]['room']['id']
		assert student.room.number == data[0]['room']['number']
		# Проверка группы
		assert student.group == data[0]['group']
		# Проверка количества студентов в ответе
		assert len(data) == 1
	
	def test_create_student(self):
		rm = baker.make("studentDormitory.Room")
		r = self.client.post('/api/students/', {
				"name": "Студент",
				"group": "ИСТб-22-2",
				"room_id": rm.id  # Используем room_id для передачи ID комнаты
		})

		new_student_id = r.json()['id']

		students = Student.objects.all()
		assert len(students) == 1

		new_student = Student.objects.filter(id=new_student_id).first()

		assert new_student.name == 'Студент'
		assert new_student.group == 'ИСТб-22-2'
		assert new_student.room == rm

	def test_delete_student(self):
		students = baker.make("Student", 10)
		r = self.client.get('/api/students/')
		data = r.json()
		assert len(data) == 10

		student_id_to_delete = students[3].id
		self.client.delete(f'/api/students/{student_id_to_delete}/')

		r = self.client.get('/api/students/')
		data = r.json()
		assert len(data) == 9

		assert student_id_to_delete not in [i['id'] for i in data]

	def test_update_student(self):
		students = baker.make("Student", 10)
		student: Student = students[2]

		# Проверка получения исходных данных студента
		r = self.client.get(f'/api/students/{student.id}/')
		data = r.json()
		assert data['name'] == student.name

		# Обновление данных студента с использованием PATCH
		update_data = {
				"name": "Вася Иванов",
				"group": student.group
		}

		if student.room:
				update_data["room_id"] = student.room.id

		r = self.client.patch(f'/api/students/{student.id}/', update_data)
		assert r.status_code == 200

		# Проверка обновления данных студента
		r = self.client.get(f'/api/students/{student.id}/')
		data = r.json()
		assert data['name'] == "Вася Иванов"

		student.refresh_from_db()
		assert data['name'] == student.name
	

class RoomViewsetTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		
	def test_get_list(self):
		# Создаем несколько комнат
		room = baker.make("Room")

		# Выполняем GET-запрос для получения списка комнат
		r = self.client.get('/api/rooms/')
		data = r.json()

		# Проверка количества комнат в ответе
		assert len(data) == 1

		# Проверка значений первой комнаты
		assert room.id == data[0]['id']
		assert room.number == data[0]['number']

	def test_create_room(self):
		# Выполняем POST-запрос для создания комнаты
		r = self.client.post('/api/rooms/', {
				"number": "101"
		})

		# Проверка, что комната была создана
		new_room_id = r.json()['id']

		rooms = Room.objects.all()
		assert len(rooms) == 1

		new_room = Room.objects.filter(id=new_room_id).first()

		assert new_room.number == "101"

	def test_delete_room(self):
		rooms = baker.make("Room", 10)
		r = self.client.get('/api/rooms/')
		data = r.json()
		assert len(data) == 10

		room_id_to_delete = rooms[3].id
		self.client.delete(f'/api/rooms/{room_id_to_delete}/')

		r = self.client.get('/api/rooms/')
		data = r.json()
		assert len(data) == 9

		assert room_id_to_delete not in [i['id'] for i in data]

	def test_update_room(self):
		rooms = baker.make("Room", 10)
		room: Room = rooms[2]

		# Проверка получения исходных данных комнаты
		r = self.client.get(f'/api/rooms/{room.id}/')
		data = r.json()
		assert data['number'] == room.number

		# Обновление данных комнаты с использованием PATCH
		update_data = {
				"number": "209б",
		}

		r = self.client.patch(f'/api/rooms/{room.id}/', update_data)
		assert r.status_code == 200

		# Проверка обновления данных комнаты
		r = self.client.get(f'/api/rooms/{room.id}/')  # Здесь исправлен эндпоинт
		data = r.json()
		assert data['number'] == "209б"

		room.refresh_from_db()
		assert data['number'] == room.number

class DutyScheduleViewsetTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_get_list(self):
		std = baker.make("studentDormitory.Student")
		duty = baker.make("DutySchedule", student=std)

		r = self.client.get('/api/dutySchedule/')
		data = r.json()
		print(data)

		# Преобразование строки даты из JSON-ответа в объект datetime.date
		response_date = datetime.strptime(data[0]['date'], "%Y-%m-%d").date()

		# Сравнение преобразованной даты с duty.date
		assert duty.date == response_date
		assert duty.id == data[0]['id']
		assert duty.student.id == data[0]['student']['id']
		assert len(data) == 1

	def test_create_duty_schedule(self):
		# Создаем студента и привязываем его к расписанию дежурств
		student = baker.make("studentDormitory.Student")
		
		# Делаем POST-запрос для создания новой записи в расписании дежурств
		r = self.client.post('/api/dutySchedule/', {
				"date": "2024-09-18",  # Указываем дату
				"student_id": student.id  # Передаем ID студента
		})

		# Получаем ID новой записи из ответа
		new_duty_schedule_id = r.json()['id']

		# Проверяем, что запись успешно создана
		duty_schedules = DutySchedule.objects.all()
		assert len(duty_schedules) == 1

		# Получаем только что созданную запись
		new_duty_schedule = DutySchedule.objects.filter(id=new_duty_schedule_id).first()

		expected_date = datetime.strptime("2024-09-18", "%Y-%m-%d").date()
		assert new_duty_schedule.date == expected_date
		assert new_duty_schedule.student == student

	def test_delete_duty_schedule(self):
		# Создаем 10 записей расписания дежурств
		duty_schedules = baker.make("DutySchedule", 10)

		# Проверяем, что записи успешно созданы
		r = self.client.get('/api/dutySchedule/')
		data = r.json()
		assert len(data) == 10

		# Удаляем одну из записей
		duty_schedule_id_to_delete = duty_schedules[3].id
		self.client.delete(f'/api/dutySchedule/{duty_schedule_id_to_delete}/')

		# Проверяем, что количество записей уменьшилось
		r = self.client.get('/api/dutySchedule/')
		data = r.json()
		assert len(data) == 9

		# Убедимся, что удалённой записи больше нет
		assert duty_schedule_id_to_delete not in [i['id'] for i in data]

	def test_update_duty_schedule(self):

		# Создаем 10 записей расписания дежурств с привязкой к студенту
		duty_schedules = baker.make("DutySchedule",10)
		duty_schedule: DutySchedule = duty_schedules[2]

		# Проверка получения исходных данных дежурства
		r = self.client.get(f'/api/dutySchedule/{duty_schedule.id}/')
		data = r.json()
		assert data['date'] == duty_schedule.date.strftime("%Y-%m-%d")

		# Обновление данных дежурства с использованием PATCH
		update_data = {
				"date": "2024-09-18",  # Обновляем дату
		}

		r = self.client.patch(f'/api/dutySchedule/{duty_schedule.id}/', update_data)
		assert r.status_code == 200

		# Проверка обновления данных дежурства
		r = self.client.get(f'/api/dutySchedule/{duty_schedule.id}/')
		data = r.json()
		assert data['date'] == "2024-09-18"

		duty_schedule.refresh_from_db()
		assert duty_schedule.date.strftime("%Y-%m-%d") == "2024-09-18"

class StaffViewsetTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		
	def test_get_list(self):
		# Создаем несколько комнат
		staff = baker.make("Staff")

		# Выполняем GET-запрос для получения списка комнат
		r = self.client.get('/api/staff/')
		data = r.json()

		# Проверка количества комнат в ответе
		assert len(data) == 1

		# Проверка значений первой комнаты
		assert staff.id == data[0]['id']
		assert staff.name == data[0]['name']
		assert staff.post == data[0]['post']

	def test_create_room(self):
		# Выполняем POST-запрос для создания комнаты
		r = self.client.post('/api/staff/', {
				"name": "Вася Пупкин",
				"post": "Каменщик"
		})

		# Проверка, что комната была создана
		new_staff_id = r.json()['id']

		staff = Staff.objects.all()
		assert len(staff) == 1

		new_staff = Staff.objects.filter(id=new_staff_id).first()

		assert new_staff.name == "Вася Пупкин"
		assert new_staff.post == "Каменщик"

	def test_delete_room(self):
		staff = baker.make("Staff", 10)
		r = self.client.get('/api/staff/')
		data = r.json()
		assert len(data) == 10

		staff_id_to_delete = staff[3].id
		self.client.delete(f'/api/staff/{staff_id_to_delete}/')

		r = self.client.get('/api/staff/')
		data = r.json()
		assert len(data) == 9

		assert staff_id_to_delete not in [i['id'] for i in data]

	def test_update_staff(self):
		# Создаем 10 записей staff
		staff = baker.make("Staff", 10)
		stf: Staff = staff[2]

		# Проверка получения исходных данных staff
		r = self.client.get(f'/api/staff/{stf.id}/')
		data = r.json()
		assert data['post'] == stf.post

		update_data = {
				"post": "Каменщик"
		}

		r = self.client.patch(f'/api/staff/{stf.id}/', update_data)
		assert r.status_code == 200

		r = self.client.get(f'/api/staff/{stf.id}/')
		data = r.json()
		assert data['post'] == "Каменщик"

		stf.refresh_from_db()
		assert stf.post == "Каменщик"

class RepairRequestsViewsetTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_get_list(self):
		rm = baker.make("studentDormitory.Room")
		stf = baker.make("studentDormitory.Staff")
		req = baker.make("RepairRequests", room = rm, staff = stf)

		r = self.client.get('/api/repairRequests/')
		data = r.json()
		print(data)

		# Преобразование строки даты из JSON-ответа в объект datetime.date
		response_date = datetime.strptime(data[0]['date'], "%Y-%m-%d").date()

		# Сравнение преобразованной даты с duty.date
		assert req.date == response_date
		assert req.id == data[0]['id']
		assert req.description == data[0]['description']
		assert req.status == data[0]['status']
		assert req.room.id == data[0]['room']['id']
		assert req.staff.id == data[0]['staff']['id']
		assert len(data) == 1

	def test_create_repair_requests(self):
		# Создаем студента и привязываем его к расписанию дежурств
		room = baker.make("studentDormitory.Room")
		staff = baker.make("studentDormitory.Staff")
		
		# Делаем POST-запрос для создания новой записи в расписании дежурств
		r = self.client.post('/api/repairRequests/', {
				"date": "2024-09-18",
				"description": "afgasf",
				"status": "completed",
				"room_id": room.id,
				"staff_id": staff.id
		})

		# Получаем ID новой записи из ответа
		new_repair_requests_id = r.json()['id']

		# Проверяем, что запись успешно создана
		repair_requests = RepairRequests.objects.all()
		assert len(repair_requests) == 1

		# Получаем только что созданную запись
		new_repair_requests = RepairRequests.objects.filter(id=new_repair_requests_id).first()

		expected_date = datetime.strptime("2024-09-18", "%Y-%m-%d").date()
		assert new_repair_requests.date == expected_date
		assert new_repair_requests.description == "afgasf"
		assert new_repair_requests.status == "completed"
		assert new_repair_requests.room == room
		assert new_repair_requests.staff == staff

	def test_delete_duty_schedule(self):
		# Создаем 10 записей расписания дежурств
		repair_requests = baker.make("RepairRequests", 10)

		# Проверяем, что записи успешно созданы
		r = self.client.get('/api/repairRequests/')
		data = r.json()
		assert len(data) == 10

		# Удаляем одну из записей
		repair_requests_id_to_delete = repair_requests[3].id
		self.client.delete(f'/api/repairRequests/{repair_requests_id_to_delete}/')

		# Проверяем, что количество записей уменьшилось
		r = self.client.get('/api/repairRequests/')
		data = r.json()
		assert len(data) == 9

		# Убедимся, что удалённой записи больше нет
		assert repair_requests_id_to_delete not in [i['id'] for i in data]

	def test_update_duty_schedule(self):
		repair_requests = baker.make("RepairRequests",10)
		repair_request: RepairRequests = repair_requests[2]

		# Проверка получения исходных данных дежурства
		r = self.client.get(f'/api/repairRequests/{repair_request.id}/')
		data = r.json()
		assert data['status'] == repair_request.status

		# Обновление данных дежурства с использованием PATCH
		update_data = {
				"status": "cancelled",  # Обновляем дату
		}

		r = self.client.patch(f'/api/repairRequests/{repair_request.id}/', update_data)
		assert r.status_code == 200

		# Проверка обновления данных дежурства
		r = self.client.get(f'/api/repairRequests/{repair_request.id}/')
		data = r.json()
		assert data['status'] == "cancelled"

		repair_request.refresh_from_db()
		assert repair_request.status == "cancelled"

	