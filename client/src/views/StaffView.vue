<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import _ from 'lodash';

const staff = ref([]);
const staffToAdd = ref({
	name: '',
	post: ''
});
const staffToEdit = ref({
	name: '',
	post: ''
});
const staffPictureRef = ref();
const staffPictureRefEdit = ref();
const staffAddImageUrl = ref();
const staffEditImageUrl = ref();
const selectedImageUrl = ref();

function openImageModal(imageUrl) {
	selectedImageUrl.value = imageUrl;
	const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
	imageModal.show();
}

async function fetchStaff() {
	const r = await axios.get("/api/staff/")
	staff.value = r.data
}

async function onStaffAdd() {
	const formData = new FormData();

	formData.append('picture', staffPictureRef.value.files[0]);

	formData.set('name', staffToAdd.value.name)
	formData.set('post', staffToAdd.value.post)

	await axios.post("/api/staff/", formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	await fetchStaff();
}

async function staffAddPictureChange() {
	staffAddImageUrl.value = URL.createObjectURL(staffPictureRef.value.files[0])
}
async function staffEditPictureChange() {
	staffEditImageUrl.value = URL.createObjectURL(staffPictureRefEdit.value.files[0])
}

async function onStaffRemoveClick(staff) {
	await axios.delete(`/api/staff/${staff.id}/`);
	await fetchStaff();
}

async function onStaffEditClick(staff) {
	staffToEdit.value = {
		id: staff.id,
		name: staff.name,
		post: staff.post,
		picture: staff.picture
	};
	staffEditImageUrl.value = staff.picture;
}

async function OnUpdateStaffClick() {
	const formData = new FormData();

	formData.append('picture', staffPictureRefEdit.value.files[0]);

	formData.set('name', staffToAdd.value.name)
	formData.set('post', staffToAdd.value.post)

	await axios.put(`/api/staff/${staffToEdit.value.id}/`, formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	await fetchStaff();
}

onBeforeMount(async () => {
	await fetchStaff()
})

</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onStaffAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="staffToAdd.name" required>
						<label for="floatingInput">ФИО</label>
					</div>
				</div>
				<div class="col-3">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="staffToAdd.post" required>
						<label for="floatingInput">Должность</label>
					</div>
				</div>
				<div class="col-3">
					<input class="form-control" type="file" ref="staffPictureRef" @change="staffAddPictureChange()" required>
				</div>
				<div class="col-auto">
					<img :src="staffAddImageUrl" style="max-height: 60px;" alt="">
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-primary">Добавить</button>
				</div>
			</div>
		</form>
	</div>

	<div>
		<div v-for="item in staff" class="staff-item">
			<div>
				{{ item.name }}
			</div>
			<div>
				{{ item.post }}
			</div>
			<div v-show="item.picture">
				<img :src="item.picture" style="max-height: 60px;" @click="openImageModal(item.picture)"
					alt="Картинка персонала" data-bs-toggle="modal" data-bs-target="#imageModal">
			</div>
			<div>
				<button class="btn btn-success" @click="onStaffEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editStaffModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onStaffRemoveClick(item)"><i class="bi bi-trash"></i></button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editStaffModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="staffToEdit.name">
								<label for="floatingInput">ФИО</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="staffToEdit.post">
								<label for="floatingInput">Должность</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col-6">
							<input class="form-control" type="file" ref="staffPictureRefEdit" @change="staffEditPictureChange()"
								required>
						</div>
						<div class="col-auto">
							<img :src="staffEditImageUrl" style="max-height: 60px;" alt="">
						</div>
					</div>
				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
					@click="OnUpdateStaffClick()">Сохранить</button>
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
</template>
<style lang="scss" scoped>
.staff-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.5fr 0.25fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}
.staff-item img {
	cursor: pointer;
}
</style>