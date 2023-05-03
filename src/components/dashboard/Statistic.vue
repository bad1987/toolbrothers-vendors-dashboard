<script setup>
import { statStore } from '../../stores/StatStore';
import { useLoaderStore } from '../../stores/statestore';
import { storeToRefs } from 'pinia';

const loaderStore = useLoaderStore() 

const { isLoading } = storeToRefs(loaderStore)

const _statstore = statStore()


</script>

<template>
    <div
          class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 sm:p-6 dark:bg-gray-800">
          <h3 class="flex items-center mb-4 text-lg font-semibold text-gray-900 dark:text-white">{{$t("static_month")}}
            <button data-popover-target="popover-description" data-popover-placement="bottom-end" type="button"><svg
                class="w-4 h-4 ml-2 text-gray-400 hover:text-gray-500" aria-hidden="true" fill="currentColor"
                viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
                  clip-rule="evenodd"></path>
              </svg></button>
          </h3>
          <div data-popover id="popover-description" role="tooltip"
            class="absolute z-10 invisible inline-block text-sm font-light text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 w-72 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400">
            <div class="p-3 space-y-2">
              <h3 class="font-semibold text-gray-900 dark:text-white">{{$t("statistics")}}</h3>
              <p>{{$t("notice_statistic")}}</p>
            </div>
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
              
          </div>
        </div>
        <!-- Card Footer -->
        <div class="flex items-center justify-between pt-3 mt-5 border-t border-gray-200 sm:pt-6 dark:border-gray-700">
          
        </div>
      </div>
</template>


<style scoped></style>