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
     <div ><h1 v-html="emailaddress"></h1></div>
     <div v-html="id" ></div>
     <Newuser />
    

    </template>
    <script>
    import Newuser from "./newuser.vue";
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
        //     users: [{
        //         name:'jackson',
        //         email:'jackson454@gmail.com'
        //     },
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
        names: "peter",
        emailaddress:"<h3>peter123@gmail.com<h3/>",
        id: '06343455',
        };
    },
    components: {Newuser},
    };
    </script>

    <style>
    h3{
    color: blue;
    font-weight: bold;
    }
    </style>