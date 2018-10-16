<template>
    <div id="app">
        <nav>
            <router-link :to="{name: 'home'}">Contactie</router-link>
        </nav>
        <div id="app-main">
            <div id="sidebar">
                <contact-query></contact-query>
            </div>
            <div id="content">
                <router-view/>
            </div>
        </div>
        <footer>
            Follow us on Google+, it's the future!
        </footer>
    </div>
</template>
<style lang="stylus">
    body, html
        margin 0
        padding 0
    #app
        height 100vh
        display flex
        flex-direction column
    #app-main
        flex: 1
        display flex
        #sidebar
            width 300px
            background #efefef
        #content
            flex 1
    nav, footer
        background #333333
        color white
        padding 20px
    nav
        font-size 200%
        a:link, a:active, a:visited
            color white
            text-decoration none
    footer
        text-align right
</style>
<script>
    import ContactQuery from "./components/ContactQuery"
    export default {
        components: {ContactQuery}
    }
</script>