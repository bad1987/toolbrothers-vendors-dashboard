<script setup>
  import VendorDashboard from './Dashboards/VendorDashboard.vue';
  import AdminDashboard from './Dashboards/AdminDashboard.vue';
  import { onMounted, ref } from 'vue';
  import { acl } from '../router/acl';

  const user = ref(null)

  onMounted(async () => {
    user.value = await acl()
  })
</script>

<template>
  <main v-if="user">
    <AdminDashboard v-if="user.roles == 'Role_admin'"/>
    <VendorDashboard v-else/>
  </main>
</template>