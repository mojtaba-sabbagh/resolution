<script>
    import DropDown from './elements/DropDown.vue';
    import InputText from './elements/InputText.vue';
    import DateInput from './elements/DateInput.vue';
    import TimeInput from './elements/TimeInput.vue';
    import Toggle from './elements/Toggle.vue';
    import axios from 'axios';
    import { serverUrl } from '../../settings';
    import PersianDate from '@alireza-ab/persian-date';
    import Confirm from './elements/Confirm.vue';
    import FileUpload from './elements/FileUpload.vue';

    export default {
        data() {
          return {
            meetingNamesOptions: Object,
            proceedingNameOptions: Object,
            proceedingData: Object,
            employeeOptions: {},
            participants: [],
            meetingId: 0,
            proceedingId: 0,
            proceedingNo: 0,
            pDate:'',
            pTime: "", //{'HH':'10', 'mm':'00'},
            loc:'',
            meetingName: '',
            proceedingName: '',
            manipulationMode: 0,
            showForm: false,
            showAlert: false,
            message: '',
            buttonLabel: 'تایید',
            preadonly: false,
            errorMessage: '',
            fileName: '',
            fileUploaded: false,
            proceedingLink: '',
          }
        },
        components: {
            DropDown,
            InputText,
            DateInput,
            Toggle,
            Confirm,
            TimeInput,
            FileUpload,
        },
        methods: {
            resetMessages(){
                this.message = '';
                this.errorMessage = '';
                this.showAlert = false;
            },
            meetingsName(){
             axios({
                    method: 'get',
                    url: serverUrl+'api/meetings/',
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.meetingNamesOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          employeesName(meetingId){
             axios({
                    method: 'get',
                    url: serverUrl+'api/employees/?meetingid='+meetingId,
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.employeeOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          onMeetinChange(meetingId){
            this.getProceedings(meetingId)
            this.blankForm();
          },
          getProceedingAPI(proceedingId){
             axios({
                    method: 'get',
                    url: serverUrl+`api/proceedings/${proceedingId}/`,
                    headers: {"Content-Type": "application/json"},
                    //credentials: 'include',
                    })
                .then(response => {
                    this.fillproceedingForm(response.data);
                    this.buttonLabel = 'بروزرسانی صورتجلسه';
                    this.manipulationMode = 1;
                    this.showForm = true;
                })
                .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          findOptionsText(optionsNames, optionId){
            var name = '';
            optionsNames.forEach(element => {
                if (element.ID == optionId){
                    name = element.text;
                }
            });
            return name;
          },
          getProceedings(meetingId){
            //this.blankForm();
            this.meetingName = this.findOptionsText(this.meetingNamesOptions, meetingId);
            axios({
                    method: 'get',
                    url: serverUrl+'api/proceedings/?meetingid='+meetingId,
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.proceedingNameOptions = response.data;
                    this.meetingId = meetingId;
                    this.employeesName(this.meetingId);

                })
                .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          addProceedingAPI(){
            if (this.manipulationMode == 0){
                axios.post(serverUrl+'api/proceedings/', {'proceeding_no':this.proceedingNo, 'pdate':this.toGregorianDate(this.pDate),
                            'ptime':this.pTime, 'loc':this.loc, 'readonly':this.preadonly, 'meeting':this.meetingId, 
                            'participants':this.participants, 'upload':this.fileName}) //`${this.pTime.HH}:${this.pTime.mm}`
                    .then(response => {
                        //this.blankForm();
                        this.getProceedings(this.meetingId);
                        this.$toast.success('تغییرات ذخیره شد.');
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطایی در ذخیره تغییرات اتفاق افتاد.');
                    });
            }
            else {
                axios.put(serverUrl+'api/proceedings/'+this.proceedingId+'/',{'proceeding_no':this.proceedingNo, 
                            'loc':this.loc, 'readonly':this.preadonly, 'meeting':this.meetingId, 
                            'pdate': this.toGregorianDate(this.pDate), 'ptime': this.pTime, 
                            'participants':this.participants, 'upload':this.fileName}) //`${this.pTime.HH}:${this.pTime.mm}`
                    .then(response => {
                        this.getProceedings(this.meetingId);
                        this.$toast.success('تغییرات ذخیره شد.');
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطایی در ذخیره تغییرات اتفاق افتاد.');
                    });   
            }
          },
          getProceeding(newValue){
            this.proceedingName = this.findOptionsText(this.proceedingNameOptions, newValue);
            if (newValue && newValue != 0){
                this.getProceedingAPI(newValue);
            }
            else {
              this.proceedingId = 0;
              this.showForm = false;
              this.blankForm();
            }
          },
          fillproceedingForm(proceedingData){
            this.proceedingNo = proceedingData.proceeding_no;
            this.pDate = this.toPersianDate(proceedingData.pdate);
            //let timeDetails = proceedingData.ptime.split(':');
            //this.pTime.HH = timeDetails[0];
            this.pTime = proceedingData.ptime;//.mm = timeDetails[1];
            this.loc = proceedingData.loc;
            this.preadonly = proceedingData.readonly;
            this.participants = proceedingData.participants;
            this.proceedingId = proceedingData.id;

            if (proceedingData.upload){
                this.fileName = proceedingData.upload.trim()
                if (this.fileName != ''){
                    this.fileUploaded = true;
                    this.proceedingLink = this.createLink(this.fileName);
                }
            }
            this.resetMessages();
          },
          updateNo(newValue){
           this.proceedingNo = newValue; 
          },
          updatePDate(newValue){
           this.pDate = newValue; 
          },
          updatePTime(newValue){
           //this.pTime.HH = newValue.HH;
           //this.pTime.mm = newValue.mm;
           this.pTime = newValue;
          },
          updateLoc(newValue){
            this.loc = newValue;
          },
          updateReadonly(newValue){
            this.preadonly = newValue;
            if (newValue) { this.addProceedingAPI() };
          },
          updateParticipant(newValue, row){
            this.participants[row] = newValue;
          },
          blankForm(){
            this.participants = [];
            this.proceedingNo = '';
            const today = new Date();
            this.pDate = this.toPersianDate(today.toDateString());
            this.pTime = {'HH':'10', 'mm':'00'};
            this.buttonLabel = 'ایجاد صورتجلسه';
            this.loc = '';
            this.preadonly = false;
            this.showForm = true;
            this.manipulationMode = 0;
            this.proceedingId = 0;
            this.fileUploaded = false;
            this.fileName = '';
            this.proceedingLink = '';
            this.resetMessages();
          },
          deleteMeeting(){
            axios.delete(serverUrl+'api/proceedings/'+this.proceedingId+'/')
            .then(response => {
                this.getProceedings(this.meetingId);
                this.blankForm();
                })
            .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                });
          },
          addParticipant(){
            this.participants.push(0);
          },
          checkParticipants(){
            if (this.participants.length == 0){
                return false;
            }
            for(const m of this.participants) {
                if (m == 0){
                    return false;
                }
            }
            return true;
          },
          addParticipants(){
            for(const element of this.employeeOptions) {
                this.participants.push(element.ID);
            };
          },
          deleteParticipant(event){
            let row = parseInt(event.currentTarget.getAttribute('row'));            
            this.participants.splice(row, 1);
          },
          showAlertFunc(message){
            this.message = message;
            this.showAlert = true;
            let delayInMilliseconds=2000;
            setTimeout(() => {
                this.showAlert = false;
            }, delayInMilliseconds);
          },
          toPersianDate(gdate){
                let p = new PersianDate(gdate, 'gregorian');
                return p.calendar('jalali').toString('?YYYY/?MM/?DD');
            },
          toGregorianDate(newValue) { 
                let p = new PersianDate(newValue, 'jalali');
                return p.calendar('gregorian').toString('?YYYY-?MM-?DD');
            },
        createLink(fileName){
            return `${serverUrl}api/downloadproc/${fileName}/`;
        },
        onFileChange(e) {
            const file = e.target.files[0]
            let fileExtention = file.name.split(".").pop();
            let filename = this.proceedingId+`.${fileExtention}`; 
            let foldername = this.meetingId
            const formData = new FormData();
            formData.append("file", e.target.files[0]);
            this.fileName = `${foldername}/${filename}`;
            axios
                .post(serverUrl+`api/procupload/${this.proceedingId}/`, formData,
                {
                    headers: {
                    'Content-Type': "image/jpeg;charset=UTF-8",
                    'Content-Disposition': `file; filename=${filename}`
                    }
                })
                .then(() => {
                 this.fileUploaded = true;
                 this.proceedingLink = this.createLink(this.fileName);
                 this.$toast.success('فایل صورتجلسه با موفقیت بارگذاری شد. بروزرسانی انجام شود.');
                })
                .catch((error) => {
                    this.$toast.error('خطایی در بارگذاری فایل صورتجلسه اتفاق افتاد.');
                    this.errorMessage = error;
                    this.fileUploaded = false;
                });
        },
        downloadProceeding(link){
            let filename = 'file';
            if (link != ''){
                let linkParts = link.split('/');
                filename = linkParts[linkParts.length-1];
            }
            if (this.fileName != ''){
                filename = this.fileName;
            }
            axios({
                    url: link, //your url
                    method: 'GET',
                    responseType: 'blob', // important
                })
                .then((response) => {
                    // create file link in browser's memory
                    const href = URL.createObjectURL(response.data);

                    // create "a" HTML element with href to file & click
                    const link = document.createElement('a');
                    link.href = href;
                    link.setAttribute('download', filename); //or any other extension
                    document.body.appendChild(link);
                    link.click();

                    // clean up "a" element & remove ObjectURL
                    document.body.removeChild(link);
                    URL.revokeObjectURL(href);
                });
        },
        deleteFileProceeding(){
            axios.delete(serverUrl+`api/procupload/${this.proceedingId}/`)
                .then((response) => {
                    this.fileUploaded = false;
                    this.proceedingLink = '';
                    this.$toast.success('پیوست صورتجلسه با موفقیت حذف شد.');
                })
                .catch(() => {
                    this.$toast.error('خطایی در حذف پیوست صورتجلسه اتفاق افتاد.');
                    this.fileUploaded = true;
                });
        },
        downloadFile() {
                const link = document.createElement('a');
                link.href = this.proceedingPDF;
                link.setAttribute('download', 'proceeding.pdf');
                document.body.appendChild(link);
                link.click();
                link.remove();
            },
        printProceeding() {
                axios({
                    method: 'get',
                    url: serverUrl+`api/printproc/${this.proceedingId}/`,
                    headers: {"Content-Type": "application/json"},
                    responseType: 'blob',
                    })
                .then(response => {
                    const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
                    this.proceedingPDF = downloadUrl;
                    this.downloadFile()
                })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
            },
        },
        created(){
          axios.defaults.withCredentials = true;
          this.meetingsName();
        },
        computed: {
            isDisabled() {
                // evaluate whatever you need to determine disabled here...
                if (this.proceedingNo == '' || this.pDate == '' || !this.checkParticipants() || this.preadonly)
                    return true;
                return false;
             },
        }
    }
</script>

<template>
    <div> 
        <span class="block-inline text-lg hover:text-blue-500 p-2 border-2 bg-red-100"> مدیریت صورتجلسه </span>
        <div class="flex flex-col font-farsi items-stretch items-center">
            <div class="flex flex-col md:flex-row items-end">
                <DropDown class="mt-5 md:mt-10 mx-5 w-4/5 md:w-2/5" label_title="جلسات موجود"  @onChangeValue="onMeetinChange"
                    :options="meetingNamesOptions" v-model:itemSelected="meetingId"/>
                <DropDown v-if="meetingId" class="mt-3 md:mt-10 mx-5 w-4/5 md:w-2/5" label_title="صورتجلسات موجود"  @onChangeValue="getProceeding"
                    :options="proceedingNameOptions" :itemSelected="proceedingId"/>
                <div v-if="meetingId" class="flex flex-row gap-4 justify-center mt-3 w-full md:w-1/5">
                    <button class="block-inline flex items-end" @click="blankForm">
                        <img class="opacity-60 hover:bg-red-100 w-8 p-1 mb-1" title="اضافه کردن صورتجلسه" src="images/plus.png"/>
                    </button>
                    <button class="block-inline flex justify-center hover:bg-red-100 p-1 mb-1" @click="deleteMeeting" :disabled="meetingId == 0">
                        <img class="w-6 opacity-60" title="حذف صورتجلسه" src="images/minus.png"/>
                    </button>
                </div>
            </div>
            <div v-if="showForm && meetingId">
                <div class="border border-gray-500 mt-5 pb-5 mx-5">
                    <form v-on:submit.prevent="">
                        <div class="md:flex md:flex-row gap-4 mt-5 items-center">
                            <InputText  class="w-5/6 mx-4" :value="proceedingNo" :disabled="preadonly"
                                @onChangeValue="updateNo" label_title="شماره صورتجلسه" input_placeholder="شماره صورتجلسه" />
                            <DateInput class="w-5/6 mx-4" label_title="تاریخ صورتجلسه"  :dateValue="pDate" 
                                 l2r @onChangeValue="updatePDate" :disabled="preadonly" />
                            <TimeInput class="w-5/6 mx-4" label_title="ساعت صورتجلسه"  :timeValue="pTime" 
                                 l2r @onChangeValue="updatePTime" :disabled="preadonly" />
                            <InputText  class="w-5/6 mx-4" :value="loc" :disabled="preadonly"
                                @onChangeValue="updateLoc" label_title="مکان جلسه" input_placeholder="سال هنری" />
                            
                            <!--Toggle v-model:value="preadonly"  @onChangeValue="updateReadonly" class="w-5/6 md:w-1/4" 
                                    l2r label_title="جلسه غیر قابل تغییر" :disabled="preadonly" @click="showModal" /-->
                        </div>
                        <div class="flex items-center mt-4">
                            <span class="block-inline float-right text-green-800 text-sm hover:text-blue-500 p-2">شرکت کنندگان: </span>
                            <button v-if="!proceedingId" class="block-inline flex items-end justify-right" 
                                    title="افزودن همه اعضا" @click="addParticipants" :disabled="preadonly">
                                <img class="opacity-60 hover:bg-red-100 w-8 p-1" src="images/addall.png"/>
                            </button>
                        </div>
                        <div class="flex flex-col items-center pb-5 mx-5 border border-gray-500">
                            <div class="w-full md:flex md:gap-6 justify-center mt-2 px-2" v-for="(member, i) in participants">
                                <DropDown class="w-full md:w-2/5 md:float-right" label_title="نام شرکت کننده"  v-model:itemSelected="participants[i]" 
                                        :options="employeeOptions" @onChangeValue="updateParticipant" :row="i" :disabled="preadonly" showLabel="false"/>
                                <div class="flex flex-row items-end justify-center w-full md:w-1/4">  
                                    <button class="block-inline flex justify-center hover:bg-red-100 p-1" title="حذف شرکت کننده" 
                                        :row="i" :name="participants[i]" @click="deleteParticipant" :disabled="preadonly">
                                        <img class="w-7 opacity-60" src="images/minus.png"/>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="flex flex-col items-center mt-5">
                            <button class="block-inline flex items-end justify-right" title="افزودن شرکت کننده" 
                                    @click="addParticipant" :disabled="preadonly">
                                <img class="opacity-60 hover:bg-red-100 w-8 p-1" src="images/plus.png"/>
                            </button>
                        </div>
                        <button type="submit" @click="addProceedingAPI" class="hover:bg-red-100 mt-7 md:mt-10 w-4/5 md:w-1/2 appearance-none border text-sm text-center rounded-lg p-2.5
                            bg-red-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 
                            focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400 disabled:bg-slate-50 disabled:text-slate-300" :disabled="isDisabled"> 
                            <span> {{ buttonLabel }} </span>
                        </button>
                    </form>
                        
                        <div class="mt-5 flex flex-col md:flex-row items-center md:justify-center">
                            <label class="ml-5 md:mr-4  bg-white text-green-700 dark:text-green-500 
                             text-sm rounded-lg bg-white-50 border-gray-500 focus:ring-gray-500 focus:border-gray-500 disabled:bg-slate-50 disabled:text-slate-300" 
                                    for="myfile">
                                <img class="opacity-100 hover:bg-red-100 w-10 p-1" src="images/upload-proc.png" title="انتخاب فایل پیوست"/>
                                <input type="file" class=" hidden" id="myfile" name="myfile" @change="onFileChange" :disabled="preadonly" /> 
                            </label>
                            <button v-if="fileUploaded" class="inline-block mt-6 md:mt-0 ml-4
                                disabled:bg-slate-50 disabled:text-slate-300 text-sm rounded-lg" 
                                @click="downloadProceeding(proceedingLink)" >
                                <img class="opacity-100 w-10 hover:bg-red-100 p-1" src="images/electronic-proc.png" title="دانلود فایل پیوست"/> 
                            </button>
                            <button v-if="fileUploaded" class="inline-block mt-6 md:mt-0 ml-4 hover:bg-red-100
                                disabled:bg-slate-50 disabled:text-slate-300 text-sm rounded-lg" @click="deleteFileProceeding">
                                <img class="w-8 p-1" title="حذف فایل پیوست" src="images/delete-proc.png"/>
                            </button>
                            <button class="inline-block mt-6 md:mt-0 ml-4 hover:bg-red-100 p-1
                                disabled:bg-slate-50 disabled:text-slate-300 text-sm rounded-lg" @click="printProceeding">
                                <img class="w-8 opacity-50" title="چاپ صورتجلسه" src="images/print.png"/>
                            </button>
                            <button v-if="!preadonly" class="inline-block mt-6 md:mt-0 ml-4 hover:bg-red-100 p-1
                                disabled:bg-slate-50 disabled:text-slate-300 text-sm rounded-lg"
                                data-bs-toggle="modal" data-bs-target="#exampleModal" :disabled="isDisabled">
                                <img class="w-8 opacity-60" title="قفل صورتجلسه" src="images/lock.png"/>
                            </button>
                            <Confirm id="exampleModal" message="درصورت تایید دیگر مشخصات صورتجلسه و مصوبات آن قابل تغییر نخواهد بود، مطمئن هستید؟" 
                                     title="قفل کردن جلسه" @onYesButtonClick="updateReadonly" @onNoButtonClick="updateReadonly"/>
                        </div>
                        
                       
                    <p class="text-red-500 mt-2"> {{ errorMessage }} </p>
                </div>
                <!--button v-if="!preadonly" type="button" class="hover:bg-red-100 mt-14 w-4/5 md:w-1/2 appearance-none border text-sm text-center rounded-lg p-2.5
                            bg-red-200 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 
                            focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400 disabled:bg-slate-50 disabled:text-slate-300" 
                                data-bs-toggle="modal" data-bs-target="#exampleModal" :disabled="isDisabled">
                                قفل کردن جلسه
                </button>
                <Confirm id="exampleModal" message="درصورت تایید دیگر مشخصات صورتجلسه و مصوبات آن قابل تغییر نخواهد بود، مطمئن هستید؟" 
                                     title="قفل کردن جلسه" @onYesButtonClick="updateReadonly" @onNoButtonClick="updateReadonly"/-->
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>