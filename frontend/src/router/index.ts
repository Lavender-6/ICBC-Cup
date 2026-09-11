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
      path: '/datasets',
      name: 'datasets',
      component: () => import('@/views/DatasetManagement.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/RecognitionHistory.vue'),
    },
  ],
})

export default router
