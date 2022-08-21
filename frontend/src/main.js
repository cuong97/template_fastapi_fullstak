import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './assets/main.css'

const app = createApp(App)

router.beforeEach((to, from) => {
  // ...
  // explicitly return false to cancel the navigation
  if (to.name !== 'login') console.log("!login")
  else console.log("abcbcb")
})

app.use(router)

app.mount('#app')
