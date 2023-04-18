<script setup>
    import { defineProps, onBeforeMount, ref, onUpdated } from 'vue'

    const props = defineProps({
        text: String,
        classes: String,
        loading: Boolean
    })

    const classeNames = ref(props['classes'])

    onUpdated(() => {
        classeNames.value = props['loading'] ? props['classes'] + ' pointer-events-none opacity-50' : props['classes']
    })

</script>

<template>
    <button
        :class=classeNames
        type="submit">{{ text }}</button>
</template>
