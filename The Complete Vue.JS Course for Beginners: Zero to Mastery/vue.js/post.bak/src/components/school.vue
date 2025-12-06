<template>
    <!-- <h1>Main compoenent</h1> -->
    <h1>{{childUser}}</h1>
    <!-- <Teacher /> -->
    <Teacher name="Bruce" :getUser="getUserName" />
    <Student name="Jackson" />
    
    </template>
    <script>
    import Teacher from "./Teacher.vue";
    import Student from "./student.vue";
    export default {
    name: "main-com",
    methods: {
        getUserName(name){
            // alert(name);
            this.childUser = name;
        },
       
    },
    data(){
        return{
            childUser: "",
        };
    },
    components: { Teacher, Student},
    };
    </script>