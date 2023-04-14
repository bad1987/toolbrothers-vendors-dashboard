<script setup>
    import { defineProps, defineEmits, ref } from 'vue'
    import CheckboxGroup from './CheckboxGroup.vue';
    import Field from '../../helpers/field'


    const props = defineProps({
        fields: Field
    })
</script>

<template>
    <form action="#" id="add-user-form">
        <div class="grid grid-cols-6 gap-6">
            <div class="col-span-6 sm:col-span-3">
                <label for="username"
                    class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">User Name</label>
                <input v-model="newUser.username" type="text" name="username" id="username"
                    class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Bonnie" required="">
            </div>
            <div class="col-span-6 sm:col-span-3">
                <label for="email"
                    class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email</label>
                <input v-model="newUser.email" type="email" name="email" id="email"
                    class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="example@company.com" required="">
            </div>
            <div class="col-span-6 sm:col-span-3">
                <label for="role" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select a role</label>
                <select v-model="newUser.roles" @change="changeRole" id="role" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                    <option value="" selected>Select a role</option>
                    <option value="Role_affiliate">Affiliate</option>
                    <option value="Role_direct_sale">Direct sale</option>
                </select>
            </div>
            <div class="col-span-6 sm:col-span-3 flex items-center">
                <input v-model="newUser.status" id="checkbox-activate-create" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <label for="checkbox-activate-create" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Activate</label>
            </div>
            <div class="col-span-6">
                <h4 class="font-bold dark:text-white">Set permissions</h4>
                <div class="permissions-list grid grid-cols-2 gap-4">
                    <CheckboxGroup :items="permissions" name="permission" id="checkbox-group-perm" @toggle-value="togglePermissionValue"/>
                </div>
            </div>
        </div>
    </form>
</template>