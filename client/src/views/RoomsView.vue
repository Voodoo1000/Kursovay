<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import _ from 'lodash';

const rooms = ref([])

const roomToAdd = ref({
	number: '',
});
const roomToEdit = ref({
	number: '',
});
const stats = ref({});

async function fetchStats() {
	const r = await axios.get("/api/rooms/stats/");
	stats.value = r.data;
}

async function onRoomAdd() {
	await axios.post("/api/rooms/", {
		...roomToAdd.value
	});
	await fetchRooms();
}

async function onRoomRemoveClick(room) {
	await axios.delete(`/api/rooms/${room.id}/`);
	await fetchRooms();
}

async function onRoomEditClick(room) {
	roomToEdit.value = { ...room };
}

async function onUpdateRoomClick() {
	await axios.put(`/api/rooms/${roomToEdit.value.id}/`, {
		...roomToEdit.value,
	});
	await fetchRooms();
}

async function fetchRooms() {
	const r = await axios.get("/api/rooms/")
	rooms.value = r.data
}

onBeforeMount(async () => {
	await fetchRooms()
})

</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onRoomAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="text" class="form-control" v-model="roomToAdd.number" required>
						<label for="floatingInput">Номер комнаты</label>
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
		<div v-for="item in rooms" class="room-item">
			<div>
				{{ item.number }}
			</div>
			<div>
				<button class="btn btn-success" @click="onRoomEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editRoomModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onRoomRemoveClick(item)"><i class="bi bi-trash"></i></button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editRoomModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="text" class="form-control" v-model="roomToEdit.number">
								<label for="floatingInput">Номер комнаты</label>
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
					<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
						@click="onUpdateRoomClick()">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Модальное окно для статистики -->
	<div class="modal fade" id="statsModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Статистика комнат</h5>
				</div>
				<div class="modal-body">
					<p>Количество комнат: {{ stats.count }}</p>
					<p>Максимальный ID комнаты: {{ stats.max }}</p>
					<p>Минимальный ID комнаты: {{ stats.min }}</p>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.room-item {
	padding: 0.5rem;
	margin: 0.5rem 0;
	border: 1px solid silver;
	border-radius: 8px;
	display: grid;
	grid-template-columns: 1fr auto auto;
	gap: 8px;
	align-items: center;

}
</style>
