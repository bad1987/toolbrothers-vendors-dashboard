<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import FooterComponent from './components/FooterComponent.vue';
import { is_authenticated, refresh_token } from './utils'
import { onBeforeMount, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { userStore } from './stores/UserStore'
import { getUser } from './api';


const classes = ref("")
const refreshIntervalID = ref(0)
const router = useRouter()


const uStore = userStore()

router.beforeEach(to => {
    if(to.meta.hideNavigation){
        classes.value = "p-4 sm:ml-64"
    }
})



onBeforeMount(async ()=>{

    const publicPages = ['/login']
    const url = '/' + window.location.href.split('/').pop()
    const authRequired = !publicPages.includes(url)
    const is_auth = is_authenticated()
    console.log("is authencate user", is_auth);
    if(authRequired && !is_auth){
        router.push('/login')
    }
 
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
    <Navbar v-if="!$route.meta.hideNavigation"/>
    <Sidebar v-if="!$route.meta.hideNavigation"/>
    <div :class="classes" >
        <div class="rounded-lg dark:border-gray-700 mt-14">
            <RouterView/>
            <FooterComponent/>
        </div>
    </div>
</template>

<style scoped>
</style>
