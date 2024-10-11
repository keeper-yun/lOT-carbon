import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '@/components/Login.vue';
import index from '@/views/index.vue';
import CarbonMange from '@/views/CarbonMange.vue';
import Register from '@/components/Register.vue';
import Factorycompare from '@/views/Factorycompare.vue';
import UserMange from '@/views/UserMange.vue';
import UpdateUser from '@/views/UpdateUser.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/Register',
    name: 'Register',
    component: Register
  },
  {
    path:'/',
    name:'碳中和监测管理',
    component:index,
    children:[
      {
        path: '/CarbonMange',
        name: '碳排放实时信息',
        component: CarbonMange,
        show: true
      },
      {
        path: '/Factorycompare',
        name: '碳排放记录',
        component: Factorycompare,
        show: true
      }
    ]
  },
  {
    path: '/navigation',
    name: '管理员',
    component: index,
    children:[
      {
        path: '/UserMange',
        name: '管理员信息',
        component: UserMange,
        show: true
      },
      {
        path: '/UpdateUser',
        name: '修改管理权限',
        component: UpdateUser,
        show: false
      }
      
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login','/Register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = sessionStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
});

export default router
