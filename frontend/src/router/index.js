import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import TagPage from '../views/TagPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/tag/:slug',
    name: 'TagPage',
    component: TagPage
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminLayout,
    redirect: '/admin/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/index.vue')
      },
      {
        path: 'sites',
        name: 'Sites',
        component: () => import('../views/sites/index.vue')
      },
      {
        path: 'hospitals',
        name: 'Hospitals',
        component: () => import('../views/hospitals/index.vue')
      },
      // {
      //   path: 'hospitals/edit/:id?',
      //   name: 'HospitalEdit',
      //   component: () => import('../views/hospitals/HospitalEdit.vue')
      // },
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('../views/articles/index.vue')
      },
      // {
      //   path: 'articles/edit/:id?',
      //   name: 'ArticleEdit',
      //   component: () => import('../views/articles/ArticleEdit.vue')
      // },
      {
        path: 'appointments',
        name: 'Appointments',
        component: () => import('../views/appointments/index.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/users/index.vue')
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('../views/categories/index.vue')
      },
      {
        path: 'geo',
        name: 'Geo',
        component: () => import('../views/geo/index.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path.startsWith('/admin') && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
