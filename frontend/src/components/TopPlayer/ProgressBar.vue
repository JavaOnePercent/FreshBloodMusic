<template>
    <div :class="isFull ? 'full-vue-simple-progress' : 'vue-simple-progress'" >
        <vue-slider-component @drag-end="dragEnd" @drag-start="dragStart" @mouseup.native="click" v-model="currentTime" ref="slider" v-bind="sliderPropsComputed" :max="sliderMax"></vue-slider-component>
        <div v-if="!isFull" class="background-progress-bar" :style="bar_style + transition"></div>
        <!--<div v-show="isPlayerHovered" class="played-time">{{ '{{' }}playedTimeTop}}</div>
        <div v-show="isPlayerHovered || isFull" class="track-length">{{ '{{' }}trackLengthTop}}</div>-->
    </div>
</template>

<script>
import vueSliderComponent from './VueSliderComponent'

export default {
    name: 'progress-bar',
    components: {
        vueSliderComponent
    },
    props: [
        'isPlayerHovered',
        'isFull'
    ],
    data() {
        return {
            lastValue: 0,
            //duration: 0.0,
            sliderPropsFull: {
                width: 750,
                height: 20,
                'dot-height': 20,
                'dot-width': 25,
                min: 0,
                tooltip: 'always',
                //speed: 0.0,
                sliderStyle: {
                    //"backgroundColor": "rgba(0,0,0,0)",
                    'border-radius': 0,
                    //"box-shadow": '0 0 0 0',
                    //'visibility': 'invisible'
                },
                processStyle: {
                    //"border-radius": "30px 0 0 30px",
                    //"background-color": "rgb(200,200,200)"
                    "backgroundImage": "-webkit-linear-gradient(left, #ffd319 20%, #ff901f 40%, #ff2975 55%, #f222ff 80%, #8c1eff 90%)"
                },
                bgStyle: {
                    "background-color": 'rgba(0,0,0,0.05)'
                },
                'tooltip-dir': 'bottom',
                'tooltip-style': {
                    'background-color': 'rgba(0,0,0,0)',
                    border: '0',
                    color: 'black',
                    font: '14px Arial,Helvetica,sans-serif'
                },
                value: 0,
                formatter: (v) => {
                    var mins = Math.floor(v / 60);
                    var secs = (v % 60).toFixed();
                    return mins + ":" + ((secs < 10) ? '0' + secs : secs);
                    }
            },
            sliderProps: {
                width: '100%',
                height: 4,
                min: 0,
                tooltip: 'false',
                'dot-height': 4,
                'dot-width': 25,
                //speed: 0.0,
                sliderStyle: {
                    "backgroundColor": "rgba(0,0,0,0)"
                },
                processStyle: {
                    "border-radius": "0",
                    //"background-color": "#f222ff"
                    "backgroundImage": "-webkit-linear-gradient(left, #ffd319 20%, #ff901f 40%, #ff2975 55%, #f222ff 80%, #8c1eff 90%)"
                },
                bgStyle: {
                    "background-color": 'rgba(0,0,0,0)',
                },
                'tooltip-dir': 'bottom',
                'tooltip-style': {
                    'background-color': 'rgba(0,0,0,0)',
                    border: '0',
                    color: 'black',
                    font: '14px Arial,Helvetica,sans-serif'
                },
                value: 0,
                formatter: (v) => {
                    var mins = Math.floor(v / 60);
                    var secs = (v % 60).toFixed();
                    return mins + ":" + ((secs < 10) ? '0' + secs : secs);
                    }
            },
            widthWatcherInterval: null
        }
    },
    created() {
        this.$bus.$on('queue-opened', event => {
            setTimeout(this.refreshSlider, 400)
        });
    },
    /*mounted() {
        var el = this.$refs.slider.$refs.wrap;
        el.setAttribute('style', "width: 100%;");
    },*/
    computed: {
        sliderPropsComputed() {
            //console.log(this.$refs.slider.$refs.wrap)
            //this.widthWatcherInterval = setInterval(this.widthWatcher, 50, this.$refs.slider.$refs.wrap)
            if(this.isFull) return this.sliderPropsFull;
            else return this.sliderProps;
        },
        duration() {
            return this.$store.state.duration;
        },
        isDragging() {
            return this.$store.state.isDragging;
        },
        playing() {
            return this.$store.state.playing;
        },
        currentTime: {
            get() {return this.$store.state.currentTime},
            set(val) {
                this.$store.commit('currentTime', val);
            }
        },
        bar_style() {
            var pct = this.currentTime / this.duration * 100;
            pct = pct.toFixed(2);
            return 'width: ' + Math.min(pct, 100) + '%;';
        },
        trackLengthTop() {
            return this.toNormalTime(this.duration);
        },
        sliderMax() {
            return Number(this.duration);
        },
        transition() {
            if(this.playing)
            {
                return 'transition: all 0.5s;';
            }
            else
            {
                return '';
            }
        }
        /*sliderValue: {
            get() {return this.autoValue},
            set(val) {
                if(val != this.autoValue)
                {
                    this.lastValue = val;
                    //this.progress = val / this.duration;
                    bus.$emit('slidermoved', {value: val});
                }
            }
        }*/
    },
    watch: {
        /*isFull() {
            this.$refs.slider.refresh();
        },*/
        duration() {
            this.$refs.slider.refresh();
        },
        isPlayerHovered() {
            this.heightChanger();
        },
        isDragging(iD) {
            this.heightChanger();
            /*if(iD)
                this.sliderProps.speed = 0;
            else
                this.sliderProps.speed = 0.5;*/
        }
    },

    methods: {
        refreshSlider() {
            this.$refs.slider.refresh();
        },
        widthWatcher() {

        },
        heightChanger() {
            if (this.isPlayerHovered || this.isDragging)
            {
                this.sliderProps.height = 10;
                this.sliderProps['dot-height'] = 10;
            }
            else
            { 
                this.sliderProps.height = 4;
                this.sliderProps['dot-height'] = 4;
            }
        },
        dragStart() {
            //console.log('start');
            //bus.$emit('startsliderdragging');
            this.$store.commit('isDragging', true);
            this.$store.commit('playing', false);
        },
        dragEnd() {
            //console.log('end');
            /*bus.$emit('endsliderdragging', {
                value: this.lastValue
            });*/
            this.$store.commit('isDragging', false);
        },
        click() {
            this.$store.commit('isDragging', true);
            setTimeout(this.dragEnd, 100);
        },
        toNormalTime(seconds) {
            mins = Math.floor(seconds / 60);
            secs = (seconds % 60).toFixed();
            if(mins != NaN && secs != NaN)
                return mins + ":" + ((secs < 10) ? '0' + secs : secs);
            else
                return '';
        },
        
    }
}
</script>

<style scoped>

.full-vue-simple-progress {
    top: 75%;
    margin: auto;
    position: absolute;
    width: 750px;
    height: 20px;
    left: 0;
    right: 0;
    transition: left 0.3s, right 0.3s;
}

.vue-simple-progress {
    position: absolute;
    height: 75px;
    top: -10px;
    z-index: -2;
    width: 100%;
}

.vue-slider-my {
    bottom: 65px;
}

.background-progress-bar {
    background: rgba(0, 0, 0, 0.08);
    height: 100%;
    position: absolute;
    top: 10px;
    z-index: -1;
}

.played-time {
    color: #222;
    font-size: 14px;
    text-align: left;
    position: absolute;
    left: 5px;
    bottom: 1px;
}

.track-length {
    color: #222;
    font-size: 14px;
    text-align: right;
    position: absolute;
    right: 5px;
    bottom: 1px;
}
</style>