<template>
    <div>
        <div :class="isFull ? 'full-volume-control-zone' : 'volume-control-zone'" @mouseleave="mouseLeave" :style="!isFull ? controlZoneStyle : ''">
            <transition>
                <div :class="isFull ? 'full-volume' : 'volume'" v-show="showVolume">
                    <div class="volume-background" v-show="showVolume"></div>
                    <vue-slider-component @drag-end="dragEnd" @drag-start="dragStart" v-model="value" :show="showVolume" ref="slider" v-bind="sliderprops"></vue-slider-component>
                </div>
            </transition>
            
            <img @mouseenter="openSpeaker" @click="clickSpeaker" :class="isFull ? 'full-speaker' : 'speaker'" :src="speakerPic" draggable="false"/>
        </div>
        
    </div>
</template>

<script>
import vueSliderComponent from './VueSliderComponent'

export default {
    name: 'volume-controller',
    components: {
        vueSliderComponent
    },
    props: ['isFull'],
    data() {
        var smallVolume = {direction: 'vertical', width: 12, height: 150, dotSize: 20, speed: 0.3, tooltip: 'hover'};
        //var fullVolume = {direction: 'horizontal', width: 180, height: 12, dotSize: 22, speed: 0.3, tooltip: 'hover'};
        var path = '/static/mainapp/images/';
        var speakerPics = {zero: path + 'speaker0.svg', thirty3: path + 'speaker33.svg', sixty6: path + 'speaker66.svg', hundred: path + 'speaker100.svg',};
        return {
            value: 100,
            showVolume: false,
            showFullVolume: false,
            sliderprops: smallVolume,
            //sliderpropsFull: fullVolume,
            dragging: false,
            mouseIn: false,
            speakerPic: speakerPics.hundred,
            speakerPics: speakerPics,
            controlZoneStyle: 'height: 59px;'
        }
    },
    watch: {
        value(value) {
            localStorage.setItem("volume", this.value);
            //this.$emit('volumechanged');
            this.$store.commit('volume', this.value);
            if(value === 0)
                this.speakerPic = this.speakerPics.zero;
            else if (value <= 33)
                this.speakerPic = this.speakerPics.thirty3;
            else if (value <= 66)
                this.speakerPic = this.speakerPics.sixty6;
            else
                this.speakerPic = this.speakerPics.hundred;
        },
        isFull() {
            this.refreshFunc()
        }
    },
    created() {
        var vol = localStorage.getItem("volume");
        if(vol)
            this.value = Number(vol);
    },
    methods: {
        clickSpeaker() {
            if(this.value > 0)
            {
                sessionStorage.setItem("volume", this.value);
                this.value = 0;
            }
            else 
            {
                var vol = Number(sessionStorage.getItem("volume"));
                if(vol !== 0)
                    this.value = vol;
                else
                    this.value = 100;
            }
        },
        refreshFunc() {
            this.$refs.slider.refresh();
        },
        mouseLeave() {
            this.mouseIn = false;
            this.closeSpeaker();
        },
        mouseEnter() {
            this.mouseIn = true;
        },
        dragEnd() {
            this.dragging = false;
            this.closeSpeaker();
        },
        dragStart() {
            this.dragging = true;
        },
        openSpeaker() {
            this.controlZoneStyle = '';
            this.showVolume = true;
            this.mouseIn = true;
            
        },
        closeSpeaker() {
            if(!this.dragging && !this.mouseIn)
            {
                this.showVolume = false;
                this.controlZoneStyle = 'height: 59px;';
            }
        }
    }
}
</script>

<style scoped>

.volume-background {
    margin: auto;
	position: absolute;
    height: 160px;
    width: 50px;
    left: -8px;
    bottom: 1px;
    background: rgba(245, 245, 245, 0.95);/*#323232;*/
    box-shadow:  0 -2px 4px rgba(0, 0, 0, .1), /*тут бы поиграть с тенями*/
    -23px 0 20px -23px rgba(0, 0, 0, .5),
    23px 0 20px -23px rgba(0, 0, 0, .5),
    0 0 40px rgba(0, 0, 0, .1) inset;
}

.full-speaker {
    width: 40px;
    height: 40px;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
	position: absolute;
    cursor: pointer;
}

.full-speaker:hover {
    width: 42px;
    height: 42px;
    bottom: -1px;
}

.speaker {
    width: 30px;
    height: 30px;
    right: 0px;
    left: 0;
    padding: 0;
    position: absolute;
    bottom: 18px;
    margin: auto;
    line-height: 0;
    cursor: pointer;
    z-index: 25;
}

.speaker:hover {
	width: 32px;
	height: 32px;
    bottom: 17px;
}

.full-volume {
    margin: auto;
	position: absolute;
    height: 155px;
    width: 34px;
    right: 0;
    left: 0;
    bottom:55px;
}

.volume {
    margin: auto;
	position: absolute;
    height: 155px;
    width: 34px;
    right: 0;
    left: 0;
    bottom:75px;
}

.full-volume-control-zone {
    height: 210px;
    width: 60px;
    top: 287px;
    right: -85px;
    margin: auto;
	position: absolute;
}

.volume-control-zone {
    margin: auto;
	position: absolute;
    right: 75px;
    bottom: 0;
    width: 60px;
    height: 236px;
    z-index: 20;
}

</style>