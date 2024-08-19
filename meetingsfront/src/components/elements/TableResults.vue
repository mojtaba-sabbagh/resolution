<script>
import Buttons from './Buttons.vue';
import axios from 'axios';
import { serverUrl } from '../../../settings';
    export default {
        components: { Buttons },

        props: {
            rows: null,
            offset: 0,
        },
        methods:{
            downloadFile(downloadUrl) {
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', 'proceeding.pdf');
                document.body.appendChild(link);
                link.click();
                link.remove();
            },
            downloadAttachProc(url){
                axios({
                    method: 'get',
                    url: serverUrl+`api/downloadproc/${url}/`,
                    headers: {"Content-Type": "application/json"},
                    responseType: 'blob',
                    })
                .then(response => {
                    const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
                    this.downloadFile(downloadUrl)
                })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
            },
            printProceeding(proceedingId) {
                axios({
                    method: 'get',
                    url: serverUrl+`api/printproc/${proceedingId}/`,
                    headers: {"Content-Type": "application/json"},
                    responseType: 'blob',
                    })
                .then(response => {
                    const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
                    this.downloadFile(downloadUrl)
                })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
            },
        },
    }
</script>

<template>
    <div dir="rtl" class="text-xs md:text-lg font-farsi sm:-mx-6 lg:-mx-8">
        <div class="py-2 sm:px-2 lg:px-4">
            <div class="">
              <table class="table-fixed border max-w-5xl">
                <thead class="bg-white border-b">
                    <tr>
                    <th scope="col" class="hidden md:table-cell text-sm font-medium text-gray-900 px-6 py-4 text-right" width="5%">
                        #
                    </th>
                    <th scope="col" class="text-sm font-medium font-bold text-gray-900 px-6 py-4 text-right">
                        جلسه
                    </th>
                    <th scope="col" class="hidden md:table-cell text-sm font-medium font-bold text-gray-900 px-6 py-4 text-right">
                        شماره‌صورتجلسه
                    </th>
                    <th scope="col" class="text-sm font-medium font-bold text-gray-900 px-6 py-4 text-right">
                        تاریخ‌صورتجلسه                   
                    </th>
                    <th scope="col" class="hidden md:table-cell text-sm font-medium font-bold text-gray-900 px-6 py-4 text-center">
                        متن مصوبه
                    </th>
                     <th scope="col" class="text-sm font-medium font-bold text-gray-900 px-6 py-4 text-center">
                       نوع ذینفع
                    </th>
                    <th scope="col" class="hidden md:table-cell text-sm font-medium font-bold text-gray-900 px-6 py-4 text-center">
                       شماره ذینفع
                    </th>
                     <th scope="col" class="hidden md:table-cell text-sm font-medium font-bold text-gray-900 px-6 py-4 text-center">
                        نام ذینفع
                    </th>
                    <th scope="col" class="hidden md:table-cell text-sm font-medium font-bold text-gray-900 px-6 py-4 text-center">
                        دانلود
                    </th>

                    </tr>
                </thead>
                <tbody>
                    <tr class="bg-gray-100 border-b
                                hover:text-gray-900 hover:ring-1 mb-20" 
                        v-for="(row, index) in rows" :key="index">
                        <td class="hidden md:table-cell px-6 py-4 text-sm font-medium text-gray-800">{{ index+offset+1 }}</td>
                        <td class="text-sm text-gray-800 font-light px-6 py-4">
                            {{ row.meeting }}
                        </td>
                        <td class="hidden md:table-cell text-sm text-gray-800 font-light px-6 py-4">
                            {{ row.proceeding_no }}
                        </td>
                        <td class="hidden md:table-cell text-sm text-gray-800 font-light px-6 py-4">
                            {{ row.proceedingdate }}
                        </td>
                        <td class="text-sm text-gray-800 font-light px-6 py-4">
                            {{ row.act_text }}
                        </td>
                        <td class="hidden md:table-cell text-sm text-gray-800 font-light px-6 py-4 break-word">
                            {{ row.stockholder_type }}
                        </td>
                        <td class="hidden md:table-cell text-sm text-gray-800 font-light px-6 py-4">
                           {{ row.zinaf }}
                        </td>
                        <td class="hidden md:table-cell text-sm text-gray-800 font-light px-6 py-4">
                           {{ row.fullname }}
                        </td>
                        <td class="hidden md:table-cell text-sm text-gray-800 font-light px-6 py-4">
                            <button class="block-inline disabled:bg-gray-100" title="دانلود صورتجلسه الکترونیکی"  name="1"
                                    @click="printProceeding(row.id)">
                                    <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/print.png"/>
                            </button>
                            <button class="block-inline disabled:bg-gray-100" title="دانلود پیوست صورتجلسه"  name="2"
                                    @click="downloadAttachProc(row.upload)" :disabled="!row.upload">
                                    <img v-show="row.upload" class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/electronic-proc.png"/>
                                    <img v-show="!row.upload" class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/not-exist.png"/>
                            </button>
                        </td>
                    </tr>
                </tbody>
                </table>
            </div>
        </div>
    </div>
</template>>

<style>
</style>