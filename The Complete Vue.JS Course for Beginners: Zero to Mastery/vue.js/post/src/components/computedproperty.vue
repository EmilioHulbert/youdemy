<!-- https://vuejs.org/guide/essentials/computed.html#basic-example -->
<template>
    <h1> Computed Property</h1>
    <span>{{ author.books.length > 0 ? "Yes" : "No" }}</span>
    </template>
    <script>
    export default{
    name: "Computed - com",
data() {
return {
author: {
name: "John Doe",
books:
[
"Vue 2 Advanced Guide",
"Vue 3 Basic Guide",
"Vue 4 The Mystery",
],
},
};
},

computed:{
// a computed getter
publishedBooksMessage() {
// this points to the component instance
return this.author.books.length > 0? 'Yes': 'No'
}
}

};
</script>
    I
    

