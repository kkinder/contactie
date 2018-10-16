import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/add/',
            name: 'add-contact',
            component: () => import(/* webpackChunkName: "add-contact" */ './views/AddContact.vue')
        },
        {
            path: '/contact/:contactId',
            name: 'view-contact',
            component: () => import(/* webpackChunkName: "contact" */ './views/Contact.vue')
        }
    ]
})
