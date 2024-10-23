<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import _ from 'lodash';

const students = ref({});
const rooms = ref({})
const studentToAdd = ref({
	name: '',
	group: '',
	room: null
});
const studentToEdit = ref({
	name: '',
	group: '',
	room: null
});
const studentsPictureRef = ref();
const studentsPictureRefEdit = ref();
const studentAddImageUrl = ref();
const studentEditImageUrl = ref();
const selectedImageUrl = ref();
const stats = ref({});

function openImageModal(imageUrl) {
	selectedImageUrl.value = imageUrl;
	const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
	imageModal.show();
}

async function fetchStudents() {
	const r = await axios.get("/api/students/")
	students.value = r.data
}

async function fetchRooms() {
	const r = await axios.get("/api/rooms/")
	rooms.value = r.data
}
async function fetchStats() {
	const r = await axios.get("/api/students/stats/");
	stats.value = r.data;
}


async function onStudentAdd() {
	const formData = new FormData();

	formData.append('picture', studentsPictureRef.value.files[0]);

	formData.set('name', studentToAdd.value.name)
	formData.set('group', studentToAdd.value.group)
	formData.set('room_id', studentToAdd.value.room_id)

	await axios.post("/api/students/", formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	await fetchStudents();
}

async function studentAddPictureChange() {
	studentAddImageUrl.value = URL.createObjectURL(studentsPictureRef.value.files[0])
}
async function studentEditPictureChange() {
	studentEditImageUrl.value = URL.createObjectURL(studentsPictureRefEdit.value.files[0])
}

async function onStudentRemoveClick(student) {
	await axios.delete(`/api/students/${student.id}/`);
	await fetchStudents();
}

async function onStudentEditClick(student) {
	studentToEdit.value = {
		id: student.id,
		name: student.name,
		group: student.group,
		room_id: student.room.id,
		picture: student.picture
	};
	studentEditImageUrl.value = student.picture;
}

async function OnUpdateStudentClick() {
	const formData = new FormData();

	formData.append('picture', studentsPictureRefEdit.value.files[0]);

	formData.set('name', studentToEdit.value.name);
	formData.set('group', studentToEdit.value.group);
	formData.set('room_id', studentToEdit.value.room_id);

	await axios.put(`/api/students/${studentToEdit.value.id}/`, formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	await fetchStudents();
}

onBeforeMount(async () => {
	await fetchStudents()
	await fetchRooms()
})

</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onStudentAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="studentToAdd.name" required>
						<label for="floatingInput">ФИО</label>
					</div>
				</div>
				<div class="col-3">
					<input class="form-control" type="file" ref="studentsPictureRef" @change="studentAddPictureChange()" required>
				</div>
				<div class="col-auto">
					<img :src="studentAddImageUrl" style="max-height: 60px;" alt="">
				</div>
				<div class="col-2">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="studentToAdd.group" required>
						<label for="floatingInput">Группа</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<select class="form-select" v-model="studentToAdd.room_id" required>
							<option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
						</select>
						<label for="floatingInput">Комната</label>
					</div>
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-primary">Добавить</button>
				</div>
			</div>
		</form>
		<div class="row pt-2">
			<div class="col">
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-success" @click="fetchStats()" data-bs-toggle="modal"
					data-bs-target="#statsModal">Статистика</button>
				</div>
			</div>
		</div>
	</div>

	<div>
		<div v-for="item in students" class="student-item">
			<div>
				{{ item.name }}
			</div>
			<div>
				{{ item.group }}
			</div>
			<div>
				{{ item.room.number }}
			</div>
			<div v-show="item.picture">
				<img :src="item.picture" style="max-height: 60px;" @click="openImageModal(item.picture)" alt="Картинка студента"
					data-bs-toggle="modal" data-bs-target="#imageModal">
			</div>
			<div>
				<button class="btn btn-success" @click="onStudentEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editStudentModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onStudentRemoveClick(item)"><i class="bi bi-trash"></i></button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editStudentModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="studentToEdit.name">
								<label for="floatingInput">ФИО</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="studentToEdit.group">
								<label for="floatingInput">Группа</label>
							</div>
						</div>
						<div class="col">
							<div class="form-floating">
								<select class="form-select" v-model="studentToEdit.room_id">
									<option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
								</select>
								<label for="floatingInput">Комната</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col-6">
							<input class="form-control" type="file" ref="studentsPictureRefEdit" @change="studentEditPictureChange()"
								required>
						</div>
						<div class="col-auto">
							<img :src="studentEditImageUrl" style="max-height: 60px;" alt="">
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
					<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
						@click="OnUpdateStudentClick()">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Модальное окно для просмотра картинки -->
	<div class="modal fade" id="imageModal" tabindex="-1" role="dialog">
		<div class="modal-dialog modal-dialog-centered" role="document">
			<div class="modal-content">
				<div class="modal-body text-center">
					<img :src="selectedImageUrl" alt="Просмотр изображения" class="img-fluid">
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Модальное окно для статистики -->
	<div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Статистика студентов</h5>
				</div>
				<div class="modal-body">
					<p>Количество студентов: {{ stats.count }}</p>
					<p>Максимальный ID студента: {{ stats.max }}</p>
					<p>Минимальный ID студента: {{ stats.min }}</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.student-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.5fr 0.25fr 0.25fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}

.student-item img {
	cursor: pointer;
}
</style>
