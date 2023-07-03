<script setup>
import axios from "axios";
import { ref, onMounted, onBeforeMount, computed, reactive } from "vue";
import { acl } from "../router/acl";
import { useLoaderStore } from "@/stores/statestore";
import { initTE, Modal, Ripple, Dropdown, Select } from "tw-elements"
import ButtonComponent from "./components/ButtonComponent.vue";
import VueBasicAlert from "vue-basic-alert";
import { initFlowbite } from "flowbite";
import PlatformAddForm from "./components/forms/PlatformAddForm.vue";
import PlatformEditForm from "./components/forms/PlatformEditForm.vue";
import { s } from "plotly.js-dist";

const platforms = ref([])
const loading = ref(false)
const userRef = ref({ user: null, isAdmin: false });
const loadStore = useLoaderStore();
const selectedPlatform = ref([]);
const newPlatform = ref([]);
const selectedPlatformFields = ref([]);
const alert = ref(null);
const languages = ref([]);
const isLoading = computed(() => loadStore.isLoading);

const platformList = computed(() => {
    return platforms.value.filter((platform) => platform.language == userRef.value.user.default_language);
});

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
            platforms.value = response.data.platforms;
            languages.value = response.data.languages;

            languages.value.forEach((language) => {
                newPlatform.value.push({ name: "", fields: [], language: language, status: false });
            })

            loading.value = false;
        })
        .then(() => {
            initTE({ Ripple, Modal, Dropdown, Select });
            initFlowbite();
        })
};

const changeSelectedPlatform = (id) => {
    selectedPlatform.value = platforms.value.filter((platform) => platform.id === id).map((platform) => ({ ...platform }));
};

const updatePlatform = () => {
    loading.value = true;
    axios.put("/admin/platforms/" + selectedPlatform.value[0].id, selectedPlatform.value)
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
                                    <tr v-for="platform in platformList" :key="platform.id">
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
        <PlatformEditForm :isLoading="isLoading"
            :change-selected-type="changeSelectedType"
            :selected-platform="selectedPlatform"
            :update-platform="updatePlatform"
            :types="types"
            v-if="platforms.length > 0"
        />
        <PlatformAddForm :isLoading="isLoading"
            :add-platform="addPlatform"
            :change-selected-type="changeSelectedType"
            :new-platform="newPlatform"
            :push-field="pushField"
            :types="types"
            :selected-platform-fields="selectedPlatformFields"
            :languages="languages"
        />

    </main>
</template>