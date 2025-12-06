<template>
<h1>Home</h1>
<button @click="active = 'First'">First</button>
<button @click="active = 'Second'">Second</button>
<button @click="active = 'Third'">Third</button>
<button @click="active = 'watchers'">watcher</button>
<!-- <First />
<Second />
<Third /> -->
<component :is="active" />
</template>
<script>

import First from "./first.vue";
import Second from "./second.vue";
import Third from "./third.vue";
import Watchers from "./watchers.vue";
export default{
    name: "home-com",
    components: {First, Second, Third,Watchers,},
    data(){
        return{
            active: "First",
        };
    },
};

</script>

<style scoped>
h1{
    color: brown;
    font-weight: bold;
}
</style>

