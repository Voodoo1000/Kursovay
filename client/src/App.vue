<script setup>

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
							<a class="nav-item dropdown-toggle link" href="#" role="button" data-bs-toggle="dropdown"
								aria-expanded="false" >
								Пользователь
							</a>
							<ul class="dropdown-menu">
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
