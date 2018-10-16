<template>
    <div class="contact-query">
        <div class="search-box">
            <div>
                <el-button-group>
                    <el-button @click="refresh" icon="el-icon-refresh">Refresh</el-button>
                    <el-button @click="addContact" icon="el-icon-circle-plus">Add Contact</el-button>
                </el-button-group>
            </div>
            <div>
                <el-input placeholder="Search" v-model="query"></el-input>
            </div>
        </div>
        <div class="search-results" v-loading="(callInProgress || callPending)">
            <router-link :to="{name: 'view-contact', params: {contactId: contact.id}}" tag="div"
                         v-for="contact in results" class="contact-row">
                {{contact.last_name}}, {{contact.first_name}}
            </router-link>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import eventBus from '@/bus.js'
    import ld from 'lodash'

    export default {
        name: "contact-query",
        data() {
            return {
                query: '',
                results: [],

                callPending: false,
                callInProgress: false
            }
        },

        created() {
            this.triggerFresh()

            eventBus.$on('refresh-contacts', this.triggerFresh)
        },

        watch: {
            query: function() {
                this.triggerFresh()
            }
        },

        methods: {
            triggerFresh() {
                this.callPending = true
                this.refresh()
            },

            refresh: ld.throttle(function() {
                if (this.callInProgress) {
                    return
                }

                this.callInProgress = true
                this.callPending = false

                let promise = null
                if (this.query)
                    promise = axios.get(`/api/contact`, {params: {'q': this.query}})
                else
                    promise = axios.get(`/api/contact`)

                promise = promise.then(response => {
                    this.results = response.data.contacts
                    this.callInProgress = false
                }).catch((error) => {
                    this.callInProgress = false
                    console.log('Error fetching contacts', error)
                    this.$alert('Error loading contacts. Check console for details', 'Error', {
                        confirmButtonText: 'Reload window',
                        callback: action => {
                            location.reload()
                        }
                    })
                })
            }, 2000),

            addContact() {
                this.$router.push({name: 'add-contact'})
            }
        }

    }
</script>

<style scoped lang="stylus">
    .contact-query
        height 100vh
        display flex
        flex-direction column
        .search-results
            flex 1

    .contact-row
        border-bottom solid 1px silver
        padding 5px
        cursor pointer

    .contact-row:hover
        background-color #d1d1d1
</style>