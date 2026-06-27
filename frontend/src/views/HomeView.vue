<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  username: string
  token: string
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  loginRequested: []
  logout: []
}>()

interface Conversation {
  id: number
  title: string
  preview: string
  time: string
}

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  time: string
}

const conversations = ref<Conversation[]>([

])

const activeConversationId = ref(1)
const draft = ref('')
const messages = ref<ChatMessage[]>([

])

const activeConversation = computed(() =>
  conversations.value.find((conversation) => conversation.id === activeConversationId.value),
)

const accountLabel = computed(() => (props.isAuthenticated ? props.username : 'Not signed in'))
const accountDetail = computed(() => {
  if (!props.isAuthenticated) {
    return 'Guest session'
  }

  if (props.token.length <= 12) {
    return `Token ${props.token}`
  }

  return `Token ${props.token.slice(0, 8)}...${props.token.slice(-4)}`
})

function selectConversation(id: number) {
  activeConversationId.value = id
}

function sendMessage() {
  const content = draft.value.trim()

  if (!content) {
    return
  }

  const time = new Intl.DateTimeFormat('en', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(new Date())

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content,
    time,
  })

  draft.value = ''

  window.setTimeout(() => {
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: props.isAuthenticated
        ? `Received: ${content}`
        : 'Please sign in to connect this message to your account.',
      time,
    })
  }, 300)
}
</script>

<template>
  <main class="workspace">
    <aside class="sidebar">
      <div class="sidebar-header">
        <p class="eyebrow">Mini Agent</p>
        <h1>Conversations</h1>
      </div>

      <div class="history-list" aria-label="Conversation history">
        <button
          v-for="conversation in conversations"
          :key="conversation.id"
          class="history-item"
          :class="{ active: conversation.id === activeConversationId }"
          type="button"
          @click="selectConversation(conversation.id)"
        >
          <span class="history-title">{{ conversation.title }}</span>
          <span class="history-preview">{{ conversation.preview }}</span>
          <span class="history-time">{{ conversation.time }}</span>
        </button>
      </div>

      <section class="account-panel">
        <div class="avatar">{{ username.slice(0, 1).toUpperCase() }}</div>
        <div class="account-copy">
          <strong>{{ accountLabel }}</strong>
          <span>{{ accountDetail }}</span>
        </div>
        <button
          v-if="isAuthenticated"
          class="account-button"
          type="button"
          @click="emit('logout')"
        >
          Logout
        </button>
        <button v-else class="account-button" type="button" @click="emit('loginRequested')">
          Login
        </button>
      </section>
    </aside>

    <section class="chat-panel">
      <header class="chat-header">
        <div>
          <p class="eyebrow">Live messages</p>
          <h2>{{ activeConversation?.title }}</h2>
        </div>
        <span class="status" :class="{ guest: !isAuthenticated }">
          {{ isAuthenticated ? 'Signed in' : 'Guest mode' }}
        </span>
      </header>

      <div class="message-list" aria-live="polite">
        <article
          v-for="message in messages"
          :key="message.id"
          class="chat-message"
          :class="message.role"
        >
          <p>{{ message.content }}</p>
          <time>{{ message.time }}</time>
        </article>
      </div>

      <form class="composer" @submit.prevent="sendMessage">
        <input v-model="draft" placeholder="Type a message..." type="text" />
        <button type="submit">Send</button>
      </form>
    </section>
  </main>
</template>

<style scoped>
.workspace {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  background: #eef3f8;
  color: #172033;
}

.sidebar {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 20px;
  padding: 24px;
  background: #ffffff;
  border-right: 1px solid #d8e1ec;
}

.sidebar-header h1,
.chat-header h2 {
  margin: 0;
  color: #111827;
  font-size: 24px;
  font-weight: 800;
  line-height: 1.2;
}

.eyebrow {
  margin-bottom: 8px;
  color: #0f766e;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

.history-list {
  display: grid;
  align-content: start;
  gap: 10px;
  overflow-y: auto;
}

.history-item {
  display: grid;
  gap: 6px;
  width: 100%;
  padding: 14px;
  text-align: left;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
}

.history-item.active {
  background: #e6f5f3;
  border-color: #0f766e;
}

.history-title {
  color: #172033;
  font-weight: 800;
}

.history-preview,
.history-time,
.account-copy span {
  color: #64748b;
  font-size: 13px;
}

.account-panel {
  display: grid;
  grid-template-columns: 40px 1fr auto;
  gap: 12px;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.avatar {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  color: #ffffff;
  background: #0f766e;
  border-radius: 50%;
  font-weight: 800;
}

.account-copy {
  display: grid;
  min-width: 0;
}

.account-copy strong,
.account-copy span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-button,
.composer button {
  height: 38px;
  padding: 0 14px;
  color: #ffffff;
  background: #0f766e;
  border: 0;
  border-radius: 6px;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.chat-panel {
  min-width: 0;
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 32px;
  background: #ffffff;
  border-bottom: 1px solid #d8e1ec;
}

.status {
  padding: 6px 10px;
  color: #14532d;
  background: #dcfce7;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;
}

.status.guest {
  color: #475569;
  background: #e2e8f0;
}

.message-list {
  display: grid;
  align-content: end;
  gap: 14px;
  padding: 32px;
  overflow-y: auto;
}

.chat-message {
  width: min(680px, 82%);
  display: grid;
  gap: 8px;
  padding: 14px 16px;
  border-radius: 8px;
}

.chat-message.assistant {
  justify-self: start;
  background: #ffffff;
  border: 1px solid #d8e1ec;
}

.chat-message.user {
  justify-self: end;
  color: #ffffff;
  background: #0f766e;
}

.chat-message p {
  margin: 0;
}

.chat-message time {
  color: currentColor;
  font-size: 12px;
  opacity: 0.72;
}

.composer {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  padding: 20px 32px;
  background: #ffffff;
  border-top: 1px solid #d8e1ec;
}

.composer input {
  min-width: 0;
  height: 42px;
  padding: 0 14px;
  color: #111827;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font: inherit;
}

.composer input:focus {
  outline: 3px solid rgba(15, 118, 110, 0.18);
  border-color: #0f766e;
}

@media (max-width: 760px) {
  .workspace {
    grid-template-columns: 1fr;
  }

  .sidebar {
    min-height: auto;
    grid-template-rows: auto auto auto;
    border-right: 0;
    border-bottom: 1px solid #d8e1ec;
  }

  .chat-panel {
    min-height: 60vh;
  }

  .chat-header,
  .message-list,
  .composer {
    padding-left: 20px;
    padding-right: 20px;
  }

  .chat-message {
    width: 100%;
  }
}
</style>
