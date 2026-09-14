import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/enterprise/:id',
      name: 'enterprise-detail',
      component: () => import('@/views/EnterpriseDetail.vue'),
    },
  ],
})

export default router
