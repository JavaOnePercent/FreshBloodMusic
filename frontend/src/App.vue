<template>
    <div id="app">
        <header-container></header-container>
        <div v-if="showLoader" class="modal" id="myModal" >
            <div class="modal-content">
                <loader></loader>
            </div>
        </div>
        <router-view></router-view>
        <top-player></top-player>
    </div>
</template>

<script>
import headerContainer from './components/Header.vue'
import profile from './components/Profile.vue'
import settings from './components/Settings.vue'
import mainCompilation from './components/Main.vue'
import loader from './components/Loader.vue'
import topPlayer from './components/TopPlayer.vue'

export default {
    name: 'app',
    components: {
        headerContainer,
        profile,
        settings,
        mainCompilation,
        loader,
        topPlayer
    },
    created() {
        var self = this
        this.$http.get('login').then(function(response){
            self.$store.commit("username", response.data.username)
        });
    },
    computed: {
        showLoader () {
            return this.$store.state.showLoader
        }
    },
}
</script>

<style>
html, body
{
    /*font-family:"Rex Bold";*/
    display: inline-block;
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    font-family: Arial,Helvetica,sans-serif;
    position: fixed;
    overflow-y: scroll;
    overflow-x: hidden;
}
html {
    overflow: hidden;
}
 .modal
 {
    pointer-events: all;
    position: fixed;
    z-index: 90000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.8);
    overflow: -moz-scrollbars-none; 
    -ms-overflow-style: none; 
 }
 .modal-content
 {
    margin: 0 auto 100px auto;
 }
.modal::-webkit-scrollbar {
    display: none;
}
</style>
