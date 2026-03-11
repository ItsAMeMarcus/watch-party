import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Room from '../views/Room.vue';

const routes = [
  { 
    path: '/', 
    name: 'Home', 
    component: Home 
  },
  { 
    path: '/room/:id', 
    name: 'Room', 
    component: Room 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;