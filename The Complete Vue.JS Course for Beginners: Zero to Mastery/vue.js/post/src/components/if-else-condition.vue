<template>
    <h1 id="pages2" v-if="display">If  Conditon</h1>
    <!-- <h1 id="pages2" v-if="show">Else Conditon 2</h1> -->
    <h1 id="pages2" v-else>Else Conditon</h1>
    <!-- <button v-on:click="display = true">Click Here</button> -->
    <button v-on:click="display = !display">Click Here</button>
    </template>
    <script>
    export default {
    name: "if-else-condition",
    data() {
    return {
        display: false,
        // show: true
    };
    },
    };
    </script>
    <style>
    #pages2 {
    color: rgb(226, 100, 27);
    }
    </style>