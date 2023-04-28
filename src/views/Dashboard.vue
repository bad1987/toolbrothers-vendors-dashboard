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

const chart = ref(null)
const _statstore = statStore()
const isErrorDate = ref(false)
const ErrorMessage = ref("")
const isLoading = ref(false)
const dates = ref(null)

const dataState = ref(_statstore.stats)

console.log("Statistic ", dataState.value);

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
  console.log("Les dates: ", dates.value)
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
  _statstore.init()
  isLoading.value = true
  initFlowbite()

  const dateRangePickerEl = document.getElementById('date-rangepicker');
  new DateRangePicker(dateRangePickerEl, {
  });

  getStats(_statstore.setStats, null).then(ans => {
      initChart(ans)      
      isLoading.value = false
    })
})

onBeforeMount (async () => {

  // initialize the stats store
  _statstore.init()
})

function initChart(datas) {
  if (!datas) return
  const element = document.getElementById('main-chart')

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
  ], {}, {
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
          <div class="flex items-center justify-between mb-4">
            <div class="flex-shrink-0">
              <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">$45,385</span>
              <h3 class="text-base font-light text-gray-500 dark:text-gray-400">Sales this week</h3>
            </div>
            <div class="flex items-center justify-end flex-1 text-base font-medium text-green-500 dark:text-green-400">
              <div date-rangepicker id="date-rangepicker" class="flex items-center space-x-4">
                
              </div>
            </div>
          </div>
          <div id="main-chart" class="min-h-[79%] relative">
            <div class="overlay absolute top-0 w-full h-full bg-white opacity-50 z-50 flex" v-if="isLoading">
              <div role="status" class="w-max m-auto">
                  <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-green-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                      <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                  </svg>
                  <span class="sr-only">Loading...</span>
              </div>
            </div>
          </div>
          <!-- Card Footer -->
          <div class="flex items-center justify-between pt-3 mt-4 border-t border-gray-200 sm:pt-6 dark:border-gray-700">
          </div>
        </div>

        <div
          class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 sm:p-6 dark:bg-gray-800">
          <h3 class="flex items-center mb-4 text-lg font-semibold text-gray-900 dark:text-white">{{$t("static_month")}}
            <button data-popover-target="popover-description" data-popover-placement="bottom-end" type="button"><svg
                class="w-4 h-4 ml-2 text-gray-400 hover:text-gray-500" aria-hidden="true" fill="currentColor"
                viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
                  clip-rule="evenodd"></path>
              </svg><span class="sr-only">Show information</span></button>
          </h3>
          <div data-popover id="popover-description" role="tooltip"
            class="absolute z-10 invisible inline-block text-sm font-light text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 w-72 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400">
            <div class="p-3 space-y-2">
              <h3 class="font-semibold text-gray-900 dark:text-white">{{$t("statistics")}}</h3>
              <p>{{$t("notice_statistic")}}</p>
            </div>
            <div data-popper-arrow></div>
          </div>
          <div class="sm:hidden">
            <label for="tabs" class="sr-only">Select tab</label>
            <select id="tabs"
              class="bg-gray-50 border-0 border-b border-gray-200 text-gray-900 text-sm rounded-t-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500">
              <option>Statistics</option>
              <option>Services</option>
              <option>FAQ</option>
            </select>
          </div>
          <ul
            class="hidden text-sm font-medium text-center text-gray-500 divide-x divide-gray-200 rounded-lg sm:flex dark:divide-gray-600 dark:text-gray-400"
            id="fullWidthTab" data-tabs-toggle="#fullWidthTabContent" role="tablist">
            <li class="w-full">
              <button id="faq-tab" data-tabs-target="#faq" type="button" role="tab" aria-controls="faq"
                aria-selected="true"
                class="inline-block w-full p-4 rounded-tl-lg bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">{{$t("mb_general_information")}}</button>
            </li>
            <li class="w-full">
              <button id="about-tab" data-tabs-target="#about" type="button" role="tab" aria-controls="about"
                aria-selected="false"
                class="inline-block w-full p-4 rounded-tr-lg bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600">Top
                Customers</button>
            </li>
          </ul>
          <div id="fullWidthTabContent" class="border-t border-gray-200 dark:border-gray-600">
            <div class="hidden pt-4" id="faq" role="tabpanel" aria-labelledby="faq-tab">
              <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
                <li class="py-3 sm:py-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <div class="ml-3">
                        <p class="font-medium text-gray-900 truncate dark:text-white">
                          {{$t("income")}}
                        </p>
                        <div v-if="_statstore.stats && parseFloat(_statstore.stats.prev_period.percent_income.slice(0, -1)) < 0" class="flex items-center justify-end flex-1 text-sm text-red-600 dark:text-red-500">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true">
                            <path clip-rule="evenodd" fill-rule="evenodd"
                              d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z">
                            </path>
                          </svg>
                          {{ parseFloat(_statstore.stats.prev_period.percent_income.slice(0, -1)) }} %
                          <span class="ml-2 text-gray-500">{{_statstore.stats.prev_period.label}}</span>
                        </div>
                        <div v-if="_statstore.stats && parseFloat(_statstore.stats.prev_period.percent_income.slice(0, -1)) > 0" class="flex items-center justify-end flex-1 text-sm text-green-500 dark:text-green-400">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true">
                            <path clip-rule="evenodd" fill-rule="evenodd"
                              d="M10 17a.75.75 0 01-.75-.75V5.612L5.29 9.77a.75.75 0 01-1.08-1.04l5.25-5.5a.75.75 0 011.08 0l5.25 5.5a.75.75 0 11-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0110 17z">
                            </path>
                          </svg>
                          {{ parseFloat(_statstore.stats.prev_period.percent_income.slice(0, -1)) }} %
                          <span class="ml-2 text-gray-500">{{_statstore.stats.prev_period.label}}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      <span v-if="!isLoading">
                        {{ _statstore.stats?.income }} €
                      </span>
                      <div v-if="isLoading" role="status">
                          <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-green-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                          </svg>
                          <span class="sr-only">Loading...</span>
                      </div>
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <div class="ml-3">
                        <p class="font-medium text-gray-900 truncate dark:text-white">
                          {{$t("sale")}}
                        </p>
                        <div v-if="_statstore.stats && parseFloat(_statstore.stats.prev_period.percent_sales.slice(0, -1)) < 0" class="flex items-center justify-end flex-1 text-sm text-red-600 dark:text-red-500">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true">
                            <path clip-rule="evenodd" fill-rule="evenodd"
                              d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z">
                            </path>
                          </svg>
                          {{ parseFloat(_statstore.stats.prev_period.percent_sales.slice(0, -1)) }} %
                          <span class="ml-2 text-gray-500">{{_statstore.stats.prev_period.label}}</span>
                        </div>
                        <div v-if="_statstore.stats && parseFloat(_statstore.stats.prev_period.percent_sales.slice(0, -1)) > 0" class="flex items-center justify-end flex-1 text-sm text-green-500 dark:text-green-400">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true">
                            <path clip-rule="evenodd" fill-rule="evenodd"
                              d="M10 17a.75.75 0 01-.75-.75V5.612L5.29 9.77a.75.75 0 01-1.08-1.04l5.25-5.5a.75.75 0 011.08 0l5.25 5.5a.75.75 0 11-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0110 17z">
                            </path>
                          </svg>
                          {{ parseFloat(_statstore.stats.prev_period.percent_sales.slice(0, -1)) }} %
                          <span class="ml-2 text-gray-500">{{_statstore.stats.prev_period.label}}</span>
                        </div>
                      </div>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      <span v-if="!isLoading">
                        {{ _statstore.stats?.sales }} €
                      </span>
                      <div v-if="isLoading" role="status">
                          <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-green-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                          </svg>
                          <span class="sr-only">Loading...</span>
                      </div>
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <div class="ml-3">
                        <p class="font-medium text-gray-900 truncate dark:text-white">
                          {{$t("orders")}}
                        </p>
                        <div v-if="_statstore.stats && parseFloat(_statstore.stats.prev_period.percent_orders.slice(0, -1)) < 0" class="flex items-center justify-end flex-1 text-sm text-red-600 dark:text-red-500">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true">
                            <path clip-rule="evenodd" fill-rule="evenodd"
                              d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z">
                            </path>
                          </svg>
                          {{ parseFloat(_statstore.stats.prev_period.percent_orders.slice(0, -1)) }} %
                          <span class="ml-2 text-gray-500">{{_statstore.stats.prev_period.label}}</span>
                        </div>
                        <div v-if="_statstore.stats && parseFloat(_statstore.stats.prev_period.percent_orders.slice(0, -1)) > 0" class="flex items-center justify-end flex-1 text-sm text-green-500 dark:text-green-400">
                          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true">
                            <path clip-rule="evenodd" fill-rule="evenodd"
                              d="M10 17a.75.75 0 01-.75-.75V5.612L5.29 9.77a.75.75 0 01-1.08-1.04l5.25-5.5a.75.75 0 011.08 0l5.25 5.5a.75.75 0 11-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0110 17z">
                            </path>
                          </svg>
                          {{ parseFloat(_statstore.stats.prev_period.percent_orders.slice(0, -1)) }} %
                          <span class="ml-2 text-gray-500">{{_statstore.stats.prev_period.label}}</span>
                        </div>
                      </div>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      <span v-if="!isLoading">
                        {{ _statstore.stats?.orders }}
                      </span>
                      <div v-if="isLoading" role="status">
                          <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-green-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                          </svg>
                          <span class="sr-only">Loading...</span>
                      </div>
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <div class="ml-3">
                        <p class="font-medium text-gray-900 truncate dark:text-white">
                          {{ $t("mb_active_product") }}
                        </p>
                      </div>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      <span v-if="!isLoading">
                        {{ _statstore.stats?.active_products }}
                      </span>
                      <div v-if="isLoading" role="status">
                          <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-green-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                          </svg>
                          <span class="sr-only">Loading...</span>
                      </div>
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <div class="ml-3">
                        <p class="font-medium text-gray-900 truncate dark:text-white">
                          {{ $t("mb_out_of_store") }}
                        </p>
                      </div>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      <span v-if="!isLoading">
                        {{ _statstore.stats?.out_of_stock }}
                      </span>
                      <div v-if="isLoading" role="status">
                          <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-green-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                          </svg>
                          <span class="sr-only">Loading...</span>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
            <div class="hidden pt-4" id="about" role="tabpanel" aria-labelledby="about-tab">
              <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
                <li class="py-3 sm:py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <img class="w-8 h-8 rounded-full" src="/images/users/neil-sims.png" alt="Neil image">
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-medium text-gray-900 truncate dark:text-white">
                        Neil Sims
                      </p>
                      <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                        email@flowbite.com
                      </p>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      $3320
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <img class="w-8 h-8 rounded-full" src="/images/users/bonnie-green.png" alt="Neil image">
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-medium text-gray-900 truncate dark:text-white">
                        Bonnie Green
                      </p>
                      <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                        email@flowbite.com
                      </p>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      $2467
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <img class="w-8 h-8 rounded-full" src="/images/users/michael-gough.png" alt="Neil image">
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-medium text-gray-900 truncate dark:text-white">
                        Michael Gough
                      </p>
                      <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                        email@flowbite.com
                      </p>
                    </div>
                    <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                      $2235
                    </div>
                  </div>
                </li>
                <li class="py-3 sm:py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <img class="w-8 h-8 rounded-full" src="/images/users/thomas-lean.png" alt="Neil image">
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-medium text-gray-900 truncate dark:text-white">
                      Thomes Lean
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      email@flowbite.com
                    </p>
                  </div>
                  <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                    $1842
                  </div>
                </div>
              </li>
              <li class="py-3 sm:py-4">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <img class="w-8 h-8 rounded-full" src="/images/users/lana-byrd.png" alt="Neil image">
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="font-medium text-gray-900 truncate dark:text-white">
                      Lana Byrd
                    </p>
                    <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                      email@flowbite.com
                    </p>
                  </div>
                  <div class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                    $1044
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <!-- Card Footer -->
        <div class="flex items-center justify-between pt-3 mt-5 border-t border-gray-200 sm:pt-6 dark:border-gray-700">
          
        </div>
      </div>
    </div>
  </div>

</main></template>