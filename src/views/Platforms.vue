<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeMount, computed } from "vue";
import { acl } from "../router/acl";
import { useLoaderStore } from "@/stores/statestore";
import { initTE, Modal, Ripple, Dropdown, Select } from "tw-elements"
import ButtonComponent from "./components/ButtonComponent.vue";
import VueBasicAlert from "vue-basic-alert";

const platforms = ref([])
const loading = ref(false)
const userRef = ref({ user: null, isAdmin: false });
const loadStore = useLoaderStore();
const searchTerm = ref("");
const selectedPlatform = ref({});
const newPlatform = ref({});
const selectedPlatformFields = ref([]);
const alert = ref(null);
const isLoading = computed(() => loadStore.isLoading);

const types = ref([{ text: "Integer", value: "int" }, { text: "String", value: "string" }, { text: "Boolean", value: "bool" }, { text: "Float", value: "float" }]);


onBeforeMount(async () => {
    const test = await acl();
    userRef.value = test;
    userRef.value.user = test;
    userRef.value.isAdmin = test.roles == "Role_admin";
});

const fetchPlatforms = async () => {
    loading.value = true;
    axios.get("/admin/platforms")
        .then((response) => {
            platforms.value = response.data;
            loading.value = false;
        })
        .then(() => {
            initTE({ Ripple, Modal, Dropdown, Select });
        })

};

const changeSelectedPlatform = (id) => {
    Object.assign(selectedPlatform.value, platforms.value.find((platform) => platform.id === id));
    selectedPlatformFields.value = selectedPlatform.value.fields;
};

const updatePlatform = () => {
    if (selectedPlatformFields.value.find((field) => field.name.trim() === "")) {
        alert.value.showAlert("error", "Please fill the empty field name", "Error!!");
        return;
    }
    loading.value = true;
    axios.put("/admin/platforms/" + selectedPlatform.value.id, selectedPlatform.value)
        .then((response) => {
            fetchPlatforms();
            document.getElementById("edit-platform-close")?.click();
            alert.value.showAlert("success", "Platform updated successfuly", "Successful!!");
        })
        .catch((error) => {
            console.log(error);
            alert.value.showAlert("error", error.response.data.detail, "Error!!");
        })
        .finally(() => {
            loading.value = false;
        })
};

const addPlatform = () => {
    // check if there is a field with empty name
    if (selectedPlatformFields.value.find((field) => field.name.trim() === "")) {
        alert.value.showAlert("error", "Please fill the empty field name", "Error!!");
        return;
    }
    loading.value = true;
    newPlatform.value.fields = selectedPlatformFields.value;
    axios.post("/admin/platforms", newPlatform.value)
        .then((response) => {
            fetchPlatforms();
            document.getElementById("add-platform-close")?.click();
            alert.value.showAlert("success", "Platform added successfuly", "Successful!!");
        })
        .catch((error) => {
            console.log(error);
            alert.value.showAlert("error", error.response.data.detail, "Error!!");
        })
        .finally(() => {
            loading.value = false;
        })
};

const deletePlatform = (id) => {
    loading.value = true;
    axios.delete("/admin/platforms/" + id)
        .then((response) => {
            fetchPlatforms();
            alert.value.showAlert("success", "Platform deleted successfuly", "Successful!!");
        })
        .catch((error) => {
            console.log(error);
            alert.value.showAlert("error", error.response.data.detail, "Error!!");
        })
        .finally(() => {
            loading.value = false;
        })
};

const changeSelectedType = (name, type) => {
    var selected = selectedPlatformFields.value.find((field) => field.name === name);
    selected.type = type;

    selectedPlatform.value.fields = selectedPlatformFields.value;
};

const pushField = () => {
    // check if there is a field with empty name
    if (selectedPlatformFields.value.find((field) => field.name.trim() === "")) {
        alert.value.showAlert("error", "Please fill the empty field name", "Error!!");
        return;
    }
    // check if there are fields with the same name
    if (selectedPlatformFields.value.length !== new Set(selectedPlatformFields.value.map((field) => field.name.trim())).size) {
        alert.value.showAlert("error", "Please make sure that there are no fields with the same name", "Error!!");
        return;
    }
    selectedPlatformFields.value.push({ name: "", type: "string" });
};

const deleteField = (field) => {
    selectedPlatformFields.value = selectedPlatformFields.value.filter((f) => f.name !== field.name);
    selectedPlatform.value.fields = selectedPlatformFields.value;
};

onMounted(() => {
    fetchPlatforms();
});

</script>

<template>
    <main class="mx-5 mt-7 mb-[5%] dark:bg-gray-800 dark:bplatform-gray-700" id="app">
        <vue-basic-alert :duration="1000" :closeIn="2000" ref="alert" />
        <div
            class="p-4 bg-white bplatform bplatform-gray-200 rounded-lg shadow-sm dark:bplatform-gray-700 sm:p-6 dark:bg-gray-800">
            <div class="items-center justify-between lg:flex">
                <div class="mb-4 lg:mb-0">
                    <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">
                        {{ $t("Platforms") }}
                    </h3>
                    <span class="text-base font-normal text-gray-500 dark:text-gray-400">Manage platforms
                    </span>
                </div>

                <div class="flex items-center ml-auto space-x-2 sm:space-x-3">
                    <button @click="selectedPlatformFields = []" type="button"
                        class="inline-flex items-center justify-center w-1/2 px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 sm:w-auto dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                        data-te-toggle="modal" data-te-target="#add-platform-modal" data-te-ripple-init
                        data-te-ripple-color="light">
                        <svg class="w-5 h-5 mr-2 -ml-1" fill="currentColor" viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd"
                                d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                                clip-rule="evenodd"></path>
                        </svg>
                        Add new platform
                    </button>
                </div>

            </div>
            <div class="flex flex-col mt-6 relative">
                <div v-if="isLoading"
                    class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-10 flex min-h-[250px]">
                    <div role="status" class="w-max m-auto">
                        <svg aria-hidden="true"
                            class="inline w-12 h-12 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-500"
                            viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="currentColor" />
                            <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="currentFill" />
                        </svg>
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
                <div class="overflow-x-auto rounded-lg">
                    <div class="inline-block min-w-full align-middle">
                        <div class="overflow-hidden shadow sm:rounded-lg">
                            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-600">
                                <thead class="bg-gray-50 dark:bg-gray-700">
                                    <tr>
                                        <th scope="col"
                                            class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                                            ID
                                        </th>
                                        <th scope="col"
                                            class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                                            Status
                                        </th>
                                        <th scope="col"
                                            class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                                            Name
                                        </th>
                                        <th scope="col"
                                            class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white dark:bg-gray-800">
                                    <!-- <tr v-for="u in skeletonCnt" role="status" :key="u"
                                        class="max-w-md p-4 space-y-5 divide-gray-200 rounded animate-pulse dark:divide-gray-700 md:p-6">
                                        <td v-for="u in 6" class="items-center" :key="u">
                                            <div class="flex items-center justify-between">
                                                <div>
                                                    <div class="w-32 h-3 bg-gray-200 rounded-full dark:bg-gray-700">
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <div class="h-3"></div>
                                    </tr> -->
                                    <tr v-for="platform in platforms" :key="platform.id">
                                        <td class="p-4 text-sm font-normal text-gray-900 whitespace-nowrap dark:text-white">
                                            <span class="font-semibold">#{{ platform.id }}</span>
                                        </td>
                                        <td
                                            class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                                            <span v-if="platform.status == true"
                                                class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-green-400 bplatform bplatform-green-100 dark:bplatform-green-500">
                                                Active
                                            </span>
                                            <span v-else
                                                class="bg-red-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-red-400 bplatform bplatform-red-100 dark:bplatform-red-500">
                                                Inactive
                                            </span>
                                        </td>
                                        <td
                                            class="inline-flex items-center p-4 space-x-2 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                                            <span>{{ platform.name }}</span>
                                        </td>
                                        <td class="p-4 text-gray-500 whitespace-nowrap dark:text-gray-400 space-x-1">
                                            <button @click="changeSelectedPlatform(platform.id)" type="button"
                                                class="inline-flex items-center px-3 py-1 text-sm font-medium text-center text-white rounded-lg bg-blue-500 hover:bg-blue-800 focus:ring-4 focus:ring-blue-400 dark:bg-blue-500 dark:hover:bg-blue-800 dark:focus:ring-blue-500"
                                                data-te-toggle="modal" data-te-target="#edit-platform-modal"
                                                data-te-ripple-init data-te-ripple-color="light">
                                                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"
                                                    xmlns="http://www.w3.org/2000/svg">
                                                    <path
                                                        d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z">
                                                    </path>
                                                    <path fill-rule="evenodd"
                                                        d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"
                                                        clip-rule="evenodd"></path>
                                                </svg>
                                                Edit
                                            </button>
                                            <button @click="deletePlatform(platform.id)" type="button"
                                                class="inline-flex items-center px-3 py-1 text-sm font-medium text-center text-white bg-red-400 rounded-lg hover:bg-red-600 focus:ring-4 focus:ring-red-300 dark:focus:ring-red-900">
                                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor"
                                                    stroke-width="1.5" viewBox="0 0 24 24"
                                                    xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5m6 4.125l2.25 2.25m0 0l2.25 2.25M12 13.875l2.25-2.25M12 13.875l-2.25 2.25M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z">
                                                    </path>
                                                </svg>
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modals -->
        <div data-te-modal-init
            class="fixed left-0 top-0 z-[1055] hidden h-full w-full overflow-y-auto overflow-x-hidden outline-none"
            id="edit-platform-modal" tabindex="-1" aria-labelledby="edit-platform-modalTitle" aria-modal="true"
            role="dialog">
            <div data-te-modal-dialog-ref
                class="pointer-events-none relative flex min-h-[calc(100%-1rem)] w-auto translate-y-[-50px] items-center opacity-0 transition-all duration-300 ease-in-out min-[576px]:mx-auto min-[576px]:mt-7 min-[576px]:min-h-[calc(100%-3.5rem)] min-[576px]:max-w-[500px]">
                <div
                    class="pointer-events-auto relative flex w-full flex-col rounded-md border-none bg-white bg-clip-padding text-current shadow-lg outline-none dark:bg-neutral-600">
                    <div v-if="isLoading" class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-10 flex">
                        <div role="status" class="w-max m-auto">
                            <svg aria-hidden="true"
                                class="inline w-12 h-12 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-500"
                                viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path
                                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                    fill="currentColor" />
                                <path
                                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                    fill="currentFill" />
                            </svg>
                            <span class="sr-only">Loading...</span>
                        </div>
                    </div>
                    <div
                        class="flex flex-shrink-0 items-center justify-between rounded-t-md border-b-2 border-neutral-100 border-opacity-100 p-4 dark:border-opacity-50">
                        <!--Modal title-->
                        <h5 class="text-xl font-medium leading-normal text-neutral-800 dark:text-neutral-200"
                            id="edit-platform-modalScrollableLabel">
                            Edit Platform
                        </h5>
                        <!--Close button-->
                        <button type="button" id="edit-platform-close"
                            class="box-content rounded-none border-none hover:no-underline hover:opacity-75 focus:opacity-100 focus:shadow-none focus:outline-none"
                            data-te-modal-dismiss aria-label="Close">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="h-6 w-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <!--Modal body-->
                    <div class="mb-4 border-b border-gray-200 dark:border-gray-700">
                        <ul class="flex flex-wrap -mb-px text-sm font-medium text-center" id="myTab"
                            data-tabs-toggle="#myTabContent" role="tablist">
                            <li class="mr-2" role="presentation">
                                <button class="inline-block p-4 border-b-2 rounded-t-lg" id="profile-tab"
                                    data-tabs-target="#profile" type="button" role="tab" aria-controls="profile"
                                    aria-selected="false">EN</button>
                            </li>
                            <li class="mr-2" role="presentation">
                                <button
                                    class="inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300"
                                    id="dashboard-tab" data-tabs-target="#dashboard" type="button" role="tab"
                                    aria-controls="dashboard" aria-selected="false">DE</button>
                            </li>
                        </ul>
                    </div>
                    <div id="myTabContent">
                        <div class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" id="profile" role="tabpanel"
                            aria-labelledby="profile-tab">
                            <div class="p-4">
                                <div class="mb-6">
                                    <label for="base-input"
                                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Platform
                                        name</label>
                                    <input v-model="selectedPlatform.name" type="text" id="base-input"
                                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                </div>
                                <div class="relative mb-4 flex w-full items-center space-x-1"
                                    v-for="field, idx in selectedPlatformFields" :key="idx">
                                    <input type="text" id="base-input" v-model="field.name"
                                        class="w-3/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                    <select data-te-select-init
                                        @change="changeSelectedType(field.name, $event.target.value)"
                                        class="w-1/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                        <option :value="type.value" v-for="type, id in types" :key="id"
                                            :selected="field.type == type.value">{{
                                                type.text }}</option>
                                    </select>
                                    <div class="text-red-600 cursor-pointer" @click="deleteField(field)">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                            stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                            <path clip-rule="evenodd" fill-rule="evenodd"
                                                d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm3 10.5a.75.75 0 000-1.5H9a.75.75 0 000 1.5h6z">
                                            </path>
                                        </svg>
                                    </div>
                                </div>
                                <div class="mt-9 flex">
                                    <input v-model="selectedPlatform.status" id="checkbox-activate-create-platform"
                                        type="checkbox" value=""
                                        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                                    <label for="checkbox-activate-create-platform"
                                        class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Activate</label>
                                </div>
                                <div class="mt-9 cursor-pointer flex items-center w-max" @click="pushField">
                                    <svg class="w-8 h-8 mr-1" fill="currentColor" viewBox="0 0 24 24"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path clip-rule="evenodd" fill-rule="evenodd"
                                            d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z">
                                        </path>
                                    </svg>
                                    <span class="text-xs font-bold text-gray-400">Add a field</span>
                                </div>
                            </div>
                        </div>
                        <div class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" id="dashboard" role="tabpanel"
                            aria-labelledby="dashboard-tab">
                            <div class="p-4">
                                <div class="mb-6">
                                    <label for="base-input"
                                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Name der Plattform</label>
                                    <input v-model="selectedPlatform.name" type="text" id="base-input"
                                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                </div>
                                <div class="relative mb-4 flex w-full items-center space-x-1"
                                    v-for="field, idx in selectedPlatformFields" :key="idx">
                                    <input type="text" id="base-input" v-model="field.name"
                                        class="w-3/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                    <select data-te-select-init
                                        @change="changeSelectedType(field.name, $event.target.value)"
                                        class="w-1/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                        <option :value="type.value" v-for="type, id in types" :key="id"
                                            :selected="field.type == type.value">{{
                                                type.text }}</option>
                                    </select>
                                    <div class="text-red-600 cursor-pointer" @click="deleteField(field)">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                            stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                            <path clip-rule="evenodd" fill-rule="evenodd"
                                                d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm3 10.5a.75.75 0 000-1.5H9a.75.75 0 000 1.5h6z">
                                            </path>
                                        </svg>
                                    </div>
                                </div>
                                <div class="mt-9 flex">
                                    <input v-model="selectedPlatform.status" id="checkbox-activate-create-platform"
                                        type="checkbox" value=""
                                        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                                    <label for="checkbox-activate-create-platform"
                                        class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">aktivieren Sie</label>
                                </div>
                                <div class="mt-9 cursor-pointer flex items-center w-max" @click="pushField">
                                    <svg class="w-8 h-8 mr-1" fill="currentColor" viewBox="0 0 24 24"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path clip-rule="evenodd" fill-rule="evenodd"
                                            d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z">
                                        </path>
                                    </svg>
                                    <span class="text-xs font-bold text-gray-400">Fügen Sie ein Feld hinzu</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!--Modal footer-->
                    <div class="items-center p-6 border-t border-gray-200 rounded-b dark:border-gray-700">
                        <ButtonComponent @click="updatePlatform()" text="Save Platform"
                            classes="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                            :loading="isLoading" />
                    </div>
                </div>
            </div>
        </div>
        <div data-te-modal-init
            class="fixed left-0 top-0 z-[1055] hidden h-full w-full overflow-y-auto overflow-x-hidden outline-none"
            id="add-platform-modal" tabindex="-1" aria-labelledby="add-platform-modalTitle" aria-modal="true" role="dialog">
            <div data-te-modal-dialog-ref
                class="pointer-events-none relative flex min-h-[calc(100%-1rem)] w-auto translate-y-[-50px] items-center opacity-0 transition-all duration-300 ease-in-out min-[576px]:mx-auto min-[576px]:mt-7 min-[576px]:min-h-[calc(100%-3.5rem)] min-[576px]:max-w-[500px]">
                <div
                    class="pointer-events-auto relative flex w-full flex-col rounded-md border-none bg-white bg-clip-padding text-current shadow-lg outline-none dark:bg-neutral-600">
                    <div v-if="isLoading" class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-10 flex">
                        <div role="status" class="w-max m-auto">
                            <svg aria-hidden="true"
                                class="inline w-12 h-12 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-500"
                                viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path
                                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                    fill="currentColor" />
                                <path
                                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                    fill="currentFill" />
                            </svg>
                            <span class="sr-only">Loading...</span>
                        </div>
                    </div>
                    <div
                        class="flex flex-shrink-0 items-center justify-between rounded-t-md border-b-2 border-neutral-100 border-opacity-100 p-4 dark:border-opacity-50">
                        <!--Modal title-->
                        <h5 class="text-xl font-medium leading-normal text-neutral-800 dark:text-neutral-200"
                            id="add-platform-modalScrollableLabel">
                            Add Platform
                        </h5>
                        <!--Close button-->
                        <button type="button" id="add-platform-close"
                            class="box-content rounded-none border-none hover:no-underline hover:opacity-75 focus:opacity-100 focus:shadow-none focus:outline-none"
                            data-te-modal-dismiss aria-label="Close">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="h-6 w-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <!--Modal body-->
                    <div class="p-4">
                        <div class="mb-6">
                            <label for="base-input"
                                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Platform name</label>
                            <input v-model="newPlatform.name" type="text" id="base-input"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                        </div>
                        <div class="relative mb-4 flex w-full" v-for="field, idx in selectedPlatformFields" :key="idx">
                            <input type="text" id="base-input" v-model="field.name"
                                class="w-3/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                            <select data-te-select-init @change="changeSelectedType(field.name, $event.target.value)"
                                class="w-1/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                <option :value="type.value" v-for="type, id in types" :key="id"
                                    :selected="field.type == type.value">{{
                                        type.text }}</option>
                            </select>
                        </div>
                        <div class="mt-9 flex">
                            <input v-model="newPlatform.status" id="checkbox-activate-create-platform" type="checkbox"
                                value=""
                                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                            <label for="checkbox-activate-create-platform"
                                class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Activate</label>
                        </div>
                        <div class="mt-9 cursor-pointer flex items-center w-max" @click="pushField">
                            <svg class="w-8 h-8 mr-1" fill="currentColor" viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg">
                                <path clip-rule="evenodd" fill-rule="evenodd"
                                    d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z">
                                </path>
                            </svg>
                            <span class="text-xs font-bold text-gray-400">Add a field</span>
                        </div>
                    </div>
                    <!--Modal footer-->
                    <div class="items-center p-6 border-t border-gray-200 rounded-b dark:border-gray-700">
                        <ButtonComponent @click="addPlatform()" text="Add"
                            classes="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                            :loading="isLoading" />
                    </div>
                </div>
            </div>
        </div>

    </main>
</template>