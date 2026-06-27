<script setup lang="ts">
import { computed, ref } from 'vue'

interface LoginResponse {
  success: boolean
  message: string
  token: string | null
}

const emit = defineEmits<{
  authenticated: [payload: { username: string; token: string }]
}>()

const username = ref('admin')
const password = ref('123456')
const confirmPassword = ref('')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const token = ref('')
const mode = ref<'login' | 'register'>('login')

const isLoggedIn = computed(() => token.value.length > 0)
const isRegisterMode = computed(() => mode.value === 'register')
const title = computed(() => (isRegisterMode.value ? 'Create account' : 'Sign in'))
const endpoint = computed(() => (isRegisterMode.value ? '/api/auth/register' : '/api/auth/login'))
const submitText = computed(() => {
  if (loading.value) {
    return isRegisterMode.value ? 'Creating...' : 'Signing in...'
  }

  return isRegisterMode.value ? 'Create account' : 'Sign in'
})

function switchMode(nextMode: 'login' | 'register') {
  mode.value = nextMode
  errorMessage.value = ''
  successMessage.value = ''
  token.value = ''
  confirmPassword.value = ''

  if (nextMode === 'register') {
    username.value = ''
    password.value = ''
  } else {
    username.value = 'admin'
    password.value = '123456'
  }
}

async function submitAuth() {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  token.value = ''

  try {
    if (isRegisterMode.value && password.value !== confirmPassword.value) {
      throw new Error('Passwords do not match')
    }

    const response = await fetch(endpoint.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    const data = (await response.json()) as LoginResponse

    if (!response.ok || !data.success || !data.token) {
      throw new Error(data.message || 'Request failed')
    }

    token.value = data.token
    successMessage.value = data.message
    emit('authenticated', { username: username.value, token: data.token })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Request failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="login-page">
    <section class="login-panel">
      <div class="login-copy">
        <p class="eyebrow">Mini Agent</p>
        <h1>{{ title }}</h1>
      </div>

      <form class="login-form" @submit.prevent="submitAuth">
        <label>
          <span>Username</span>
          <input v-model="username" autocomplete="username" name="username" type="text" />
        </label>

        <label>
          <span>Password</span>
          <input
            v-model="password"
            :autocomplete="isRegisterMode ? 'new-password' : 'current-password'"
            name="password"
            type="password"
          />
        </label>

        <label v-if="isRegisterMode">
          <span>Confirm password</span>
          <input
            v-model="confirmPassword"
            autocomplete="new-password"
            name="confirmPassword"
            type="password"
          />
        </label>

        <button :disabled="loading" type="submit">
          {{ submitText }}
        </button>

        <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
        <p v-if="isLoggedIn" class="message success">{{ successMessage }}. Token: {{ token }}</p>

        <div class="mode-switch">
          <span>{{ isRegisterMode ? 'Already have an account?' : 'Need an account?' }}</span>
          <button
            class="link-button"
            type="button"
            @click="switchMode(isRegisterMode ? 'login' : 'register')"
          >
            {{ isRegisterMode ? 'Sign in' : 'Register' }}
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #f4f7fb;
}

.login-panel {
  width: min(100%, 900px);
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 100px;
  align-items: center;
  padding: 40px;
  background: #ffffff;
  border: 1px solid #d9e2ef;
  border-radius: 8px;
  box-shadow: 0 18px 45px rgba(34, 49, 70, 0.12);
}

.login-copy {
  color: #1d2735;
}

.eyebrow {
  margin-bottom: 12px;
  color: #0f766e;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

h1 {
  margin-bottom: 14px;
  color: #111827;
  font-size: 42px;
  font-weight: 800;
  line-height: 1.1;
}

.login-form {
  display: grid;
  gap: 16px;
}

label {
  display: grid;
  gap: 8px;
  color: #334155;
  font-size: 14px;
  font-weight: 700;
}

input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  color: #111827;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font: inherit;
}

input:focus {
  outline: 3px solid rgba(15, 118, 110, 0.18);
  border-color: #0f766e;
}

button {
  height: 44px;
  color: #ffffff;
  background: #0f766e;
  border: 0;
  border-radius: 6px;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

button:disabled {
  cursor: wait;
  opacity: 0.7;
}

.mode-switch {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: center;
  color: #526071;
  font-size: 14px;
}

.link-button {
  width: auto;
  height: auto;
  padding: 0;
  color: #0f766e;
  background: transparent;
  border: 0;
  font-weight: 800;
}

.message {
  padding: 12px;
  border-radius: 6px;
  overflow-wrap: anywhere;
}

.error {
  color: #991b1b;
  background: #fee2e2;
}

.success {
  color: #14532d;
  background: #dcfce7;
}

@media (max-width: 760px) {
  .login-panel {
    grid-template-columns: 1fr;
    padding: 24px;
  }

  h1 {
    font-size: 34px;
  }
}
</style>
