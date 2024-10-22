<script setup>
import axios from 'axios';
import { computed, ref, onBeforeMount } from 'vue';
import _ from 'lodash';

const students = ref([]);
const duty = ref([])
const dutyToAdd = ref({
	date: '',
	student: null
});
const dutyToEdit = ref({
	date: '',
	student: null
});

async function fetchStudents() {
	const r = await axios.get("/api/students/")
	students.value = r.data
}

async function fetchDuty() {
	const r = await axios.get("/api/dutySchedule/")
	duty.value = r.data
}

async function onDutyAdd() {
	await axios.post("/api/dutySchedule/", {
		...dutyToAdd.value
	});
	await fetchDuty();
}

async function onDutyRemoveClick(duty) {
	await axios.delete(`/api/dutySchedule/${duty.id}/`);
	await fetchDuty();
}

async function onDutyEditClick(duty) {
	dutyToEdit.value = {
		id: duty.id,
		date: duty.date,
		student_id: duty.student.id,
	};
}

async function onUpdateDutyClick() {
	await axios.put(`/api/dutySchedule/${dutyToEdit.value.id}/`, {
		...dutyToEdit.value,
	});
	await fetchDuty();
}

onBeforeMount(async () => {
	await fetchStudents()
	await fetchDuty()
})
</script>
<template>
	<div class="p-2">
		<form @submit.prevent.stop="onDutyAdd()">
			<div class="row">
				<div class="col">
					<div class="form-floating">
						<input type="date" class="form-control" v-model="dutyToAdd.date" required>
						<label for="floatingInput">Дата</label>
					</div>
				</div>
				<div class="col-5">
					<div class="form-floating">
						<select class="form-select" v-model="dutyToAdd.student_id" required>
							<option :value="s.id" v-for="s in students">{{ s.name }}</option>
						</select>
						<label for="floatingInput">Студент</label>
					</div>
				</div>
				<div class="col-auto d-flex align-self-center">
					<button class="btn btn-primary">Добавить</button>
				</div>
			</div>
		</form>
	</div>

	<div>
		<div v-for="item in duty" class="duty-item">
			<div>
				{{ item.date }}
			</div>
			<div>
				{{ item.student.name }}
			</div>
			<div>
				<button class="btn btn-success" @click="onDutyEditClick(item)" data-bs-toggle="modal"
					data-bs-target="#editDutyModal">
					<i class="bi bi-pen"></i>
				</button>
			</div>
			<div>
				<button class="btn btn-danger" @click="onDutyRemoveClick(item)"><i class="bi bi-trash"></i></button>
			</div>
		</div>
	</div>
	<!-- Modal -->
	<div class="modal fade" id="editDutyModal" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Редактировать</h5>
				</div>
				<div class="modal-body m">
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<input type="date" class="form-control" v-model="dutyToEdit.date">
								<label for="floatingInput">Дата</label>
							</div>
						</div>
					</div>
					<div class="row p-1">
						<div class="col">
							<div class="form-floating">
								<select class="form-select" v-model="dutyToEdit.student_id" required>
									<option :value="r.id" v-for="r in students">{{ r.name }}</option>
								</select>
								<label for="floatingInput">Студент</label>
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
					<button type="button" class="btn btn-primary" data-bs-dismiss="modal"
						@click="onUpdateDutyClick()">Сохранить</button>
				</div>
			</div>
		</div>
	</div>
</template>
<style lang="scss" scoped>
.duty-item {
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