
<script>
    export default {
        props: {
            message:'',
            title: '',
        },
        methods:{
            yesClicked() {
                this.$emit('onYesButtonClick', true);
            },
            noClicked() {
                this.$emit('onNoButtonClick', false);
            },
        },
    }
</script>

<template>
    <div class="modal fade fixed top-0 left-0 hidden w-full h-full outline-none overflow-x-hidden overflow-y-auto"
        id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog relative w-auto pointer-events-none">
        <div
        class="modal-content border-none shadow-lg relative flex flex-col w-full pointer-events-auto bg-white bg-clip-padding rounded-md outline-none text-current">
        <div class="modal-header w-full flex flex-row items-center justify-between p-4 border-b border-gray-200 rounded-t-md">
            <h6 class="text-lg font-medium leading-normal text-gray-800" id="exampleModalLabel"> {{ title }} </h6>
            <button type="button"
            class="box-content w-4 h-4 p-1 text-black text-xl border-none rounded-none opacity-50 focus:shadow-none focus:outline-none focus:opacity-100 hover:text-black hover:opacity-75 hover:no-underline"
            data-bs-dismiss="modal" aria-label="Close"> X </button>
        </div>
        <div class="modal-body relative p-4">
            {{ message }}
        </div>
        <div class="modal-footer flex flex-shrink-0 flex-wrap gap-4 items-center justify-end p-4 border-t border-gray-200 rounded-b-md">
            <button type="button" class="px-6
                py-2.5
                bg-purple-600
                text-white
                font-medium
                text-lg
                leading-tight
                uppercase
                rounded
                shadow-md
                hover:bg-purple-700 hover:shadow-lg
                focus:bg-purple-700 focus:shadow-lg focus:outline-none focus:ring-0
                active:bg-purple-800 active:shadow-lg
                transition
                duration-150
                ease-in-out" data-bs-dismiss="modal" @click="noClicked">  خیر  </button>
            <button type="button" class="px-6
                py-2.5
                bg-blue-600
                text-white
                font-medium
                text-lg
                leading-tight
                uppercase
                rounded
                shadow-md
                hover:bg-blue-700 hover:shadow-lg
                focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0
                active:bg-blue-800 active:shadow-lg
                transition
                duration-150
                ease-in-out
                ml-1" data-bs-dismiss="modal" @click="yesClicked"> بله </button>
        </div>
        </div>
    </div>
    </div>    
</template>