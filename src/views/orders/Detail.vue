<script setup>
    import { useRoute } from 'vue-router';
    import { userStore } from './../../stores/UserStore'
    import axios from "axios";
    import { ref, onBeforeMount, computed } from "vue";
    import { initFlowbite } from 'flowbite'
    import { acl } from '../../router/acl';
    import moment from 'moment'

    const router = useRoute();
    
    const id = router.params.id
    const userRef = ref({user: null, isAdmin: false})
    const order = ref([]);
    const order_detail = ref([])
    const skeletonCnt = ref(5);
    const isSuccess = ref("")

    const uStore = userStore()

    onBeforeMount( async () => {
        uStore.init() 

        const test = await acl()
        userRef.value = test
        userRef.value.user = test
        userRef.value.isAdmin = test.roles == "Role_admin"
    })

    const getDetailOrder = () => {
        
        axios
            .get(`/order/detail/${id}`)
            .then((response) => {
            console.log("eeeeeeeeeeeeeeeeeeee", response.data);
            order.value = response.data['order'];
            order_detail.value = response.data['order_detail']

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

    getDetailOrder()

</script>

<template>
    <div class="py-5 px-4 2xl:container 2xl:mx-auto pb-[5%]">
        <div class="flex justify-start item-start space-y-2 flex-col">
            <h1 class="text-3xl lg:text-4xl font-semibold leading-7 lg:leading-9 text-gray-800 dark:text-gray-300" v-if="order">Order #{{ id }}</h1>
            <p class="text-base dark:text-gray-400 font-medium leading-6 text-gray-600" v-if="order">{{moment(order.timestamp).format("ddd MMM DD, YYYY [at] HH:mm a")}}</p>
        </div>
        <div class="mt-10 flex flex-col xl:flex-row jusitfy-center items-stretch w-full xl:space-x-8 space-y-4 md:space-y-6 xl:space-y-0">
            <div class="flex flex-col justify-start items-start w-full space-y-4 md:space-y-6 xl:space-y-8">
                <div class="flex flex-col justify-start items-start dark:bg-gray-700 rounded-lg bg-gray-50 px-4 py-4 md:py-6 md:p-6 xl:p-8 w-full" v-if="order_detail">
                    <p class="text-lg md:text-xl dark:text-gray-300 font-semibold leading-6 xl:leading-5 text-gray-800">Customer’s Cart</p>
                    <div class="mt-4 md:mt-6 flex flex-col cursor-pointer md:flex-row justify-start items-start md:items-center md:space-x-6 xl:space-x-8 w-full hover:shadow-lg hover:scale-105 duration-300" v-for="u in order_detail" :key="u">
                        <div class="pb-4 md:pb-8 w-full md:w-40">
                            <img class="w-full hidden md:block" src="https://cdn.toolbrothers.com/images/detailed/3880/GKS_18V-70.jpg" alt="dress" />
                            <img class="w-full md:hidden" src="https://cdn.toolbrothers.com/images/detailed/3880/GKS_18V-70.jpg" alt="dress" />
                        </div>
                        <div class="border-b border-gray-200 dark:border-gray-600 md:flex-row flex-col flex justify-between items-start w-full pb-8 space-y-4 md:space-y-0">
                            <div class="w-full flex flex-col justify-start items-start space-y-8">
                                <h3 class="text-lg dark:text-gray-300 font-semibold leading-6 text-gray-800 " > 
                                    {{ u.extra.product }}
                                </h3>
                                <div class="flex justify-start items-start flex-col space-y-2">
                                    <p class="text-sm dark:text-gray-300 leading-none text-gray-800"><span class="dark:text-gray-400 text-gray-300">Product code: </span> #{{ u.product_code }}</p>
                                    <p class="text-sm dark:text-gray-300 leading-none text-gray-800"><span class="dark:text-gray-400 text-gray-300">Product Id: </span> #{{ u.product_id }}</p>
                                </div>
                            </div>
                            <div class="flex justify-between space-x-8 items-start w-full">
                                <p class="text-base dark:text-gray-300 xl:text-lg leading-6 ld:px-16">{{ u.price }} €</p>
                                <p class="text-base dark:text-gray-300 xl:text-lg leading-6 text-gray-800">× {{ u.amount }}</p>
                                <p class="text-base dark:text-gray-300 xl:text-lg font-semibold leading-6 text-gray-800">{{ u.price*u.amount }} €</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex justify-center flex-col md:flex-row items-stretch  w-full space-y-4 md:space-y-0 md:space-x-6 xl:space-x-8">
                    <div class="flex flex-col px-4 py-6 md:p-6 xl:p-8 w-full bg-gray-50 rounded-lg dark:bg-gray-700 space-y-6">
                        <h3 class="text-xl dark:text-gray-300 font-semibold leading-5 text-gray-800">Summary</h3>
                        <div class="flex justify-center items-center w-full space-y-4 flex-col border-gray-200 dark:border-gray-600 border-b pb-4">
                            <div class="flex justify-between w-full">
                            <p class="text-base dark:text-gray-300 leading-4 text-gray-800">Subtotal</p>
                            <p class="text-base dark:text-gray-300 leading-4 text-gray-600" v-if="order">{{ order.subtotal }} €</p>
                            </div>
                            <div class="flex justify-between items-center w-full">
                            <p class="text-base dark:text-gray-300 leading-4 text-gray-800">Discount</p>
                            <p class="text-base dark:text-gray-300 leading-4 text-gray-600">00.00 (00%)</p>
                            </div>
                            <div class="flex justify-between items-center w-full">
                            <p class="text-base dark:text-gray-300 leading-4 text-gray-800">Shipping</p>
                            <p class="text-base dark:text-gray-300 leading-4 text-gray-600" v-if="order">{{ order.shipping_cost }} €</p>
                            </div>
                        </div>
                        <div class="flex justify-between items-center w-full">
                            <p class="text-base dark:text-gray-300 font-semibold leading-4 text-gray-800">Total</p>
                            <p class="text-base dark:text-gray-300 font-semibold leading-4 text-gray-600" v-if="order">{{ order.total }} €</p>
                        </div>
                    </div>
                    <div class="flex rounded-lg flex-col justify-center px-4 py-6 md:p-6 xl:p-8 w-full bg-gray-50 dark:bg-gray-700 space-y-6">
                        <h3 class="text-xl dark:text-gray-300 font-semibold leading-5 text-gray-800">Shipping</h3>
                        <div class="flex justify-between items-start w-full">
                            <div class="flex justify-center items-center space-x-4">
                                <div class="w-8 h-8">
                                    <img class="w-full h-full" alt="logo" src="https://i.ibb.co/L8KSdNQ/image-3.png" />
                                </div>
                                <div class="flex flex-col justify-start items-center">
                                    <p class="text-lg leading-6 dark:text-gray-300 font-semibold text-gray-800">DPD Delivery<br /><span class="font-normal" v-if="order">{{ order.b_address }}</span></p>
                                </div>
                            </div>
                            <p class="text-lg font-semibold leading-6 dark:text-gray-300 text-gray-800" v-if="order">{{ order.shipping_cost }} €</p>
                        </div>
                        <div class="w-full flex justify-center items-center">
                            <button class="hover:bg-black dark:bg-white dark:text-gray-800 dark:hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800 py-5 w-96 md:w-full bg-gray-800 text-base font-medium leading-4 text-white">View Carrier Details</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700 w-full xl:w-96 rounded-lg flex justify-between items-center md:items-start px-4 py-6 md:p-6 xl:p-8 flex-col">
                <h3 class="text-xl dark:text-gray-300 font-semibold leading-5 text-gray-800">Customer</h3>
                <div class="flex flex-col md:flex-row xl:flex-col justify-start items-stretch h-full w-full md:space-x-6 lg:space-x-8 xl:space-x-0">
                    <div class="flex flex-col justify-start items-start flex-shrink-0">
                        <div class="flex justify-center w-full md:justify-start items-center space-x-4 py-8 border-b border-gray-200 dark:border-gray-600">
                            <img src="/assets/user.png" class="h-12" alt="avatar" />
                            <div class="flex justify-start items-start flex-col space-y-2">
                            <p class="text-base dark:text-gray-300 font-semibold leading-4 text-left text-gray-800" v-if="order">{{ order.lastname }} {{ order.firstname }}</p>
                            <p class="text-sm dark:text-gray-300 leading-5 text-gray-600">10 Previous Orders</p>
                            </div>
                        </div>

                        <div class="flex justify-center text-gray-800 dark:text-gray-300 md:justify-start items-center space-x-4 py-4 border-b border-gray-200 dark:border-gray-600 w-full">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M3 7L12 13L21 7" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" />
                            </svg>
                            <p class="cursor-pointer text-sm leading-5 " v-if="order">{{ order.email }}</p>
                        </div>
                    </div>
                    <div class="flex rounded-lg justify-between items-stretch w-full flex-col mt-6 md:mt-0">
                        <div class="flex justify-center md:justify-start xl:flex-col flex-col md:space-x-6 lg:space-x-8 xl:space-x-0 space-y-4 xl:space-y-12 md:space-y-0 md:flex-row items-center md:items-start">
                            <div class="flex justify-center md:justify-start items-center md:items-start flex-col space-y-4 xl:mt-8">
                            <p class="text-base dark:text-gray-300 font-semibold leading-4 text-center md:text-left text-gray-800">Shipping Address / Phone</p>
                            <p class="w-48 lg:w-full dark:text-gray-300 xl:w-48 text-center md:text-left text-sm leading-5 text-gray-600" v-if="order">{{ order.b_address }} / {{ order.phone }}</p>
                            </div>
                            <div class="flex justify-center md:justify-start items-center md:items-start flex-col space-y-4">
                            <p class="text-base dark:text-gray-300 font-semibold leading-4 text-center md:text-left text-gray-800">City / State / zip code</p>
                            <p class="w-48 lg:w-full dark:text-gray-300 xl:w-48 text-center md:text-left text-sm leading-5 text-gray-600" v-if="order">
                                {{ order.b_city }} / 
                                <span v-if="!order.b_state">-</span> {{ order.b_state }} /
                                {{ order.b_zipcode }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>