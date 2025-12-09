<template>
    <h1>Simple Form</h1>
<!-- <form action=""> -->
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
    <!-- <button type="button" @click="login">Sign Up</button> -->

<!-- </form> -->
<!-- <p>{{ form }}</p> -->
 <ul>
    <li v-for="item in fun" v-bind:key="item">
        {{ item }} Not Submitted
    </li>
 </ul>
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
                gender: [],
            },
            fun: [],
        };
    },
    
    methods:{
        login(){
            this.fun = [];
            // console.log("login data", this.form);
            for(const item in this.form){
                if(this.form[item] === "" || this.form[item].length === 0){
                    this.fun.push(item);
                }
            }
            // console.table("login data", this.form);
            if(this.fun.length ===0 ){
                alert("Information has been submitted")
            }
            // console.log(this.form, this.fun);
            console.table(this.form, this.fun);
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
