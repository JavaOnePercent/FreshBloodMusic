<template>
  <div class="main" id="main">
        <div class="topics-conteiner">
            <div class="topics"> 
                <music-top></music-top>
                <performer-top></performer-top>
            </div>
        </div>
            <compilation-top></compilation-top>
        <footer>
            ©Отвратительные мужики
        </footer>
    </div>
</template>

<script>
import compilationTop from './Main/CompilationTop.vue'
import performerTop from './Main/PerformerTop.vue'
import musicTop from './Main/MusicTop.vue'

export default {
    name: 'main-compilation',
    components: {
        compilationTop,
        performerTop,
        musicTop
    },
    data() {
	    return {
            message: 'сообщение',
            hoverClass: 'disk'
        }
    },
    methods: {

    }
}
</script>

<style scoped>
.main
{
    top:55px;
    position: relative;
}
/*панель топов*/
.topics-conteiner
{
    box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    -webkit-box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    -moz-box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    background-color: rgb(55, 55, 55);
    top: 0px;
    left: 0px;
    height: 350px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    justify-content: center;
}
.topics
{
    height: 350px;
    padding-left: 15px;
    padding-right: 15px;
    box-sizing: border-box;
    margin: 0 auto;
    max-width: 1143px; 
    min-width: 915px; 
}
/*подвал*/
footer
{
    position: relative;
    display: block;
    margin: 0 auto 69px auto;
    text-align: center;
}
a
{
    text-decoration: none;
}

a:active {color: black;}

a:visited {color: black;}
</style>