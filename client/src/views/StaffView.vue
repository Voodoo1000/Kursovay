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

async function fetchStaff() {
	const r = await axios.get("/api/staff/")
	staff.value = r.data
}

async function onStaffAdd() {
	await axios.post("/api/staff/", {
		...staffToAdd.value
	});
	await fetchStaff();
}

async function onStaffRemoveClick(staff) {
	await axios.delete(`/api/staff/${staff.id}/`);
	await fetchStaff();
}

async function onStaffEditClick(staff) {
	staffToEdit.value = { ...staff };
}

async function OnUpdateStaffClick() {
	await axios.put(`/api/staff/${staffToEdit.value.id}/`, {
		...staffToEdit.value,
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
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
						<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
							@click="OnUpdateStaffClick()">Сохранить</button>
					</div>
				</div>
			</div>
		</div>
</template>
<style scoped>
.staff-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.5fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}
</style>