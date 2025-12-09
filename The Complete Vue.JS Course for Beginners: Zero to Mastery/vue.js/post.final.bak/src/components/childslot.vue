<template>
    <h1>Slots</h1>
    <!-- <slot></slot> -->
     <!-- <h1>{{ data }}</h1> -->
      <!-- <slot></slot> -->
      <!-- <slot><h1>data</h1></slot>
      <slot><h1>data</h1></slot> -->
<div id="price-card">
      <header><slot name="header"></slot></header>
      <section><slot name="section"></slot></section>
      <main><slot name="main"></slot></main>
      <footer><slot name="footer"></slot></footer>
 </div>

</template>
    <script>
    export default {
    name: "childslot - com", 
    // props: {
    //     data: String,
    // },
    };
    </script>
<style>
#price-card {
    width: 400px;
    padding: 22px;
    text-align: center;
    border: 1px solid green;
    background-color: blanchedalmond;
}
</style>