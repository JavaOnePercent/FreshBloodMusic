<template>
    <div class="aboutConteiner">
        <div class="about"> 
            <img :src="logo" alt="аватарка" class="ProfileImg" />
            <div style="height: auto;" >
                <span class="name"> {{name}} </span>
                <br>
                <span class="description"> {{description}} </span>
            </div>
        </div>

        <div class="controll">
            <div class="controll-btn"> Настройки </div>
            <div class="controll-btn"> Статистика </div>
            <div class="controll-btn"> Уведомления </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'about',
    props: ['logo', 'name', 'description'],
    data() {
        return {

        }
    },
}
</script>

<style scoped src="./About.css">

</style>