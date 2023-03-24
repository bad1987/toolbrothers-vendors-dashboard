<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import FooterComponent from './components/FooterComponent.vue';
import { is_authenticated } from './utils'
import { onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';

onBeforeMount(()=>{
    const router = useRouter()
    const publicPages = ['/login']
    const url = '/' + window.location.href.split('/').pop()
    const authRequired = !publicPages.includes(url)
    const is_auth = is_authenticated()
    if(authRequired && !is_auth){
        router.push('/login')
    }
})
</script>

<template>
    <Navbar/>
    <Sidebar/>
    <div class="p-4 sm:ml-64">
        <div class="rounded-lg dark:border-gray-700 mt-14">
            <RouterView/>
            <FooterComponent/>
        </div>
    </div>
</template>

<style scoped>
</style>
