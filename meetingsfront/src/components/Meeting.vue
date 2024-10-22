<script>
    import DropDown from './elements/DropDown.vue';
    import InputText from './elements/InputText.vue';
    import axios from 'axios';
    import { serverUrl } from '../../settings';
    export default {
        data() {
          return {
            meetingNamesOptions: Object,
            meetingData: Object,
            employeeOptions: {},
            members: [],
            meetingId: 0,
            meetingName: '',
            meetingPeriod: '0',
            manipulationMode: 0,
            showForm: false,
            showAlert: false,
            message: '',
            buttonLabel: 'تایید',
            periodOptions: [
                { "ID": "روزانه",
                  "text":"روزانه"
                },
                {"ID": "روزانه",
                  "text":"هفتگی"
                },
                {"ID": "دوهفتگی",
                  "text":"دوهفتگی"
                },
                {"ID": "ماهیانه",
                  "text":"ماهیانه"
                },
                {"ID": "غیرمشخص",
                  "text":"غیرمشخص"
                }
            ],
            roleOptions: [
                {"ID":"عضو", "text":"عضو"},
                {"ID":"دبیر", "text":"دبیر"},
            ],
            errorMessage: '',
          }
        },
        components: {
            DropDown,
            InputText,
        },
        methods: {
            isEmpty(obj) {
                for (const prop in obj) {
                    if (Object.hasOwn(obj, prop)) {
                        return false;
                    }
                }
                return true;
            },
            meetingsName(){
             axios.defaults.withCredentials = true;
             axios({
                    method: 'get',
                    url: serverUrl+'api/meetings/',
                    withCredentials: true,
                    }
                    )
                .then(response => {
                    this.meetingNamesOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          employeesName(){
             axios({
                    method: 'get',
                    url: serverUrl+'api/employees/',
                    headers: {
                        'Accept': '*/*',
                        'Content-Type': 'application/json',},
                    })
                .then(response => {
                    this.employeeOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          getMeetingAPI(meetingId){
             axios({
                    method: 'get',
                    url: serverUrl+'api/meetings/'+meetingId+'/',
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.fillMeetingForm(response.data);
                })
                .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          addMeetingAPI(){
            if (this.manipulationMode == 0){
                axios.post(serverUrl+'api/meetings/', {'meeting_name':this.meetingName, 
                                                       'period':this.meetingPeriod})
                    .then(response => {
                        this.blankForm();
                        this.meetingsName();
                        this.$toast.success('جلسه با موفقیت ذخیره گردید.');
                        this.errorMessage = '';
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در ذخیره اطلاعات رخ داد.');
                    });
            }
            else {
                axios.put(serverUrl+'api/meetings/'+this.meetingId+'/', {'meeting_name':this.meetingName, 'period':this.meetingPeriod})
                    .then(response => {
                        this.meetingsName();
                        this.$toast.success('جلسه با موفقیت ذخیره گردید.');
                        this.errorMessage = '';
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در ذخیره اطلاعات رخ داد.');
                    });   
            }
          },
          getMeeting(newValue){
            if (newValue && newValue != 0){
                this.meetingId = newValue;
                this.getMeetingAPI(newValue);
                this.buttonLabel = 'بروزرسانی جلسه';
                this.manipulationMode = 1;
                this.showForm = true;
            }
            else {
              this.meetingId = 0;
              this.blankForm();
            }
          },
          fillMeetingForm(meetingData){
            this.meetingName = meetingData.meeting_name;
            this.meetingPeriod = meetingData.period;
            this.members = meetingData.members;
          },
          updateName(newValue){
           this.meetingName = newValue; 
          },
          updatePeriod(newValue){
           this.meetingPeriod = newValue; 
          },
          updateRole(newValue, row){
            this.members[row].role = newValue;
          },
          updateMember(newValue, row){
            this.members[row].employee_id = newValue;
          },
          blankForm(){
            this.members = [];
            this.meetingName = '';
            this.meetingPeriod = '0';
            this.buttonLabel = 'ایجاد جلسه';
            this.manipulationMode = 0;
            this.showForm = true;
            this.meetingId = 0;
          },
          deleteMeeting(){
            axios.delete(serverUrl+'api/meetings/'+this.meetingId+'/')
            .then(response => {
                    this.meetingsName();
                    this.blankForm();
                    this.$toast.success('جلسه حذف گردید.');
                    this.errorMessage = '';
                })
            .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                });
          },
          addMember(){
            this.members.push({"role": "0", "employee_id":"0", "id":0});
          },
          deleteMember(event){
            let row = parseInt(event.currentTarget.getAttribute('row'));
            let memId = this.members[row].id;
            if (memId !=0 ){
                axios.delete(serverUrl+'api/members/'+memId+'/')
                .then(response => {
                    this.members.splice(row, 1);
                    this.$toast.success('عضو حذف گردید.');
                    this.errorMessage = '';
                    })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                    });
                }
          },
          showAlertFunc(message){
            this.message = message;
            this.showAlert = true;
            let delayInMilliseconds=2000;
            setTimeout(() => {
                this.showAlert = false;
            }, delayInMilliseconds);
          },
          saveAPI(memId, row) {
            // call apis
            if (memId !=0 ){
                axios.put(`${serverUrl}api/members/${memId}/`, {'employee':this.members[row].employee_id, 
                                                        'role':this.members[row].role, 'meeting':this.meetingId})
                .then(response => {
                    this.$toast.success('تغییرات ذخیره شد.');
                    this.errorMessage = '';
                    })
                .catch(error => {
                    this.errorMessage = error; 
                    this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                    console.log(memId, row);
                    });
                }
            else {
                axios.post(`${serverUrl}api/members/`, {'employee':this.members[row].employee_id, 
                                                        'role':this.members[row].role, 'meeting':this.meetingId})
                    .then(response => {
                        if (this.isEmpty(response.data)){
                            this.$toast.success('عضو تکراری است.');
                        }
                        else {
                            this.$toast.success('تغییرات ذخیره شد.');
                            this.errorMessage = '';
                        }
                    })
                    .catch(error => {
                        this.errorMessage = error;
                        this.$toast.error('اطلاعات عضو کامل نیست.');
                    });
            }
          },
          saveMember(event){
            let row = parseInt(event.currentTarget.getAttribute('row'));
            let memId = this.members[row].id;
            this.saveAPI(memId, row); 
          },
          saveAllMembers(){
           // this.members.forEach(function (member, row) {
           //     this.saveAPI(member.id, row);
           // });
            for (const [row, member] of this.members.entries()) {
                this.saveAPI(member.id, row);
                };
            },
        },
        created(){
          this.meetingsName();
          this.employeesName();
        },
        computed: {
            isDisabled() {
                // evaluate whatever you need to determine disabled here...
                if (this.meetingName == '' || this.meetingPeriod == '0')
                    return true;
                return false;
             },
        }
    }
</script>

<template>
    <div> 
        <span class="block-inline text-lg hover:text-blue-500 p-2 border-2 bg-red-100"> مدیریت جلسه </span>
        <div class="flex flex-col font-farsi items-center p-4 bg-gray-50">
    <!-- Header Section for Meeting Selection -->
    <div class="flex items-center justify-between w-full md:w-2/3 mb-8">
        <DropDown class="w-full md:w-4/5" label_title="جلسات موجود" @onChangeValue="getMeeting"
                  :options="meetingNamesOptions" :order=1 :itemSelected="meetingId"/>
        <div class="flex space-x-3">
            <!-- Add Meeting Button -->
            <button class="flex items-center justify-center hover:bg-green-100 p-2 rounded-full bg-gray-200" @click="blankForm">
                <img class="w-6" src="images/plus.png" title="اضافه کردن جلسه"/>
            </button>
            <!-- Delete Meeting Button -->
            <button class="flex items-center justify-center hover:bg-red-100 p-2 rounded-full bg-gray-200"
                    @click="deleteMeeting" :disabled="meetingId == 0">
                <img class="w-6" src="images/minus.png" title="حذف جلسه"/>
            </button>
        </div>
    </div>

    <!-- Form Section for Adding/Editing Meeting -->
    <div v-if="showForm" class="w-full md:w-2/3 p-5 bg-white rounded-lg shadow-lg">
        <form @submit.prevent="addMeetingAPI">
            <!-- Meeting Name and Period Selection -->
            <div class="md:flex md:gap-4 mb-4">
                <InputText class="w-full md:w-2/3" v-model:value="meetingName" @onChangeValue="updateName" 
                           label_title="نام جلسه" input_placeholder="نام جلسه"/>
                <DropDown class="w-full md:w-1/3" label_title="دوره" v-model="meetingPeriod" 
                            :options="periodOptions" @onChangeValue="updatePeriod" :order=2 />

            </div>
            <!-- Submit Button -->
            <button class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300" 
                    :disabled="isDisabled">
                <span> {{ buttonLabel }} </span>
            </button>
        </form>
        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-500 mt-2 text-center"> {{ errorMessage }} </p>
    </div>

    <!-- Members Section -->
    <div class="w-full md:w-2/3 mt-8">
        <div class="flex items-center justify-between mb-4">
            <span class="text-lg text-green-800">اعضاء جلسه:</span>
            <button class="hover:bg-green-100 p-2 rounded-full" @click="saveAllMembers">
                <img class="w-6" src="images/ok.png" title="ذخیره همه اعضا"/>
            </button>
        </div>

        <!-- Members List -->
        <div class="space-y-4">
            <div class="flex items-center space-x-4" v-for="(member, i) in members" :key="i">
                <!-- Member Name -->
                <DropDown class="w-full md:w-2/5" label_title="نام عضو" v-model:itemSelected="members[i].employee_id" 
                          :options="employeeOptions" @onChangeValue="updateMember" :row="i" :order=3 />
                <!-- Member Role -->
                <DropDown class="w-full md:w-2/5" label_title="نقش" v-model:itemSelected="members[i].role" 
                          :options="roleOptions" @onChangeValue="updateRole" :row="i" :order=4 />
                <!-- Delete and Save Buttons -->
                <div class="flex space-x-2">
                    <button class="hover:bg-red-100 p-2 rounded-full" @click="deleteMember(i)">
                        <img class="w-6" src="images/minus.png" title="حذف عضو"/>
                    </button>
                    <button class="hover:bg-green-100 p-2 rounded-full" @click="saveMember(i)">
                        <img class="w-6" src="images/ok.png" title="ذخیره عضو"/>
                    </button>
                </div>
            </div>
        </div>

        <!-- Add Member Button -->
        <div class="flex justify-center mt-4">
            <button class="hover:bg-blue-100 p-2 rounded-full" @click="addMember">
                <img class="w-6" src="images/plus.png" title="افزودن عضو"/>
            </button>
        </div>
    </div>

    <!-- Alert Section -->
    <div class="w-full md:w-2/3 mt-8">
        <div v-if="showAlert" class="bg-yellow-100 text-yellow-800 py-2 px-4 rounded-lg text-center">
            {{ message }}
        </div>
    </div>
</div>

    </div>
</template>

<style scoped>

</style>