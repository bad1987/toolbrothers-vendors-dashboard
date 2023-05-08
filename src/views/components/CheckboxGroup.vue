<script setup>
    import { defineProps, ref, defineEmits, onBeforeMount, onMounted } from 'vue'


    const itemsByGroup = ref([])
    const props = defineProps({
        items: Array,
        name: String,
        id: String,
        selected: Array,
        isGrouped: Boolean,
        isHorizontal: Boolean
    })

    onBeforeMount(() => {
        props['items'].forEach(item => {
            let val = itemsByGroup.value.find(x => x.name == item.text.split("_")[1])
            if ( val == null) {
                itemsByGroup.value.push({name: item.text.split("_")[1], items: [item]})
            }else {
                val.items.push(item)
            }
        })
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
    <div v-if="!isGrouped" v-for="(item, idx) in props.items" :key="idx" :class="isHorizontal ? 'grid grid-cols-3' : ''">
        <input :checked="isChecked(item.value)" @change="toggleValue(item)" :id="`checkbox-${props.name}-${idx}`" type="checkbox"  :value="item.value" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
        <label :for="`checkbox-${props.name}-${idx}`" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{ item.description }}</label>
    </div>
    <div v-else>
        <div class="grid grid-cols-2 gap-4">
            <div class="" v-for="group in itemsByGroup" :key="group.name">
                <div class="my-3"><strong>{{ group.name }} permissions: </strong></div>
                <div class="" v-for="(item, idx) in group.items" :key="idx">
                    <input :checked="isChecked(item.value)" @change="toggleValue(item)" :id="`checkbox-${props.name}${group.name}-${idx}`" type="checkbox"  :value="item.value" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                    <label :for="`checkbox-${props.name}${group.name}-${idx}`" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">{{ item.description }}</label>
                </div>
            </div>
        </div>
    </div>
</template>