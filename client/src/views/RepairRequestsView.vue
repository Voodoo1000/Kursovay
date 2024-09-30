<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import _ from 'lodash';

const requests = ref([]);
const rooms = ref([])
const staff = ref([])
const statusOptions = ref([
	{ value: 'new', label: 'Новая' },
	{ value: 'in_progress', label: 'В процессе' },
	{ value: 'completed', label: 'Завершена' },
	{ value: 'cancelled', label: 'Отменена' }
]);

const requestToAdd = ref({
	date: '',
	description: '',
	status: 'new',
	room: null,
	staff: null
});
const requestToEdit = ref({
	date: '',
	description: '',
	status: null,
	room: null,
	staff: null
});

async function fetchRequests() {
	const r = await axios.get("/api/repairRequests/")
	requests.value = r.data
}

async function fetchRooms() {
	const r = await axios.get("/api/rooms/")
	rooms.value = r.data
}

async function fetchStaff() {
	const r = await axios.get("/api/staff/")
	staff.value = r.data
}

async function onRequestAdd() {
	await axios.post("/api/repairRequests/", {
		...requestToAdd.value
	});
	await fetchRequests();
}

async function onRequestRemoveClick(request) {
	await axios.delete(`/api/repairRequests/${request.id}/`);
	await fetchRequests();
}

async function onRequestEditClick(request) {
	requestToEdit.value = { ...request };
}

async function OnUpdateRequestClick() {
	await axios.put(`/api/repairRequests/${requestToEdit.value.id}/`, {
		...requestToEdit.value,
	});
	await fetchRequests();
}

onBeforeMount(async () => {
	await fetchRequests()
	await fetchRooms()
	await fetchStaff()
})
</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onRequestAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="requestToAdd.description" required>
						<label for="floatingInput">Описание проблемы</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<input type="date" class="form-control" v-model="requestToAdd.date" required>
						<label for="floatingInput">Дата</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<select class="form-select" v-model="requestToAdd.status" required>
							<option :value="option.value" v-for="option in statusOptions" :key="option.value">{{ option.label }}
							</option>
						</select>
						<label for="floatingInput">Статус заявки</label>
					</div>
				</div>
				<div class="col-1">
					<div class="form-floating">
						<select class="form-select" v-model="requestToAdd.room_id" required>
							<option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
						</select>
						<label for="floatingInput">Комната</label>
					</div>
				</div>
				<div class="col-2">
					<div class="form-floating">
						<select class="form-select" v-model="requestToAdd.staff_id" required>
							<option :value="s.id" v-for="s in staff">{{ s.post }}({{ s.name }})</option>
						</select>
						<label for="floatingInput">Персонал</label>
					</div>
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-primary">Добавить</button>
				</div>
			</div>
		</form>
	</div>

	<div>
		<div v-for="item in requests" class="request-item">
			<div>
				{{ item.description }}
			</div>
			<div>
				{{ item.date }}
			</div>
			<div>
				{{ item.status_display }}
			</div>
			<div>
				{{ item.room.number }}
			</div>
			<div>
				{{ item.staff.post }}({{ item.staff.name }})
			</div>
			<div>
				<button class="btn btn-success" @click="onRequestEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editRequestModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onRequestRemoveClick(item)"><i class="bi bi-trash"></i></button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editRequestModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="requestToEdit.description" required>
								<label for="floatingInput">Описание проблемы</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col-4">
							<div class="form-floating">
								<input type="date" class="form-control" v-model="requestToEdit.date" required>
								<label for="floatingInput">Дата</label>
							</div>
						</div>
						<div class="col-4">
							<div class="form-floating">
								<select class="form-select" v-model="requestToEdit.status" required>
									<option :value="option.value" v-for="option in statusOptions" :key="option.value">{{ option.label }}
									</option>
								</select>
								<label for="floatingInput">Статус заявки</label>
							</div>
						</div>
						<div class="col-4">
							<div class="form-floating">
								<select class="form-select" v-model="requestToEdit.room_id" required>
									<option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
								</select>
								<label for="floatingInput">Комната</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<select class="form-select" v-model="requestToEdit.staff_id" required>
									<option :value="s.id" v-for="s in staff">{{ s.post }}({{ s.name }})</option>
								</select>
								<label for="floatingInput">Персонал</label>
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
					<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
						@click="OnUpdateRequestClick()">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
</template>
<style lang="scss" scoped>
.request-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 0.7fr 0.3fr 0.3fr 0.3fr 1fr auto auto;
	gap: 8px;
	align-items: center;
}
</style>