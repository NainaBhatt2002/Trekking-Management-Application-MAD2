import { createRouter, createWebHistory } from 'vue-router';

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import AdminDashboard from "../views/admin/Dashboard.vue";
import Treks from "../views/admin/Treks.vue";
import Staff from "../views/admin/Staff.vue";
import Users from "../views/admin/Users.vue";
import Bookings from "../views/admin/Bookings.vue";
import StaffDashboard from "../views/staff/dashboard.vue";
import TrekkerDashboard from "../views/trekker/dashboard.vue";
import Reports from "../views/admin/Reports.vue";
import AssignedTreks from "../views/staff/AssignedTreks.vue"
import ManageTrek from "../views/staff/ManageTrek.vue"

const routes = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
  path: "/",
  redirect: "/login",
},
{
  path: "/login",
  component: LoginView,
},
{
  path: "/register",
  component: RegisterView,
},
    
    {
  path: "/admin/dashboard",
  component: AdminDashboard,
  meta: {
    requiresAuth: true,
    role: "admin",
  },
},
{
  path: "/admin/treks",
  component: Treks,
  meta: {
    requiresAuth: true,
    role: "admin",
  },
},
{
  path: "/admin/staff",
  component: Staff,
  meta: {
    requiresAuth: true,
    role: "admin",
  },
},
{
  path: "/admin/users",
  component: Users,
  meta: {
    requiresAuth: true,
    role: "admin",
  },
},
{
  path: "/admin/bookings",
  component: Bookings,
  meta: {
    requiresAuth: true,
    role: "admin",
  },
},
{
  path: "/admin/reports",
  component: Reports,
  meta: {
    requiresAuth: true,
    role: "admin",
  },
},
{
  path: "/staff/dashboard",
  component: StaffDashboard,
  meta: {
    requiresAuth: true,
    role: "staff",
  },
},
{
  path: "/staff/treks",
  component: AssignedTreks,
  meta: {
    requiresAuth: true,
    role: "staff",
  },
},
{
  path: "/staff/treks/:id",
  component: ManageTrek,
  meta: {
    requiresAuth: true,
    role: "staff",
  },
},
{
  path: "/trekker/dashboard",
  component: TrekkerDashboard,
  meta: {
    requiresAuth: true,
    role: "trekker",
  },
},
]
});

routes.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if(to.meta.requiresAuth && !token) {
    return next('/login');
  }

  if(to.meta.role && to.meta.role !== role) {
    return next('/login');
  }

  next();
});

export default routes;
