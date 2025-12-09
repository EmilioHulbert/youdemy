<template>
  <h1>Email {{ email  }}</h1>
  <h1>Number {{ mobile == 445 }}</h1>
  <h1>Name {{ getName1("werestwet")  }}</h1>
  </template>
  <script>
  export default {
  name: "PAGES",
  data(){
    return {
   email: "abc@gmail.com",
   mobile: "445",
   getName1:function (a){
    return a;
   },
  };
  },
  };
  </script>
  <style scoped>
  h1 {
  color: red;
  }
  </style>
  T