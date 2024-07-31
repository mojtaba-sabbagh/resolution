<script setup>
    const props = defineProps(['isLoggin'])
</script>

<template>
    <div> 
        <img class="w-full opacity-40" src="images/Uni-Gallery-img1.jpg"/>
        <div v-if="!isLoggin" class="flex flex-row items-end justify-center w-full md:w-1/4">  
            <button class="block-inline flex justify-center hover:bg-red-100 hover:border hover:border-1 p-1"
                title="ورود" :row="i" :name="members[i].id" @click="saveMember">
                <img class="w-7 opacity-60" src="images/ok.png"/>
            </button>
        </div>
    </div>
</template>

<style scoped>
.bg-image {
    background-image: url("images/Uni-Gallery-img1.jpg");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    }

</style>