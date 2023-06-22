<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeMount, nextTick } from "vue";
import { initDrawers } from "flowbite";
import VueBasicAlert from "vue-basic-alert";
import { acl } from "../../../router/acl";
import { useRouter } from "vue-router";

const userRef = ref({ user: null, isAdmin: false });
const router = useRouter();
const alert = ref(null);

onBeforeMount(async () => {
  const test = await acl();
  userRef.value = test;
  userRef.value.user = test;
  userRef.value.isAdmin = test.roles == "Role_admin";
  console.log("get user information from acl", userRef.value.email);
});
const plenty_market = ref(null);
const isSuccess = ref("");
const isError = ref("");

const getPlentyMarketInformationByVendorPlatform = () => {
  axios
    .get("/plenty-market/vendor")
    .then((res) => {
      plenty_market.value = res.data[0] ?? {};
    })
    .then(() => {
      initDrawers();
    })
    .catch((err) => {
      if (err.response) {
        let status = err.response.status;
        if (status) {
          if (status == 403) {
            console.log(err.response.status);
            router.push("/error/403");
          } else if (status == 401) {
            router.push("/login");
          }
        }
      }
      isError.value = "You have an error please try again";
    });
};

const handSubmit = (e) => {
  const data = {
    referrer_id: e.target["referrer_id"].value | null,
    api_id: e.target["api_id"].value,
    api_secret: e.target["api_secret"].value,
    access_token: e.target["access_token"].value,
    platform_url: e.target["platform_url"].value,
    method_payment_id: e.target["method_payment_id"].value,
    shipping_profile_id: e.target["shipping_profile_id"].value,
    platform_id: e.target["platform_id"].value,
    export_product_link: e.target["export_product_link"].value,
  };

  axios
    .post("/plenty-market/update", data)
    .then((res) => {
      getPlentyMarketInformationByVendorPlatform();
      alert.value.showAlert("success", res.data, "Successful!!");
      console.log(res.data);
    })
    .catch((err) => {
      if (err.code == "ERR_NETWORK") {
        alert.value.showAlert("error", err.message, "Error !!");
      }
      alert.value.showAlert("error", err.response.data.detail[0].msg, "Error !!");
    });
};

onMounted(() => {});
getPlentyMarketInformationByVendorPlatform();
</script>

<template>
  <div id="app">
    <vue-basic-alert :duration="2000" :closeIn="5000" ref="alert" />
  </div>
  <div
    v-if="!userRef.isAdmin"
    class="px-[5%] justify-center items-center justify-items-center m-auto md:mt-[5%]"
  >
    <div class="grid w-full grid-cols-1">
      <h1
        class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-4xl lg:text-5xl dark:text-white"
      >
        {{ $t("mb_config_plenty_market") }}
      </h1>
      <p
        class="my-5 mb-10 text-lg font-normal text-gray-500 lg:text-xl dark:text-gray-400"
      >
        {{ $t("mb_plenty_market_des") }}
      </p>
    </div>

    <div
      v-if="isSuccess"
      id="alert-border-3"
      class="flex p-4 mb-4 text-green-800 border border-l-4 border-green-300 rounded-md bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800"
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
      class="flex p-4 mb-4 text-green-800 border border-l-4 border-red-300 rounded-md bg-red-50 dark:text-red-400 dark:bg-gray-800 dark:border-red-800"
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

    <form
      @submit.prevent="handSubmit($event)"
      action="/plenty-market/update"
      method="post"
      class="m-auto space-y-5"
      v-if="plenty_market"
    >
      <div class="gap-2 m-auto space-y-5 md:grid md:grid-cols-2 md:space-y-0">
        <div className="relative">
          <input
            type="number"
            id="platform_id"
            v-model="plenty_market.platform_id"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="platform_id"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_plenty_id") }}</label
          >
        </div>
        <div className="relative">
          <input
            type="number"
            id="referrer_id"
            v-model="plenty_market.referrer_id"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="referrer_id"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_referrer_id") }}</label
          >
        </div>
      </div>
      <div class="gap-2 m-auto space-y-5 md:grid md:grid-cols-2 md:space-y-0">
        <div className="relative">
          <input
            type="number"
            id="api_id"
            v-model="plenty_market.api_id"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="api_id"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_api_id") }}</label
          >
        </div>
        <div className="relative">
          <input
            type="number"
            id="api_secret"
            v-model="plenty_market.api_secret"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="api_secret"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_api_secret_id") }}</label
          >
        </div>
      </div>
      <div class="gap-2 m-auto space-y-5 md:grid md:grid-cols-2 md:space-y-0">
        <div className="relative">
          <input
            type="number"
            id="access_token"
            v-model="plenty_market.access_token"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="access_token"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_access_token") }}</label
          >
        </div>
        <div className="relative">
          <input
            type="text"
            id="platform_url"
            v-model="plenty_market.platform_url"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="platform_url"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_plenty_url") }}</label
          >
        </div>
      </div>
      <div class="gap-2 m-auto space-y-5 md:grid md:grid-cols-2 md:space-y-0">
        <div className="relative">
          <input
            type="number"
            id="method_payment_id"
            v-model="plenty_market.method_payment_id"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="method_payment_id"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_method_of_payment") }}</label
          >
        </div>
        <div className="relative">
          <input
            type="number"
            id="shipping_profile_id"
            v-model="plenty_market.shipping_profile_id"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="shipping_profile_id"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_shipping") }}</label
          >
        </div>

        <div className="relative w-full">
          <input
            type="text"
            id="export_product_link"
            v-model="plenty_market.export_product_link"
            className="block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-800 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
            placeholder=" "
          />
          <label
            htmlFor="export_product_link"
            className="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white dark:bg-gray-800 px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
            >{{ $t("md_export_product") }}</label
          >
        </div>
      </div>
      <button
        @click="handSubmit"
        class="float-left px-5 py-2 text-xl font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        {{ $t("md_save") }}
      </button>
    </form>
  </div>
</template>
