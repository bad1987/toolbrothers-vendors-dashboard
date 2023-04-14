<script setup>
    import { defineProps, ref, defineEmits } from 'vue'


    const selected = ref([])
    const props = defineProps({
        items: Array,
        name: String,
        id: String,
        selected: Array
    })

    const emits = defineEmits(['toggleValue'])

    function toggleValue(item) {
        emits('toggleValue', item)
    }

    function isChecked(val) {
        if (props['selected'] == null) return false
        return props['selected'].map(x => x.id).includes(val)
    }
</script>

<template>
    <div v-for="(item, idx) in props.items" :key="idx">
        <input :checked="isChecked(item.value)" @change="toggleValue(item)" :id="`checkbox-${props.name}-${idx}`" type="checkbox"  :value="item.value" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
        <label :for="`checkbox-${props.name}-${idx}`" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{ item.description }}</label>
    </div>
</template>