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
    <br/>
    <label for="">Hobbies</label>&nbsp;&nbsp;
    <input type="checkbox" value="Hockey"   v-model="form.hobbies"/>
    <label for="">Hockey</label>&nbsp;&nbsp;
    <input type="checkbox" value="cricket"  v-model="form.hobbies"/>
    <label for="">Cricket</label>&nbsp;&nbsp;
    <input type="checkbox" value="football"  v-model="form.hobbies"/>
    <label for="">Football</label>&nbsp;&nbsp;


    <br/>
    <br/>
    <label for="">Gender</label>&nbsp;&nbsp;
    <input type="radio" value="male"   v-model="form.gender" name="gender"/>
    <label for="">Male</label>&nbsp;&nbsp;
    <input type="radio" value="female"  v-model="form.gender" name="gender"/>
    <label for="">Female</label>&nbsp;&nbsp;
    <br/>
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
                hobbies: [],
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