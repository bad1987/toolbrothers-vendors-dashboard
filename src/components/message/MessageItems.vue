<script setup>

    const props = defineProps({
        item: {
            type: Object,
        }
    })
    
    console.log(props.item);
</script>

<template>
    <div className="w-full h-84 p-3 border bg-white dark:bg-gray-600 dark:border-gray-500 mt-5 rounded-lg">
        <div className="flex items-center gap-1">
            <svg fill="currentColor" class="h-6 w-6 text-gray-300" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path clip-rule="evenodd" fill-rule="evenodd" d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"></path>
            </svg>
            <p className="text-gray-500 dark:text-gray-300 font-semibold text-sm ">{{ props.item.cscart_users.firstname }} {{ props.item.cscart_users.lastname }}</p>
        </div>
        <p className="text-lg font-semibold mt-5 dark:text-gray-300">Thread #{{ props.item.thread_id }}</p>
        <p className="text-sm mt-3 text-gray-500 dark:text-gray-300 line-clamp-4">{{ props.item.last_message }}</p>
        <RouterLink :to="`/chat/${props.item.thread_id}/${props.item.user_id}/${props.item.cscart_users.lastname}`" className="h-8 mt-5 w-32 cursor-pointer font-semibold transition-all hover:text-gray-700 dark:bg-gray-500 bg-gray-300 dark:text-gray-300 flex justify-center items-center text-sm rounded-full">Open chat</RouterLink>
        <div className="flex justify-between items-center mt-6">
            <div className="flex items-center gap-2">
                <i className="cursor-pointer text-gray-400 fa fa-calendar-o" />
                <p className="text-gray-400 font-semibold text-xs dark:text-gray-300">{{ props.item.last_updated }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped></style>