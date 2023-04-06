<script setup>
    import { defineProps, ref, onUpdated, defineEmits } from 'vue'


    const selected = ref([])
    const props = defineProps({
        items: Array,
        name: String,
        id: String
    })

    const emits = defineEmits(['toggleValue'])

    onUpdated(() => {

    })

    function toggleValue(item) {
        emits('toggleValue', item)
    }

</script>

<template>
    <div v-for="(item, idx) in props.items" :key="idx">
        <input @change="toggleValue(item)" :id="`checkbox-${props.name}-${idx}`" type="checkbox"  :value="item.value" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
        <label :for="`checkbox-${props.name}-${idx}`" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{ item.text }}</label>
    </div>
</template>