<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import FooterComponent from './components/FooterComponent.vue';
import { is_authenticated } from './utils'
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router';
import { userStore } from './stores/UserStore'

const classes = ref("")
const router = useRouter()

router.beforeEach(to => {
    if(to.path != '/login'){
        classes.value = "p-4 sm:ml-64"
    }
})

onBeforeMount(()=>{
    const publicPages = ['/login']
    const url = '/' + window.location.href.split('/').pop()
    const authRequired = !publicPages.includes(url)
    const is_auth = is_authenticated()
    if(authRequired && !is_auth){
        router.push('/login')
    }

    // init the user store
    const uStore = userStore()
    uStore.init()
})

function showMenubars(){
    const url = window.location.href.split('/').pop()
    console.log(url != 'login')
    return url != 'login'
}

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
