import { createWebHistory, createRouter} from "vue-router";
import Home from "./components/home.vue";
import Login from "./components/login.vue";
import Signup from "./components/signup.vue";
import PNF from './components/PNF.vue'
const routes=[
{
    name: "Home",
    path: '/',
    component: Home,
},
{
    name: "Login",
    path: '/login/:name',
    component: Login,
},
{
    name: "Signup",
    path: '/signup/:name',
    component: Signup,
},
{
    name: "Notfound",
    path: '/:pathMatch(.*)*',
    component: PNF,
},
];

const  router = createRouter({
    history: createWebHistory(),
    routes,
});
export default router;