<script setup>
    import { ref, onBeforeMount } from 'vue';
    import axios from 'axios'
    

    const credentials = ref({
        email: "",
    })
    const _state = ref({
        error: "",
        show: false,
        loading: false
    })
    const url = axios.defaults.baseURL + "forgot-password"
    
    // redirect the user from where he came from if he is authenticated
    onBeforeMount(()=>{
    })

    function handleSubmit(e) {
        const data = {
            ...credentials.value
        }

        _state.value.show = false
        _state.value.error = ""
        _state.value.loading = true
        axios.post(
            url,
            {
                ...data,
            }
        )
        .then(response=> {

        })
        .catch(err => {
            console.log(err)
            _state.value.show = true
            if(err.response.data){
                console.log(err.response.data);
                _state.value.error = err.response.data
            }
            else{
                _state.value.error = "Unknown error"
            }
        })
        .finally(() => {
            _state.value.loading = false
        })
    }
</script>

<template>
    <div class="flex flex-col items-center justify-center px-6 pt-8 mx-auto md:h-screen pt:mt-0 dark:bg-gray-900">
    <div class="w-full max-w-xl p-6 space-y-8 sm:p-8 bg-white rounded-lg shadow dark:bg-gray-800">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Forgot password
        </h2>
        
        <div v-if="_state.show" class="max-w-lg mx-auto items-center justify-center justify-items-center m-auto mt-10">
            <div class="flex bg-red-100 rounded-lg p-4 mb-4 text-sm text-red-700" role="alert">
                <svg class="w-5 h-5 inline mr-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                <div>
                    <p>
                        <p class="">{{ _state.error }}</p>
                    </p>
                </div>
            </div>
        </div>
        <form class="mt-8 space-y-6" @submit.stop.prevent="handleSubmit">
            <div>
                <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
                <input type="email" name="email" v-model="credentials.email" required class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="bad@company.com" >
            </div>
            <button class="w-full text-white bg-gray-500 hover:bg-gray-500 focus:ring-4 focus:outline-none focus:ring-gray-500font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                <svg v-if="_state.loading" aria-hidden="true" role="status" class="inline w-4 h-4 mr-3 text-gray-200 animate-spin dark:text-gray-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="#1C64F2"/>
                </svg>
                Send e-mail
            </button>
        </form>
    </div>
</div>
</template>


<style lang="scss" scoped>

</style>