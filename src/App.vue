<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import FooterComponent from './components/FooterComponent.vue';
import { refresh_token } from './utils'
import { onBeforeMount, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { userStore } from './stores/UserStore'


const classes = ref("")
const refreshIntervalID = ref(0)
const router = useRouter()


const uStore = userStore()


// define a function that toggles the hidden class based on the route
const toggleHiddenClass = (path="") => {
    // get the Navbar and Sidebar elements by id
    const navbar = document.getElementById('navbar')
    const sidebar = document.getElementById('logo-sidebar')
    // const routeName = router.currentRoute.value.name
    const routeName = window.location.href
    if(!path) {
        path = routeName
    }
    // if the route is login, add the hidden class
    if (path.includes('login')) {
        navbar.classList.add('hidden')
        sidebar.classList.add('hidden')
    } else {
        // otherwise, remove the hidden class
        navbar.classList.remove('hidden')
        sidebar.classList.remove('hidden')
    }
}

router.beforeEach(to => {
    toggleHiddenClass(to.path)

    if(!to.meta.hideNavigation){
        classes.value = "p-4 sm:ml-64"
    }
})

onBeforeMount(async ()=>{
 
    // init the user store
    uStore.init()

    // refresh token after each 5 minutes
    refreshIntervalID.value = setInterval(() => {
        refresh_token() 
    }, 300000);
})

onUnmounted(()=>{
    clearInterval(refreshIntervalID.value)
})

</script>

<template>
    <!-- <div v-if="!$route.meta.hideNavigation">
    </div> -->
    <Navbar class="hidden"/>
    <Sidebar  class="hidden"/>
    <div :class="classes" >
        <div class="rounded-lg dark:border-gray-700 mt-14">
            <RouterView/>
            <FooterComponent/>
        </div>
    </div>
</template>

<style scoped>
.hidden {
    display: none;
}
</style>
