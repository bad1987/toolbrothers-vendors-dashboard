<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import FooterComponent from './components/FooterComponent.vue';

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
