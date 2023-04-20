<script setup>
  import { useRoute } from 'vue-router';
  import axios from "axios";
  import { ref, onMounted, onBeforeMount } from "vue";
  import { initDrawers, initFlowbite } from 'flowbite'
  import { acl } from '../../router/acl';


const router = useRoute(); 

const thread_id = router.params.threat_id
const user_id = router.params.user_id
const username = router.params.username
const userRef = ref({user: null, isAdmin: false})

onBeforeMount( async () => {

    const test = await acl()
    userRef.value = test
    userRef.value.user = test
    userRef.value.isAdmin = test.roles == "Role_admin"
    console.log("get user information from acl", userRef.value.email );
})

const chat = ref([]);
const skeletonCnt = ref(5);
const isSuccess = ref("")
const isError = ref("")
let is_valid = ref(false)

const getChatByThread = () => {
  axios
    .get(`/message/chat/${thread_id}/${user_id}`)
    .then((response) => {
      chat.value = response.data;
      skeletonCnt.value = 0;

      console.log(chat.value);
      isSuccess.value = true
    })
    .then(() => {
      initFlowbite()
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

getChatByThread()

</script>

<template>
    
    <div class="mx-auto">
      <div class="border m-auto rounded dark:border-gray-600">
        <div class="">
          <div class="w-full ">
            <div class="relative flex items-center p-3 border-b border-gray-300 dark:border-gray-600">
              <img class="object-cover w-10 h-10 rounded-full"
                src="https://cdn.pixabay.com/photo/2018/01/15/07/51/woman-3083383__340.jpg" alt="username" />
              <span class="block ml-2 font-bold text-gray-600 dark:text-gray-300">{{ username }}</span>
              <span class="absolute w-3 h-3 bg-green-600 rounded-full left-10 top-3">
              </span>
            </div>
            <div class="relative w-full p-6 overflow-y-auto h-[48rem]">
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
                                    <img class="w-12 h-12 rounded-full mx-auto" src="https://cdn.pixabay.com/photo/2018/01/15/07/51/woman-3083383__340.jpg" alt="chat-user" />
                                    <span class="absolute w-4 h-4 bg-gray-400 rounded-full right-0 bottom-0 border-2 border-white"></span>
                                </div>
                            </div>
                            <div class="flex-1 px-2">
                                <div class="inline-block bg-gray-300 dark:bg-gray-400 rounded-lg p-2 px-6 text-gray-700 md:w-2/3">
                                    <span>{{ item.message }} {{ item.message }}</span>
                                </div>
                                <div class="pl-4"><small class="text-gray-500">15 April</small></div>
                            </div>
                        </div>
                        <div class="message me mb-4 flex text-right" v-if="item.user_type == 'V' ">
                            <div class="flex-1 px-2">
                                <div class="inline-block bg-sky-800 rounded-lg p-2 px-6 text-white md:w-2/3">
                                    <span>{{ item.message }}</span>
                                </div>
                                <div class="pr-4"><small class="text-gray-500">15 April</small></div>
                            </div>
                        </div>
                    </div>
                </div>
              </ul>
            </div>

            <div class="flex items-center justify-between w-full p-3 border-t border-gray-300 dark:border-gray-600">
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
                name="message" required />
              <button>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </button>
              <button type="submit">
                <svg class="w-5 h-5 text-gray-500 origin-center transform rotate-90" xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<style>

</style>