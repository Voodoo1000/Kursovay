<script setup>
import { storeToRefs } from 'pinia';
import useUserStore from './stores/userStore';
import { useToast } from 'vue-toastification';
import axios from 'axios';
import Cookies from 'js-cookie'; 

const userStore = useUserStore();
const { isAuthenticated,	username,	userId } = storeToRefs(userStore);
const toast = useToast();

async function logout() {
    const csrfToken = Cookies.get('csrftoken');
    try {
        const response = await axios.post('/api/user/logout/', {}, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        if (response.data.success) {
            userStore.resetUser();
            window.location.reload();
        } else {
            toast.error('Ошибка выхода, попробуйте еще раз.');
        }
    } catch (error) {
        console.error('Ошибка выхода:', error);
        toast.error('Ошибка выхода, попробуйте еще раз.');
    }
}

</script>
<template>
	<div class="container">
		<nav class="navbar navbar-expand-lg bg-body-tertiary">
			<div class="container-fluid">
				<a class="navbar-brand">Общежитие</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
					aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse justify-content-between" id="navbarNav">
					<ul class="navbar-nav">
						<li class="nav-item">
							<router-link class="nav-link" to="/">Студенты</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/rooms">Комнаты</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/dutySchedule">График дежурств</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/staff">Персонал общежития </router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/repairRequests">Заявки на ремонт</router-link>
						</li>
					</ul>
					<ul class="navbar-nav">
						<li class="nav-item dropdown">
							<a class="nav-item dropdown-toggle link" href="#" role="button" data-bs-toggle="dropdown"	aria-expanded="false">
								{{ username }}
							</a>
							<ul class="dropdown-menu">
								<li class="nav-item"><router-link class="dropdown-item" to="/login">Войти</router-link></li>
								<li class="nav-item"><a class="dropdown-item" @click.prevent="logout()">Выход</a></li>
								<li><a class="dropdown-item" href="/admin">Админка</a></li>
							</ul>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	</div>
	<div class="container">
		<router-view />
	</div>
</template>

<style lang="scss" scoped>
.link {
	text-decoration: none;
	color: #666;
}
</style>
