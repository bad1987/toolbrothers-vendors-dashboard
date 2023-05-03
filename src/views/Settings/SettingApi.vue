<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeMount } from "vue";
import { initDrawers } from "flowbite";

import { acl } from "../../router/acl";
import { useRouter } from "vue-router";

const userRef = ref({ user: null, isAdmin: false });
const router = useRouter();

onBeforeMount(async () => {
  const test = await acl();
  userRef.value = test;
  userRef.value.user = test;
  userRef.value.isAdmin = test.roles == "Role_admin";
});
const token_api = ref([]);
const isSuccess = ref("");
const isError = ref("");

const generateTokenApi = () => {
  axios
    .get("/setting/api-token-user")
    .then((res) => {
        getTokenApi();
    })
    .then(() => {
      initDrawers();
    })
    .catch((err) => {
      if (err.response) {
        let status = err.response.status;
        if (status) {
          if (status == 403) {
            router.push("/error/403");
          } else if (status == 401) {
            router.push("/login");
          }
        }
      }
      isError.value = "You have an error please try again";
    });
};

const getTokenApi = () => {
  axios
    .get("/setting/get-token-api")
    .then((res) => {
      token_api.value = res.data;
    })
    .then(() => {
      initDrawers();
    })
    .catch((err) => {
      if (err.response) {
        let status = err.response.status;
        if (status) {
          if (status == 403) {
            router.push("/error/403");
          } else if (status == 401) {
            router.push("/login");
          }
        }
      }
      isError.value = "You have an error please try again";
    });
};

onMounted(() => {});
getTokenApi();
</script>

<template>
  <div
    v-if="!userRef.isAdmin"
    class="px-[5%] justify-center items-center justify-items-center m-auto md:mt-[5%]"
  >
    <div class="w-full grid grid-cols-1">
      <h1
        class="mb-4 text-2xl font-extrabold leading-none tracking-tight text-gray-900 md:text-4xl dark:text-white"
      >
        Your token Api
      </h1>
      <p
        class="my-5 mb-10 text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400"
      >
      This token will allow you to use our API from your platform. It must be kept secret
      </p>
    </div>

    <div
      v-if="isSuccess"
      id="alert-border-3"
      class="flex p-4 mb-4 text-green-800 border-l-4 border rounded-md border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800"
      role="alert"
    >
      <svg
        class="flex-shrink-0 w-5 h-5"
        fill="currentColor"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
          clip-rule="evenodd"
        ></path>
      </svg>
      <div class="ml-3 text-sm font-medium">
        {{ isSuccess }}
      </div>
      <button
        type="button"
        class="ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"
        data-dismiss-target="#alert-border-3"
        aria-label="Close"
      >
        <span class="sr-only">Dismiss</span>
        <svg
          aria-hidden="true"
          class="w-5 h-5"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          ></path>
        </svg>
      </button>
    </div>

    <div
      v-if="isError"
      id="alert-border-4"
      class="flex p-4 mb-4 text-green-800 border-l-4 border rounded-md border-red-300 bg-red-50 dark:text-red-400 dark:bg-gray-800 dark:border-red-800"
      role="alert"
    >
      <svg
        class="flex-shrink-0 w-5 h-5"
        fill="currentColor"
        viewBox="0 0 20 20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
          clip-rule="evenodd"
        ></path>
      </svg>
      <div class="ml-3 text-sm font-medium">
        {{ isError }}
      </div>
      <button
        type="button"
        class="ml-auto -mx-1.5 -my-1.5 bg-red-50 text-red-500 rounded-lg focus:ring-2 focus:ring-red-400 p-1.5 hover:bg-red-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-red-400 dark:hover:bg-gray-700"
        data-dismiss-target="#alert-border-4"
        aria-label="Close"
      >
        <span class="sr-only">Dismiss</span>
        <svg
          aria-hidden="true"
          class="w-5 h-5"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          ></path>
        </svg>
      </button>
    </div>
    <div class="w-full mb-4 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
        <div class="px-4 py-2 bg-white rounded-t-lg dark:bg-gray-800">
            <label for="token" class="sr-only">Your token</label>
            <textarea v-model="token_api" id="token" rows="4" disabled class="w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400" placeholder="You don't have a token" required></textarea>
        </div>
        <div class="flex items-center justify-between px-3 py-2 border-t dark:border-gray-600">
            <button @click="generateTokenApi" type="submit" class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 hover:bg-blue-800">
                Generate a new token
            </button>
        </div>
    </div>
  </div>
</template>

<style></style>
