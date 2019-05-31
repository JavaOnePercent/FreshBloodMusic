<template>
<div>
    <div class="RadioConteiner">
        <img title="Радио" src="/static/mainapp/images/radio.svg">
    </div>
    <div v-if="showRadio" class="RadioWave-cont">
        <div class="row">
            <div v-if="showTips && history.length>0 && tips.length === 0 " class="RadioWave">
                <!--Сюда вставить радио волны -->
            </div>
        </div>
    </div>
</div>

</template>

<script>
export default {
    name: 'radio',
    data() {
        return {
            showRadio: true
        }
    },
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
    left: 245px;
    transform: translateX(0%);
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
    max-height: 200px;
    top: 55px;
    /* position: absolute; */
    /* min-width: 100%; */
    width: auto;
    max-width: 500px;
    z-index: 1;
}
</style>