import { createWebHistory, createRouter} from "vue-router";
import Home from "./components/home.vue";
import Login from "./components/login.vue";
import Signup from "./components/signup.vue";
const routes=[
{
    name: "Home",
    path: '/',
    component: Home,
},
{
    name: "Login",
    path: '/login',
    component: Login,
},
{
    name: "Signup",
    path: '/signup',
    component: Signup,
},
];

const  router = createRouter({
    history: createWebHistory(),
    routes,
});
export default router;