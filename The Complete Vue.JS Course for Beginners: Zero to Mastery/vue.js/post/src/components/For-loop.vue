<template>
    <h1 id="pages3">For Loop</h1>
    <ul>
        <li v-for="program in technology" :key="program">
            {{ program }}
        </li>
    </ul>
    <br/>
    <ul>
        <li v-for="data in user" :key="data.name"> Name is : {{ data.name }}</li>
        <li v-for="data in user" :key="data.name"> Email is : {{ data.Email }}</li>
        <li v-for="data in user" :key="data.name"> Contact is : {{ data.contact }}</li>
    </ul>
    </template>
    <script>
    export default {
    name: "For-loop",
    data() {
    return {
    technology: ["PHP", "Javascript", "C++", "C-sharp",],
    user:[
        {
        name: "jack",
        Email:"jack002@gmail.com",
        contact:+94782559870,
    },
    {
        name: "Stark",
        Email:"stark002@gmail.com",
        contact:+783482559870,
    },
    {
        name: "John",
        Email:"john002@gmail.com",
        contact:+934873470,
    },
   ],
    };
    },
    };
    </script>
    <style>
    #pages3 {
    color: rgb(211, 25, 0);
    }
    </style>