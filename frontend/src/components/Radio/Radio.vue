<template >
<div v-outside="changeShowRadio">
    <div  class="RadioConteiner" @click="showRadio = !showRadio">
        <img title="Радио" src="/static/mainapp/images/radio.svg">
    </div>
    <div  v-if="showRadio" class="RadioWave-cont">
        <div class="row">
            <h3 style="width:200px; margin: 5px; height: 40px"> Радио волны </h3>
            <vue-custom-scrollbar id='father' v-if="showRadio" class="RadioWave"  :settings="settings">
                    <div class="wave">
                        <span>
                            Специально для вас
                        </span>
                    </div>
                    <!--Сюда вставить радио волны -->
                    <div class="wave" :key="index" v-for="(gener, index) in geners">
                        <span>
                            {{gener.name_gnr}}
                        </span>
                    </div>
            </vue-custom-scrollbar>
        </div>
    </div>
</div>

</template>

<script>
import vueCustomScrollbar from 'vue-custom-scrollbar'
export default {
    name: 'radio',
    data() {
        return {
            showRadio: false,
            geners: [],
            settings: {
                maxScrollbarLength: 60,
                wheelPropagation: true,
                wheelSpeed: 0.2,
            },
        }
    },
    components: {
        vueCustomScrollbar
    },
    directives: {
        outside: {
            bind(el, binding) {
                el.addEventListener('click', e => e.stopPropagation());
                document.body.addEventListener('click', binding.value);
            },
            unbind(el, binding) {
                document.body.removeEventListener('click', binding.value);
            }
        }
    },
    created: function() {
        this.getGeners()
    },
    methods: {
        changeShowRadio() {
            this.showRadio = false
        },
        getGeners() {
            this.$http.get('../api/genre').then(function(response){
                console.log(response.data)
                this.geners = response.data
            });
        },
    }
}
</script>

<style scoped>
    .RadioConteiner
    {
        width: 55px;
        height: 55px;
        display: inline-block;
        position: relative;
    }
    .RadioConteiner img
    {
        width: 25px;
        height: auto;
        margin: auto;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
    }
    .RadioConteiner
    {
        border-radius: 25px;
        cursor: pointer;
    }
    .RadioConteiner:after {
    display: block;
    position: absolute;
    margin: 0;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    content: '.';
    color: transparent;
    width: 1px;
    height: 1px;
    border-radius: 50%;
    background: transparent;
    }
    .RadioConteiner:hover:after {
        -webkit-animation: circle .3s ease-in forwards;
    }
    @-webkit-keyframes circle {
    0% {
            width: 1px;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            margin: auto;
            height: 1px;
            z-index: -1;
            background: #eee;
            border-radius: 100%;
        }
    100% {
            background: rgba(170, 170, 170, 0.2);
            height: 45px;
            width: 45px;
            z-index: -1;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            margin: auto;
            border-radius: 35px;
        }
    } 
@supports not ( -webkit-animation: circle .3s ease-in forwards) {
    .uploud-cont:hover{
        background-color: rgba(204, 204, 204,0.3);
    }
}
.row
{
    position: relative;
    margin: auto;
    display: block;
    max-width: 1280px;
    min-width: 915px;
    /* left: 245px; */
    /* transform: translateX(0%); */
    /* right: 0;
    left: 0; */
}
.RadioWave-cont
{
    position: fixed;
    top: 55px;
    background-color:rgb(255, 255, 255);
    border-top: 1px solid rgb(204, 204, 204);
    width: 100%;
    height: auto;
    left: 0;
    box-shadow: 0 15px 15px -15px #333;
}
.RadioWave
{
    height: auto;
    position: relative;
    max-height: 600px;
    /* min-width: 100%; */
    width: auto;
    /* max-width: 500px; */
    z-index: 1;
}
.RadioWave
{
    padding-top:15px;
    display: flex;
    flex-wrap: wrap;
}
.wave:last-child
{
    margin-right: 15px;
}
.wave
{
    width: 168px;
    /* line-height: 168px; */
    text-align: center;
    height: 168px;
    font-size: 19.5px;
    margin-bottom: 15px;
    margin-left: 15px;
    line-height: 25px;
    position: relative;
}
.wave 
{
    display: table;
    background-color: rgba(192,192,192,0.3);
}
.wave span 
{
    display: table-cell;
    vertical-align: middle;
}
.wave:hover{
    cursor: pointer;
    background-color: rgba(255, 181, 43, 0.3)
}
.scroll-area {
    margin: auto;
    width: 100%;
    height: 400px;
    height: 100%;
    height: calc(100% - 198px);
    background-color: white;
    top: 15px;
    position: relative;
    padding-top:3px; 
}
.current {
    cursor: default;
    background-color: rgba(255, 181, 43, 0.3)
}
</style>