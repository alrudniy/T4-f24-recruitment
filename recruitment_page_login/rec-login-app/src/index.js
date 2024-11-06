import Vue from 'vue';
import VueRouter from 'vue-router';
import AdminPage from 'AdminPage.vue';
import HomeownerPage from 'HomeownerPage.vue';
import LoginPage from 'rec_login.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/', component: LoginPage },
  { path: '/admin', component: AdminPage },
  { path: '/homeowner', component: HomeownerPage },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
