<template>
    <h1>beforeCreate and created</h1>
 </template>
 <script>
    export default {
   name: "beforecreate-com",
   data(){
    console.error("created")
   },
   beforeCreate(){
        alert("Page loading...");
    },
    created(){
        alert("Page Loaded");
    },
    };
   
 </script>
 
 <style>
    h1 {
    color: rgb(235, 20, 20);
    font-weight: bold;
}
</style>