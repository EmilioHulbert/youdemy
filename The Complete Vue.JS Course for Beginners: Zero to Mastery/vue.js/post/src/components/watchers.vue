 <template>
    <h1>Watchers</h1>
    <h2>{{ counter }}</h2>
    <button v-on:click="counter = counter + 1">+</button>
    <button v-on:click="counter = counter - 1">-</button>
    <!-- <Childslot data="Meta"/> -->
<Childslot> 
    <h1>MetaBrains.org</h1> 
    <button>Click Here</button>
    <a href="#">Youtube.com</a>
    <img src="https://images.pexels.com/photos/674010/pexels-photo-674010.jpeg?cs=srgb&dl-pexels-anjana-c-674010.jpg&fm=jpg" width="200" alt="" />
</Childslot>

<!-- 
<Childslot> 
    <a href="#">Youtube.com</a>
</Childslot>


<Childslot> 
    <img src="https://images.pexels.com/photos/674010/pexels-photo-674010.jpeg?cs=srgb&dl-pexels-anjana-c-674010.jpg&fm=jpg" width="200" alt="" />
</Childslot>
 -->

</template>

    <script>
    import Childslot from "./childslot.vue"
    export default {
    name: "Watchers - com", 
    data() {
    return {
    counter: 0,
    };
    },
    watch: {
        counter (num, last){
            if (num > 10 && num > last){
                alert("Maximum number is 10");
                this.counter = 0
            }
        },
    },
    components: { Childslot },
    };

    </script>