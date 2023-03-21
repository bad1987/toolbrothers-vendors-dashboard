<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import FooterComponent from './components/FooterComponent.vue';

</script>

<template>
    <Navbar></Navbar>
    <div class="dark:bg-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:border-gray-700">
        <div class="flex overflow-hidden bg-white pt-16 dark:bg-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:border-gray-700">
            <Sidebar></Sidebar>
            <div class="bg-gray-900 opacity-50 hidden fixed inset-0 z-10 dark:bg-gray-800 dark:border-gray-700" id="sidebarBackdrop"></div>
            <div id="main-content" class="h-full w-full bg-gray-50 relative overflow-y-auto lg:ml-64 dark:bg-gray-800 dark:border-gray-700">
                <div class="main-section min-h-screen dark:bg-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:border-gray-700">
                    <RouterView></RouterView>
                </div>
                <FooterComponent></FooterComponent>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>
