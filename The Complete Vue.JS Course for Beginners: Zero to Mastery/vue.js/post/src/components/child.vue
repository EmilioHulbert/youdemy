<template>
    <h1>child components</h1>
    <h3>{{ name }}</h3>
    <h3>{{ user.email }}</h3>
    <button v-on:click="getData()">Call The Function</button>
    <ul>
        <li v-for="item in users" :key="item.name">
            <Newuser :data="item"/>
            {{ item.name }}    
            {{ item.email }}    
        </li>
    </ul>
    <!-- <h1>{{ emailaddress }}</h1> -->
     <!-- <div v-html="emailaddress"></div> -->
     <!-- <div ><h1 v-html="emailaddress"></h1></div> -->
     <!-- <div v-html="id" ></div> -->
     <h1>Class Binding</h1>
     <!-- <h3 :class="{yellow:true}">Dynamic class</h3> -->
     <h3 :class="{ yellow:color }">Dynamic class</h3> 
     <button v-on:click="color = !color">Change the color</button>
     <!-- <Newuser/> -->
     <!-- <Newuser :data="{ name: 'Default User', email: 'default@example.com' }"/> -->
    <School />
    <Form/>
    <Props />
    <ComputedProperty />
    <Watchers />
    <BeforeCreate />
</template>
    <script>
    import Newuser from "./newuser.vue";
    import School from "./school.vue";
    import Form from "./loginform.vue";
    import Props from "./props.vue";
    import ComputedProperty from "./computedproperty.vue";
    import Watchers from "./watchers.vue"; 
    import BeforeCreate from "./beforecreate.vue";
    export default
    {
    name: "child-components",
    props:{
        name: String,
        user: Object,
        getData: Function, 
},
    data(){
        return {
            // users: [{
            //     name:'jackson',
            //     email:'jackson454@gmail.com'
            // },
        //     {
        //         name:'jamws',
        //         email:'jamsw8454@gmail.com'
        //     },
        //     {
        //         name:'Henry',
        //         email:'Henry@gmail.com'
        //     },
        //     {
        //         name:'Tony',
        //         email:'tony3657@gmail.com'
        //     },
        //     {
        //         name:'Samuel',
        //         email:'Samuel890@gmail.com'
        //     },
        // ],
        // names: "peter",
        // emailaddress:"<h3>peter123@gmail.com<h3/>",
        // id: '06343455',
        color:false,
        };
    },
    components: {Newuser, School,Form,Props,ComputedProperty,Watchers,BeforeCreate,},
    };
    </script>

    <style>
    /* h3{
    color: blue;
    font-weight: bold;
    } */
    .yellow{
    color: blue;
    font-weight: bold;
    background-color: yellow;
    width: 150px;
    height: 50px;
    }
    </style>