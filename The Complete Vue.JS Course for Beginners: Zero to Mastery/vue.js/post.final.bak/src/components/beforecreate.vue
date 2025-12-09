<template>
    <!-- <h1>beforeCreate and created</h1> -->
    <!-- <h1>beforeMount and Mounted</h1> -->
     <!-- <h1 ref="adding">count:{{counter}}</h1> -->
<!-- <button v-on:click="counter = counter + 1"> Update the number</button> -->
<h1>beforeunmount and unmounted</h1>
<button v-on:click="show = !show">Togglebar</button>
<Lifecyclechild v-if="show" />
 </template>
 <script>
 import Lifecyclechild from "./lifecyclechild.vue";
    export default {
   name: "beforecreate-com",
   data(){
    // console.error("created");
    return{
        counter: 0,
        show:true,
    };
   },
//    beforeCreate(){
//         alert("Page loading...");
//     },
//     created(){
//         alert("Page Loaded");
//     },
// beforeMount(){
//     console.log("This is a beforeMount Method", this.$el);
// },
// mounted(){
//     console.log("This is a mounted Method", this.$el);
// },
// beforeUpdate(){
// // console.log("beforeUpdate", this.counter);
// console.log("beforeUpdate", this.$refs["adding"].textContent);
// },
// updated(){
//     console.log("updated", this.$refs["adding"].textContent);
// },

components:{Lifecyclechild,},
    };
   
 </script>
 
 <style>
    h1 {
    color: rgb(235, 20, 20);
    font-weight: bold;
}
</style>