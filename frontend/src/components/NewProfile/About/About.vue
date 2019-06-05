<template>
    <div class="aboutConteiner">
        <div class="about"> 
            <img :src="logo" alt="аватарка" class="ProfileImg" />
            <div style="height: auto;" >
                <h1 style="margin:0">
                    <span class="name"> {{name}} </span>
                </h1>
                <br>
                <span class="description"> {{description}} </span>
            </div>
        </div>

        <div class="controll">
            <router-link class="controll-btn" to="/settings" v-if="this.$route.params.id == this.$store.state.myPerformerID">
                <div > Настройки </div>
            </router-link>
            <router-link class="controll-btn" to="/statistic" v-if="this.$route.params.id == this.$store.state.myPerformerID">
                <div > Статистика </div>
            </router-link>
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