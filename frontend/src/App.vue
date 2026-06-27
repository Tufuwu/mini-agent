<script setup lang="ts">
import { ref } from 'vue'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'

const user = ref<{ username: string; token: string } | null>(null)
const showLogin = ref(false)

function handleAuthenticated(payload: { username: string; token: string }) {
  user.value = payload
  showLogin.value = false
}

function handleLogout() {
  user.value = null
}

function handleLoginRequested() {
  showLogin.value = true
}
</script>

<template>
  <LoginView v-if="showLogin" @authenticated="handleAuthenticated" />
  <HomeView
    v-else
    :is-authenticated="Boolean(user)"
    :token="user?.token ?? ''"
    :username="user?.username ?? 'Guest'"
    @login-requested="handleLoginRequested"
    @logout="handleLogout"
  />
</template>
