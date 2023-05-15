<script setup>
  import { useRoute } from 'vue-router';
  import { userStore } from './../../stores/UserStore'
  import axios from "axios";
  import { ref, onMounted, onBeforeMount } from "vue";
  import { initDrawers, initFlowbite } from 'flowbite'
  import { acl } from '../../router/acl';


const router = useRoute(); 

const thread_id = router.params.threat_id
const user_id = router.params.user_id
const username = router.params.username
const userRef = ref({user: null, isAdmin: false})
const chat = ref([]);
const skeletonCnt = ref(5);
const isSuccess = ref("")
const isError = ref("")
let is_valid = ref(false)

const input = ref("")

const uStore = userStore()

onBeforeMount( async () => {
    uStore.init() 

    const test = await acl()
    userRef.value = test
    userRef.value.user = test
    userRef.value.isAdmin = test.roles == "Role_admin"
})

const getChatByThread = () => {
  axios
    .get(`/message/chat/${thread_id}/${user_id}`)
    .then((response) => {
      chat.value = response.data;
      skeletonCnt.value = 0;
      isSuccess.value = true

      chat.value.map(chat => {
        chat.timestamp =  new Date(chat.timestamp * 1000).toUTCString()

        return chat
      })
    })
    .then(() => {
      initFlowbite()

      document.getElementById("end").scrollIntoView()
    })
    .catch(err => {
      if (err.response) {
        isSuccess.value = false
        let status = err.response.status
        if (status) {
          if (status == 403) {
            console.log(err.response.status);
            router.push('/error/403')
          }
          else if (status == 401) {
            router.push('/login')
          }
        }

      }
      skeletonCnt.value = 0;
    })
};

const handlerSubmit = (e) => {
  const data = {
    user_id: user_id,
    thread_id: thread_id,
    message: e.target["message"].value,
    message_id: 1,
    timestamp: 325465,
    role: uStore.user.roles
  }

  axios
    .post("/chat/send", data)
    .then((res) => {
      getChatByThread()
      input.value = ""
    })
    .catch((err) => {
      console.log("this error", err);
    })
}

onMounted(() => {
})

getChatByThread()

</script>

<template>
    <div class="mx-auto">
      <div class="border m-auto rounded dark:border-gray-600">
        <div class="">
          <div class="w-full ">
            <div class="relative flex items-center p-3 border-b border-gray-300 dark:border-gray-600">
              <svg class="object-cover w-10 h-10 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155"></path>
              </svg>
              <span class="block ml-2 font-bold text-gray-600 dark:text-gray-300">{{ uStore.user.username }}</span>
              <span class="absolute w-3 h-3 bg-green-600 rounded-full left-10 top-3">
              </span>
            </div>
            <div class="relative w-full p-6 overflow-y-auto xl:h-[45rem]">
              <ul class="space-y-2">
                 <div role="status" class="animate-pulse" v-if="!isSuccess">
                      <div class="" v-for="p=0 in 10" :key="p">
                          <div class="flex items-center">
                            <svg class="w-10 h-32 mr-2 text-gray-200 dark:text-gray-700" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clip-rule="evenodd"></path></svg>
                            <div class="w-1/3 h-8 bg-gray-200 rounded-lg dark:bg-gray-700 mr-3"></div>
                          </div>
                          <div class="w-32 h-3 bg-gray-200 ml-16 rounded-lg dark:bg-gray-700 -mt-6"></div>
                          <div class="float-right m-auto w-1/3">
                            <div class="h-8 bg-gray-200 rounded-lg dark:bg-gray-700 "></div>
                            <div class="w-24 h-3 bg-gray-200 rounded-lg dark:bg-gray-700 mt-5 -mr-5"></div>
                          </div>
                      </div>
                  </div>
                <div class="messages flex-1 overflow-auto" v-if="isSuccess">
                    <div v-for="item in chat" :key="item.message_id">
                        <div class="message mb-4 flex" v-if="item.user_type != 'V'">
                            <div class="flex-2">
                                <div class="w-12 h-12 relative">
                                  <svg class="object-cover w-10 h-10 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                  </svg>
                                  
                                </div>
                            </div>
                            <div class="flex-1 px-2 max-w-2xl">
                                <div class="inline-block bg-gray-300 dark:bg-gray-400 rounded-lg p-2 px-6 text-gray-700">
                                    <span>{{ item.message }}</span>
                                </div>
                                <div class="pl-4"><small class="text-gray-500 text-[10px]"><span class="font-semibold">{{ item.cscart_users.lastname }} {{ item.cscart_users.firstname }}</span> {{item.timestamp}} </small></div>
                            </div>
                        </div>
                        <div class="message me mb-4 flex text-right " v-if="item.user_type == 'V'">
                            <div class="flex-1 px-2 ">
                                <div class="inline-block max-w-3xl text-left bg-sky-800 rounded-lg p-2 px-6 text-white">
                                    <span>{{ item.message }}</span>
                                </div>
                                <div class="pr-4"><small class="text-gray-500 text-[10px]"><span class="font-semibold"> {{ item.cscart_users.lastname }} {{ item.cscart_users.firstname }}</span> {{item.timestamp}}</small></div>
                            </div>
                        </div>
                    </div>
                    <div id="end"></div>
                </div>
              </ul>
            </div>
            <form @submit.prevent="handlerSubmit($event)" class="flex items-center justify-between w-full p-3 border-t border-gray-300 dark:border-gray-600">
              <button>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-500" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </button>
              <button>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
              </button>

              <input type="text" placeholder="Message"
                class="block w-full py-2 pl-4 mx-3 bg-gray-100 dark:bg-gray-400 rounded-full outline-none focus:text-gray-700"
                name="message" 
                v-model="input"
                required />
              <button @click="handlerSubmit">
                <svg class="w-8 h-8 text-gray-500 origin-center transform rotate-90" xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<style>

</style>