<template>
  <div class="main" id="main">
        <div class="topics">
            <music-top></music-top>
            <performer-top></performer-top>
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
.topics
{
    background-color: rgb(85, 85, 85);
    top: 0px;
    left: 0px;
    height: 350px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    display: flex;
    justify-content: center;
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