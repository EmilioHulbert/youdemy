<template>
    <h1>Simple Form</h1>
<form action="">
    <label for="">Username</label>&nbsp;
    <input type="text" name="" id="" placeholder="username" v-model="form.username"/>
    <br/>
    <br/>
    <label for="">Password</label>&nbsp;&nbsp;
    <input type="password" name="" id="" placeholder="password"  v-model="form.password"/>
    <br/>
    <button v-on:click="login">Sign Up</button>


</form>
<p>{{ form }}</p>
</template>
<script>
    export default {
    name: "form-com",
    data(){
        return {
            form:{
                username: "",
                password: "",
            },
        };
    },
    
    methods:{
        login(){
            // console.log("login data", this.form);
            console.table("login data", this.form);
        },
    },
    };
</script>
<style>
    h1 {
    font-weight: 700;
    color: red;
    }
</style>