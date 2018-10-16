<template>
    <div>
        <el-form ref="contactForm" :model="contactForm" :rules="contactFormRules"
                 @submit.native.prevent="contactFormSubmit">
            <el-card>
                <div slot="header">
                    <span>Basic Contact Info</span>
                </div>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="First Name" prop="first_name">
                            <el-input v-model="contactForm.first_name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Last Name" prop="last_name">
                            <el-input v-model="contactForm.last_name"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="Date of Birth" prop="date_of_birth">
                    <el-date-picker v-model="contactForm.date_of_birth"></el-date-picker>
                </el-form-item>
            </el-card>
            <br>

            <el-card>
                <div slot="header">
                    <span>Postal Addresses</span>
                </div>

                <el-form-item
                        v-for="address, index in contactForm.addresses"
                        label=""
                        :key="index">
                    <el-input :rows="4" :value="address" type="textarea" @change="setAddress(index, $event)"
                              :placeholder="'123 Fake St\nDenver, CO\n80305\nUSA'">
                    </el-input>
                    <el-button @click.prevent="removeAddress(index)" icon="el-icon-delete">Remove Address</el-button>
                </el-form-item>
                <el-button @click="addAddress">Add Postal Address</el-button>
            </el-card>
            <br>
            <el-row :gutter="24">
                <el-col :span="12">
                    <el-card>
                        <div slot="header">
                            <span>Phone Numbers</span>
                        </div>
                        <el-form-item
                                v-for="phone, index in contactForm.phone_numbers"
                                label=""
                                :key="index">
                            <el-input :value="phone" type="tel" @change="setPhoneNumber(index, $event)"
                                      placeholder="555-123-4567">
                                <el-button @click.prevent="removePhoneNumber(index)" slot="append"
                                           icon="el-icon-delete"></el-button>
                            </el-input>
                        </el-form-item>
                        <el-button @click="addPhoneNumber">Add Phone Number</el-button>
                    </el-card>
                </el-col>
                <el-col :span="12">
                    <el-card>
                        <div slot="header">
                            <span>Email Addresses</span>
                        </div>
                        <el-form-item
                                v-for="email, index in contactForm.email_addresses"
                                label=""
                                :key="index">
                            <el-input :value="email" type="email" @change="setEmailAddress(index, $event)"
                                      placeholder="name@example.com">
                                <el-button @click.prevent="removeEmailAddress(index)" slot="append"
                                           icon="el-icon-delete"></el-button>
                            </el-input>
                        </el-form-item>
                        <el-button @click="addEmailAddress">Add Email Address</el-button>
                    </el-card>
                </el-col>
            </el-row>

            <br>
            <el-form-item>
                <el-button type="primary" @click="contactFormSubmit()">Save Contact</el-button>
            </el-form-item>
            <button type="submit" style="display: none;"></button>
        </el-form>
    </div>
</template>

<script>
    export default {
        name: "contact-editor",
        props: ['contact'],
        data: function () {
            return {
                contactForm: {},
                contactFormRules: {
                    first_name: [
                        {required: true, message: 'Please input your first name', trigger: 'blur'},
                    ],
                    last_name: [
                        {required: true, message: 'Please provide your last name', trigger: 'blur'},
                    ],
                    date_of_birth: [
                        {required: true, message: 'Please enter your date of birth', trigger: 'blur'},
                    ]
                }
            }
        },

        mounted() {
            // JavaScript doesn't have a deep copy.
            this.contactForm = JSON.parse(JSON.stringify(this.contact))
        },

        methods: {
            contactFormSubmit() {
                this.$refs['contactForm'].validate((valid) => {
                    if (valid) {
                        // Extra validation
                        if (this.contactForm.email_addresses.length === 0) {
                            this.$notify({
                                title: 'Cannot Save Contact',
                                message: 'You must specify at least one email address.',
                                type: 'error'
                            })
                            return
                        }

                        this.$emit('contact-saved', this.contactForm)
                    }
                })
            },


            //////////////////
            // TODO: DYI
            // ---------
            // This is pretty quick and dirty, but could be factored out into a better repeating list component.

            // Email addresses
            addEmailAddress() {
                this.contactForm.email_addresses.push('')
            },
            removeEmailAddress(index) {
                this.contactForm.email_addresses.splice(index, 1)
            },
            setEmailAddress(index, value) {
                this.$set(this.contactForm.email_addresses, index, value)
            },

            // Phone Numbers
            addPhoneNumber() {
                this.contactForm.phone_numbers.push('')
            },
            removePhoneNumber(index) {
                this.contactForm.phone_numbers.splice(index, 1)
            },
            setPhoneNumber(index, value) {
                this.$set(this.contactForm.phone_numbers, index, value)
            },

            // Addresses
            addAddress() {
                this.contactForm.addresses.push('')
            },
            removeAddress(index) {
                this.contactForm.addresses.splice(index, 1)
            },
            setAddress(index, value) {
                this.$set(this.contactForm.addresses, index, value)
            },

        }
    }
</script>

<style scoped>

</style>