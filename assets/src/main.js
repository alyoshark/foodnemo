import Vue from 'vue'
import app from './app.vue'
import VueRouter from 'vue-router'

Vue.config.debug = process.env.NODE_ENV !== 'production'
Vue.use(VueRouter)
const router = new VueRouter()
const App = Vue.extend(app)
router.start(App, 'body')
