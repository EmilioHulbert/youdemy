<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Meta Brains.org"/>
  <!-- <PAGES /> -->
  <HomeOne />
  <PagesOne />
  <Inputboxes />
  <IfElseCondition/>
  <ForLoop />
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
// import PAGES from './components/New-onef.vue'
import  HomeOne from './components/Home-one.vue'
import  PagesOne from './components/pages.vue'
import  Inputboxes from './components/inputboxes.vue'
import  IfElseCondition from './components/if-else-condition.vue'
import  ForLoop from './components/For-loop.vue'


export default {
  name: 'App',
  components: {
    HelloWorld,
    // PAGES,
    HomeOne,
    PagesOne,
    Inputboxes,
    IfElseCondition,
    ForLoop

  }
}
</script>

<!-- <style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  margin-top: 60px;
}
</style> -->
