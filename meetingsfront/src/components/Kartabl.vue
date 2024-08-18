<script>
    import DropDown from './elements/DropDown.vue';
    import InputText from './elements/InputText.vue';
    import DateInput from './elements/DateInput.vue';
    import Radio from './elements/Radio.vue';
    import TableResults from './elements/TableKartabl.vue';
    import axios from 'axios';
    import { serverUrl } from '../../settings';
    import PersianDate from '@alireza-ab/persian-date';
    import Buttons from './elements/Buttons.vue';


    export default {
        data() {
          return {
            unsingnedProceedings: [],
            message: '',
            errorMessage: '',
            searchStart: false,
            searchResults: {},
            pre: '',
            next: '',
            offset: 0,
          }
        },
        components: {
            DropDown,
            //InputText,
            DateInput,
            Radio,
            TableResults,
            Buttons,
        },
        methods: {
            resetMessages(){
                this.message = '';
                this.errorMessage = '';
                this.showAlert = false;
            },
          
          getUnsignedProceeding(){
            axios.defaults.withCredentials = true;
            axios({
                method: 'get',
                url: serverUrl+"api/participants/?signed=f",
                headers: {"Content-Type": "application/json"},
                })
            .then(response => {
                this.unsingnedProceedings = response.data;
                })
            .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
        },  
        created(){
            this.resetMessages();
            this.getUnsignedProceeding();
         },
        computed: {
            
        }
    }
</script>

<template>
    <div> 
        <span class="block-inline text-lg hover:text-blue-500 p-2 border-2 bg-red-100"> کارتابل </span>
        <div class="flex flex-col  font-farsi items-stretch items-center">
            <div>
                <div class="flex flex-col w-full items-center">
                    <TableResults class="mt-5" :rows="unsingnedProceedings" :offset="offset"/>
                </div>
                <div class="flex flex-row items-center my-7">
                    <!-- Previous Button -->
                    <button v-if="next"  type="button" @click="getNext" class="inline-flex items-center py-2 px-4 mr-3 text-sm font-medium text-gray-500 bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        <svg class="mr-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd"></path></svg>
                        بعدی    
                    </button>
                    <button v-if="pre"  type="button" @click="getPre" class="inline-flex items-center py-2 px-4 text-sm font-medium text-gray-500 bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        قبلی    
                        <svg class="ml-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>