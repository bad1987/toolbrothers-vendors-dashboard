<script setup>
import { initFlowbite } from 'flowbite'
import { onMounted, ref, onBeforeMount } from 'vue'
import DateRangePicker from 'flowbite-datepicker/DateRangePicker';
import { Chart, registerables } from 'chart.js'
import Plotly, { lo } from 'plotly.js-dist'
import { statStore } from '../stores/StatStore'
import moment from 'moment';
import { getStats } from '../api';
import axios from 'axios';
import Statistic from '../components/dashboard/Statistic.vue';
import GraphStatistic from '../components/dashboard/GraphStatistic.vue';

const chart = ref(null)
const _statstore = statStore()
const isErrorDate = ref(false)
const ErrorMessage = ref("")
const isLoading = ref(false)
const dates = ref(null)

const dataState = ref(_statstore.stats)

Chart.register(...registerables)
  const chartData = ref([
      ['Date', 'Nombre'],
      [new Date(2023, 0, 1), 100],
      [new Date(2023, 0, 2), 150],
      [new Date(2023, 0, 3), 200],
      [new Date(2023, 0, 4), 250],
      [new Date(2023, 0, 5), 300],
      [new Date(2023, 0, 6), 300],
      [new Date(2023, 0, 7), 300],
      [new Date(2023, 0, 8), 300],
      [new Date(2023, 0, 9), 300],
      [new Date(2023, 0, 10), 300],
      [new Date(2023, 0, 11), 300],
      [new Date(2023, 0, 12), 300],
      [new Date(2023, 0, 13), 300],
      [new Date(2023, 0, 14), 300],
      [new Date(2023, 0, 15), 300],
      [new Date(2023, 0, 16), 300],
      [new Date(2023, 0, 17), 300],
      [new Date(2023, 0, 18), 300],
      [new Date(2023, 0, 19), 300],
      [new Date(2023, 0, 20), 300],
      [new Date(2023, 0, 21), 300],
      [new Date(2023, 0, 22), 300],
      [new Date(2023, 0, 23), 300],
      [new Date(2023, 0, 24), 300],
    ]);

  const chartOptions = ref({
    title: 'Nombre de ventes par jour',
    curveType: 'function',
    height: 500,
    width: '100%'
  });

  Chart.register(...registerables)

function handleSubmitDate () {
  isLoading.value = true
  const today = new Date();
  const start_date = moment(document.querySelector("input[name=start_date]").value, "MM/DD/YYYY").format('YYYY-MM-DD') 
  const end_date = moment(document.querySelector("input[name=end_date]").value, "MM/DD/YYYY").format('YYYY-MM-DD')
  if (document.querySelector("input[name=start_date]").value == '') {
    isLoading.value = false
    return
  }
  dates.value = { start_date, end_date }
  const data = {
    start_date,
    end_date
  };
  if(data.end_date > moment(today).format('YYYY-MM-DD') | data.start_date > moment(today).format('YYYY-MM-DD') ){

    isErrorDate.value = true;
    ErrorMessage.value = "You cannot exceed the current date"
  }else{
    getStats(_statstore.setStats, data).then(ans => {
      initChart(ans)      
      isLoading.value = false
    })
    isErrorDate.value = false;
  }
}

onMounted(async () => {
  // initialize the stats store
  isLoading.value = true
  initFlowbite()
  
  const dateRangePickerEl = document.getElementById('date-rangepicker');
  new DateRangePicker(dateRangePickerEl, {
  });
  
  _statstore.init().then(ans => {
      initChart(ans)      
      isLoading.value = false
    })

  // getStats(_statstore.setStats, null)
})

onBeforeMount (async () => {

  // initialize the stats store
  // _statstore.init()
})

function initChart(datas) {
  if (!datas) return

  // if (dates.value && moment(dates.value.end_date).diff(dates.value.start_date, 'month') <= 12) {
  //   console.log(datas.chart_datas.map(x => x.date.slice(5)))
  //  // Plot the chart based on months 
  //   Plotly.newPlot('main-chart', [
  //     {
  //       x: datas.chart_datas.map(x => x.date.slice(5)),
  //       y: datas.chart_datas.map(x => x.count),
  //       type: 'scatter',
  //       mode: 'lines',
  //       name: 'Current period'
  //     },
  //     {
  //       x: datas.prev_period.prev_chart.map(x => x.date.slice(5)),
  //       y: datas.prev_period.prev_chart.map(x => x.count),
  //       type: 'scatter',
  //       mode: 'lines',
  //       name: 'Prev period'
  //     }
  //   ], {
  //         xaxis: { tickformat: '%m-%d' }
  //   }, {
  //     displayModeBar: false, scrollZoom: false, responsive: true
  //   })

  //  return
  // }

  const element = document.getElementById('main-chart')
  Plotly.newPlot('main-chart', [
    {
      x: datas.chart_datas.map(x => x.date),
      y: datas.chart_datas.map(x => x.count),
      type: 'scatter',
      name: 'Current period'
    },
    {
      x: datas.prev_period.prev_chart.map(x => x.date),
      y: datas.prev_period.prev_chart.map(x => x.count),
      type: 'scatter',
      name: 'Prev period'
    }
  ], {paper_bgcolor:"#FFF3"}, {
    displayModeBar: false, scrollZoom: false, responsive: true
  })
}
</script>

<template>
  <main>
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
          <div date-rangepicker id="date-rangepicker" class="flex items-center space-x-4">
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path
                      d="M5.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H6a.75.75 0 01-.75-.75V12zM6 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H6zM7.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H8a.75.75 0 01-.75-.75V12zM8 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H8zM9.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V10zM10 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H10zM9.25 14a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V14zM12 9.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V10a.75.75 0 00-.75-.75H12zM11.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V12zM12 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H12zM13.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H14a.75.75 0 01-.75-.75V10zM14 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H14z">
                    </path>
                    <path clip-rule="evenodd" fill-rule="evenodd"
                      d="M5.75 2a.75.75 0 01.75.75V4h7V2.75a.75.75 0 011.5 0V4h.25A2.75 2.75 0 0118 6.75v8.5A2.75 2.75 0 0115.25 18H4.75A2.75 2.75 0 012 15.25v-8.5A2.75 2.75 0 014.75 4H5V2.75A.75.75 0 015.75 2zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75z">
                    </path>
                  </svg>
                </div>
                <input type="text" name="start_date" required
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                  placeholder="Start date"> 
              </div>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path
                      d="M5.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H6a.75.75 0 01-.75-.75V12zM6 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H6zM7.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H8a.75.75 0 01-.75-.75V12zM8 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H8zM9.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V10zM10 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H10zM9.25 14a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V14zM12 9.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V10a.75.75 0 00-.75-.75H12zM11.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V12zM12 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H12zM13.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H14a.75.75 0 01-.75-.75V10zM14 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H14z">
                    </path>
                    <path clip-rule="evenodd" fill-rule="evenodd"
                      d="M5.75 2a.75.75 0 01.75.75V4h7V2.75a.75.75 0 011.5 0V4h.25A2.75 2.75 0 0118 6.75v8.5A2.75 2.75 0 0115.25 18H4.75A2.75 2.75 0 012 15.25v-8.5A2.75 2.75 0 014.75 4H5V2.75A.75.75 0 015.75 2zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75z">
                    </path>
                  </svg>
                </div>
                <input type="text" name="end_date"  required
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                  placeholder="End date">
              </div>
              <button @click="handleSubmitDate" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 mt-2 focus:ring-blue-300 font-medium rounded-md text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Change date</button>
          </div>
      </div>
      <div class="grid gap-4 xl:grid-cols-2 2xl:grid-cols-3">
        <!-- Main widget -->
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
          <GraphStatistic :isLoading="isLoading" />
          
          <!-- statistic number -->
          <div class="flex items-center justify-between pt-3 mt-4 border-t border-gray-200 sm:pt-6 dark:border-gray-700">
          </div>
        </div>
        <Statistic :isLoading="isLoading" />
       
    </div>
  </div>

</main></template>