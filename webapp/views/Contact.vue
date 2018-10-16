<template>
    <div class="contact" v-if="contact">
        <el-card>
            <div slot="header">
                <span>{{contact.last_name}}, {{contact.first_name}}</span>
            </div>
            <dl>
                <dt>First Name</dt>
                <dd>{{contact.first_name}}</dd>

                <dt>Last Name</dt>
                <dd>{{contact.last_name}}</dd>

                <dt>Date of Birth</dt>
                <dd>{{contact.date_of_birth}}</dd>

                <dt>Email Address(es)</dt>
                <dd>
                    <ul>
                        <li v-for="email in contact.email_addresses"><a :href="`mailto:${email}`">{{email}}</a></li>
                    </ul>
                </dd>
                <dt>Phone Numbers</dt>
                <dd>
                    <ul>
                        <li v-for="phone in contact.phone_numbers"><a :href="`tel:${phone}`">{{phone}}</a></li>
                    </ul>
                </dd>
                <dt>Postal Addresses</dt>
                <dd>
                    <ul>
                        <li v-for="addr in contact.addresses">
                            <pre>{{addr}}</pre>
                        </li>
                    </ul>
                </dd>
            </dl>
            <el-button type="primary" @click="editContact = true">Edit Contact</el-button>
            <el-button type="danger" @click="deleteContact">Delete Contact</el-button>
        </el-card>
        <el-dialog

                title="Contact Editor"
                :show-close="true"
                :visible.sync="editContact">

            <contact-editor @contact-saved="saveContact" :contact="contact"></contact-editor>

            <span slot="footer" class="dialog-footer">
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import axios from 'axios'
    import ContactEditor from "../components/ContactEditor"

    import eventBus from '@/bus.js'

    export default {
        name: "contact-view",
        components: {ContactEditor},
        data: function () {
            return {
                contact: null,

                editContact: false
            }
        },

        computed: {
            contactId: function () {
                return this.$route.params.contactId
            }
        },

        mounted() {
            this.fetchContact()
        },

        watch: {
            contactId() {
                this.fetchContact()
            }
        },


        methods: {
            fetchContact() {
                this.contact = null

                const loading = this.$loading({
                    lock: true,
                    text: 'Loading Contact...',
                    spinner: 'el-icon-loading',
                })

                let promise = axios.get(`/api/contact/${this.contactId}`)

                promise = promise.then(response => {
                    this.contact = response.data
                    loading.close()
                }).catch((error) => {
                    loading.close()
                    console.log('Error fetching contact information', error)
                    this.$alert('Error loading contact. Check console for details', 'Error', {
                        confirmButtonText: 'Reload window',
                        callback: action => {
                            location.reload()
                        }
                    })
                })
            },

            saveContact(updatedContact) {
                const loading = this.$loading({
                    lock: true,
                    text: 'Saving Contact...',
                    spinner: 'el-icon-loading',
                })

                let promise = axios.post(`/api/contact/${this.contactId}`, updatedContact)

                promise = promise.then(response => {
                    this.contact = response.data
                    loading.close()
                    this.editContact = false

                    this.$notify({
                        title: 'Updated',
                        message: 'Contact information updated',
                        type: 'success'
                    })

                    eventBus.$emit('refresh-contacts')
                }).catch((error) => {
                    loading.close()
                    if (error.response.data.description) {
                        this.$notify({
                            title: 'Contact did not validate',
                            message: error.response.data.description,
                            type: 'warning'
                        })
                    } else {
                        console.log('Error saving contact', error)
                        this.$alert('Error saving contact. Check console for details', 'Error', {
                            confirmButtonText: 'Reload window',
                            callback: action => {
                                location.reload()
                            }
                        })
                    }

                })
            },

            deleteContact() {
                this.$confirm('Really delete this contact?', 'Warning', {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }).then(() => {
                    let promise = axios.delete(`/api/contact/${this.contactId}`)

                    promise = promise.then(response => {
                        this.$notify({
                            title: 'Deletion Successful',
                            message: 'Contact has been deleted',
                            type: 'success'
                        })

                        this.$router.push({'name': 'home'})

                        eventBus.$emit('refresh-contacts')
                    }).catch((error) => {
                        this.editContact = false
                        loading.close()
                        console.log('Error saving contact', error)
                        this.$alert('Error saving contact. Check console for details', 'Error', {
                            confirmButtonText: 'Reload window',
                            callback: action => {
                                location.reload()
                            }
                        })
                    })
                }).catch(() => {
                    return null
                });
            }
        }
    }
</script>

<style scoped lang="stylus">

</style>