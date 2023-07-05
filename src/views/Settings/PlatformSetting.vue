<script setup>
import { useI18n } from "vue-i18n";
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import VueBasicAlert from "vue-basic-alert";

const platform = ref(null);
const { t } = useI18n();
const values = ref([])
const fields = ref([])
const alert = ref(null);
const updatedValues = ref({});

const dataValues = computed(() => {
    const arr = [];

    // parcourir l'objet et créer des mini-objets
    for (const prop in updatedValues.value) {
    if (updatedValues.value.hasOwnProperty(prop)) {
            const miniObj = {};
            miniObj.name = prop;
            miniObj.value = updatedValues.value[prop];
            arr.push(miniObj);
        }
    }

    return arr;
});



onMounted(async () => {
    fetchPlatform();
});

const fetchPlatform = async () => {
    try {
        const response = axios.get("/users/platform")
        .then((response) => {
            platform.value = response.data;
            values.value = response.data.values;
            fields.value = response.data.fields;

            for (const prop in values.value) {
                let value = values.value[prop];

                updatedValues.value[value.name] = value.value;
            }
        })


    } catch (error) {
        console.log(error);
    }
};

const updatePlatform = async () => {
    try {
        const response = axios.put("/users/platform", {
            id: platform.value.id,
            values: dataValues.value
        })
        .then((response) => {
            fetchPlatform();
            alert.value.showAlert("success", "Platform settings updated successfuly", "Successful!!");
        })
    }
    catch (error) {
        console.log(error);
        alert.value.showAlert("error", error.response.data.detail, "Error!!");
    }
}

function getType(type) {
    return type == 'int' || type == 'float' ? 'number' : 'text';
}

function getValue(name) {
    return values.value[name];
}

</script>

<template>
    <main class="mx-5 mt-[6%] px-[5%] dark:bg-gray-800 dark:border-gray-700" v-if="platform">
        <vue-basic-alert :duration="2000" :closeIn="5000" ref="alert" />
        <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 sm:p-6 dark:bg-gray-800">
            <!-- Card header -->
            <div class="items-center justify-between lg:flex">
                <div class="items-center justify-between lg:flex">
                    <div class="mb-4 lg:mb-0">
                        <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">
                            {{ $t('your_platform') }}
                            <span class="px-2 py-1 text-sm text-white bg-green-500 rounded-md">{{
                                $t("mb_active")
                            }}</span>
                        </h3>
                        <span class="text-base font-normal text-gray-500 dark:text-gray-400">
                            {{ $t('this_your_platform') }} ({{ platform.name }})
                        </span>
                    </div>
                </div>
            </div>
            <!-- Card body -->

            <form class="mt-20" id="form" @submit.prevent="updatePlatform">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
                    <div class="mb-2" v-for="(field, idx) in fields" :key="idx">
                        <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{ field.name }}</label>
                        <input :type="getType(field.type)" id=""
                            class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
                            :placeholder="field.name" v-model="updatedValues[field.name]" required>
                    </div>
                </div>
                <button 
                    type="submit"
                    id="submit"
                    class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 mt-3">{{ $t('update_settings') }}</button>
            </form>

        </div>
    </main>
</template>