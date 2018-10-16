<template>
    <div class="home">
        <p>Welcome to Contacty. To get started, use the sidebar on the left to view existing contacts. You can also
            add a new contact.</p>
        <p>Enjoy.</p>
        <router-link :to="{'name': 'add-contact'}" tag="el-button">
            Add Contact
        </router-link>
    </div>
</template>

<style lang="stylus">
.home
    margin 20px
</style>

<script>
    import ContactQuery from "../components/ContactQuery"

    export default {
        name: 'home',
        components: {
            ContactQuery,
        }
    }
</script>
