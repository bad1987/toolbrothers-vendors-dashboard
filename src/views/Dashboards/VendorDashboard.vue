<script setup>
import { initFlowbite } from 'flowbite'
import { onMounted, ref, onBeforeMount } from 'vue'
import { statStore } from '../../stores/StatStore'
import moment from 'moment';
import { getStats } from '../../api';
import Statistic from '../../components/dashboard/Statistic.vue';
import GraphStatistic from '../../components/dashboard/GraphStatistic.vue';
import initChart from '../../utils/drawshart';
import { useLoaderStore } from '../../stores/statestore';
import { storeToRefs } from 'pinia';
import DatePicker from '../../components/DatePicker.vue';

const _statstore = statStore()
const loaderStore = useLoaderStore()
const isErrorDate = ref(false)
const ErrorMessage = ref("")
const statDatas = ref(null)
const dates = ref(null)

const { isLoading } = storeToRefs(loaderStore)

function handleSubmitDate (_dates) {
  loaderStore.changeLoadingStatus(true)  
  const today = new Date();
  const start_date = moment(_dates.start_date, "MM/DD/YYYY").format('YYYY-MM-DD') 
  const end_date = moment(_dates.end_date, "MM/DD/YYYY").format('YYYY-MM-DD')
  dates.value = { start_date, end_date }
  const data = {
    start_date,
    end_date
  };
  if(data.end_date > moment(today).format('YYYY-MM-DD') || data.start_date > moment(today).format('YYYY-MM-DD') ){
    isErrorDate.value = true;
    ErrorMessage.value = "You cannot exceed the current date"
    loaderStore.changeLoadingStatus(false)  
  }else{
    getStats(_statstore.setStats, data).then(ans => {
      statDatas.value = ans
      loaderStore.changeLoadingStatus(false)  
    })
    isErrorDate.value = false;
  }   
}

onMounted(async () => {
  // initialize the stats store
  loaderStore.changeLoadingStatus(true)
  initFlowbite()
})
</script>

<template>
    <div class="px-4 pt-6 2xl:px-0">
      <div v-if="isErrorDate" class="flex p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800" role="alert">
        <svg aria-hidden="true" class="flex-shrink-0 inline w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
        <span class="sr-only">Info</span>
        <div>
          <span class="font-medium">Alert!</span> {{ErrorMessage}}.
        </div>
      </div>
      <!-- Filter by date form -->
      <div class="flex items-center justify-end flex-1 text-base font-medium text-green-500 dark:text-green-400 mb-5 ">
          <DatePicker @filter-date-range="handleSubmitDate" />
      </div>
      <div class="grid gap-4 xl:grid-cols-2 2xl:grid-cols-3">
        <div
          class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm 2xl:col-span-2 dark:border-gray-700 sm:p-6 dark:bg-gray-800">
          <div class="flex items-center justify-between mb-4" v-if="_statstore.stats">
            <div class="flex-shrink-0">
              <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white" >{{ _statstore.stats.sales }} €</span>
              <h3 class="text-base font-light text-gray-500 dark:text-gray-400">Sales this month</h3>
            </div>
            <div class="flex items-center justify-end flex-1 text-base font-medium text-green-500 dark:text-green-400">
              <div date-rangepicker id="date-rangepicker" class="flex items-center space-x-4">
                
              </div>
            </div>
          </div>
          <!-- statistic graph -->
          <GraphStatistic :datas="statDatas"/>
          
          <!-- statistic number -->
          <div class="flex items-center justify-between pt-3 mt-4 border-t border-gray-200 sm:pt-6 dark:border-gray-700">
          </div>
        </div>
        <Statistic/>
    </div>
  </div>
</template>