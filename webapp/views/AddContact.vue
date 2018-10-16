<template>
    <div class="add-contact">
        <h2>Add New Contact</h2>
        <contact-editor @contact-saved="saveContact" :contact="newContact"></contact-editor>
    </div>
</template>

<script>
    import axios from 'axios'

    import ContactEditor from "../components/ContactEditor"
    import eventBus from '@/bus.js'

    export default {
        data: function () {
            return {
                newContact: {
                    first_name: '',
                    last_name: '',
                    date_of_birth: new Date(1970, 1, 1),
                    addresses: [],
                    phone_numbers: [],
                    email_addresses: [],
                }
            }
        },
        components: {ContactEditor},
        methods: {
            saveContact(newContact) {
                let promise = axios.post(`/api/contact/_new`, newContact)
                const loading = this.$loading({
                    lock: true,
                    text: 'Saving Contact',
                    spinner: 'el-icon-loading',
                });

                promise = promise.then(response => {
                    loading.close()
                    this.$notify({
                        title: 'Contact Created',
                        message: 'This contat has been successfully created.',
                        type: 'success'
                    });

                    this.$router.push({name: 'view-contact', params: {contactId: response.data.id}})
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
            }
        }
    }
</script>

<style scoped lang="stylus">
    .add-contact
        margin 50px
</style>