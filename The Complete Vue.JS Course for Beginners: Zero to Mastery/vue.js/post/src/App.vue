


<!-- <template>
  
  <img alt="Vue logo" src="./assets/logo.png" width="200" />
  <h1>App.vue</h1>
   
  
  <RouterLink to="/" >Home</RouterLink> <br/>
   <RouterLink to="/login/stark" >login1</RouterLink><br/>
   <RouterLink to="/login/stark2" >login2</RouterLink><br/>
   <RouterLink to="/login/stark3" >login3</RouterLink><br/>
   <RouterLink to="/login/stark4" >login4</RouterLink><br/>


   <RouterLink to="/signup/user2" >signup</RouterLink><br/>
   <RouterView></RouterView>

  </template> -->
  <!-- <script>
  
  export default {
  name: "App",
  components: {
   
  },
  };
  </script> -->








  <!-- <template>
    <img alt="Vue logo" src="./assets/logo.png" width="200" />
    <h1>Call API's</h1>
  
    <table>
      <tr>
        <th>ID</th>
        <th>First-Name</th>
        <th>Last-Name</th>
        <th>Email</th>
        <th>Picture</th>
      </tr>
  
      <tr v-for="item in info" :key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.username }}</td>
        <td>{{ item.email }}</td>
        <td><img :src="item.avatar" alt="" /></td>
      </tr>
    </table>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "App",
    data() {
      return {
        info: [],
      };
    },
    async mounted() {
      const res = await axios.get("https://reqres.in/api/users?page=2");
      const res = await axios.get("https://jsonplaceholder.typicode.com/users");

      this.info = res.data.data;
      this.info = res.data

    },
  };
  </script>
  
  <style>
  table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
  }
  
  td,
  th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
  }
  
  tr:nth-child(even) {
    background-color: #dddddd;
  }
  </style>
   -->


   <template>
    <img alt="Vue logo" src="./assets/logo.png" width="200" />
    <h1>Call API's</h1>
  
    <table>
      <tr>
        <th>ID</th>
        <th>First-Name</th>
        <th>Last-Name</th>
        <th>Email</th>
        <th>Picture</th>
      </tr>
  
      <tr v-for="item in info" :key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.firstName }}</td>
        <td>{{ item.lastName }}</td>
        <td>{{ item.email }}</td>
        <td>
          <img :src="item.avatar" alt="" />
        </td>
      </tr>
    </table>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "App",
  
    data() {
      return {
        info: [],
      };
    },
  
    async mounted() {
      const res = await axios.get("https://jsonplaceholder.typicode.com/users");
  
      // Transform jsonplaceholder data to match your table fields
      this.info = res.data.map((user) => ({
        id: user.id,
        firstName: user.name.split(" ")[0],      // extract first name
        lastName: user.name.split(" ").slice(1).join(" "), // rest becomes last name
        email: user.email,
        avatar: `https://i.pravatar.cc/150?u=${user.id}`,  // generate fake avatar
      }));
    },
  };
  </script>
  
  <style>
  table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
  }
  
  td,
  th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
  }
  
  tr:nth-child(even) {
    background-color: #dddddd;
  }
  </style>
  

  <!-- <template>

  </template>
  
  <script>
  export default{
    name: "App",
  };
  
  </script>
  
   -->
  