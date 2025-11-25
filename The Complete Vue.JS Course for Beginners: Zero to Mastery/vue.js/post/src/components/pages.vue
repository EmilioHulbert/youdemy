<template>
  <h1 id="pages">Two Way Binding</h1>
  <input type="text" placeholder=" Add The NUmber" v-model="count" />
  <h3>{{ count }}</h3>
</template>

<script>
export default {
  name: "PagesOne",
  data() {
    return {
      count: 0,
    };
  },
};
</script>
<style>
h1 {
    color: red;
}
</style>