<template>
    <div>
        <div class="Button main-logo" @click="click" @mouseenter="onMouseEnterMain" @mouseleave="onMouseLeaveMain" :style="mainLogoAnimation">
            <img class=vinyl src="/static/mainapp/images/redVinyl.png">
            <img class="logo" :src="logoLink" draggable="false" :style="rotationCSS"/>
            <img class="Player like" v-show="showLike" src="/static/mainapp/images/like.png" draggable="false"/>
        </div>
        <img class="main-to-prev-logo" :src="logo" draggable="false" :style="mainToPrevLogoAnimation"/>
        <img class="next-to-main-logo" :src="logoLink" draggable="false" :style="nextToMainLogoAnimation"/>
        <img class="prev-envelope" :src="logo" draggable="false" :style="prevEnvelopeAnimation"/>
        <img class="Button prev-logo" :src="prevLogo" v-show="showPrev" draggable="false" :style="prevLogoAnimation"/>
        <img class="Button next-logo" @click="nextLogoClick" :src="nextLogoLink" draggable="false" :style="nextLogoAnimation"/>
        <img class="next-envelope" :src="nextEnvelopeLogo" draggable="false" :style="nextEnvelopeAnimation"/>
    </div>
</template>

<script>
export default {
    name: 'logos',
    props:[
        'logoLink',
        'nextLogoLink',
        'prevLogoLink',
        'isLiked',
        'isFull',
    ],
    data() {
        return {
            showLike: false,
            showPrev: false,
            rotationCSS: '',
            mainToPrevLogoAnimation: '',
            nextToMainLogoAnimation: '',
            mainLogoAnimation: '',
            prevEnvelopeAnimation:'',
            prevLogoAnimation: '',
            nextEnvelopeAnimation:'',
            nextLogoAnimation: '',
            audio: null,
            logo: '',
            prevLogo: '',
            lastRotation: '',
            wasPlaying: false,
            nextEnvelopeLogo: ''
            //duration: 0,
            //currentTime: 0
        }
    },
    computed: {
        currentTime() {
            return this.$store.state.currentTime;
        },
        /*duration() {
            return this.$store.state.duration;
        },*/
        playing() {
            return this.$store.state.playing;
        },
        isDragging() {
            return this.$store.state.isDragging;
        }
    },
    created() {
        this.$bus.$on('nextclick', event => {
            this.lastRotation = this.audio.currentTime/this.audio.duration * 1080;
            this.wasPlaying = this.playing;
        });
        this.$bus.$on('playingended', event => {
            this.lastRotation = this.audio.currentTime/this.audio.duration * 1080;
            this.wasPlaying = true;
        });
        this.$bus.$on('startplaying', event => {
            this.rotate(false, 0);
            //console.log(this.rotationCSS);
            if(this.wasPlaying)
            {
                this.rotate(false, 0.1/this.audio.duration * 1080);
                setTimeout(this.rotate, 100, true, 1080, this.audio.duration - this.audio.currentTime);
            }
        });
        this.$bus.$on('next-track-load', event => {
            this.nextEnvelopeAnimation = {opacity: 1.0, transition: 'opacity 0.1s'};
            this.nextLogoAnimation = 'visibility: hidden;';
            this.mainLogoAnimation = 'visibility: hidden;';
            this.mainToPrevLogoAnimation = 'transform: rotate(' + this.lastRotation + 'deg);';
            setTimeout(this.startAnimation, 100);
        });
        
        /*bus.$on('slidermoved', event => {
            this.updateRotation(false);
        });
        bus.$on('endsliderdragging', event => {
            //console.log(event.value);
            
        });*/
    },
    mounted() {
        this.audio = document.getElementById('audio');
    },
    watch: {
        isDragging(isDragging) {
            if(!isDragging)
            {
                this.rotate(false, (this.audio.currentTime + 0.1) / this.audio.duration * 1080);
                setTimeout(this.updateRotation, 100, true);
            }
        },
        currentTime(cur) {
            if(this.isDragging && this.isFull)
            {
                this.rotate(false, cur/this.audio.duration * 1080);
            }
        },
        isLiked(shL) {
            this.showLike = shL;
        },
        prevLogo(pr) {
            if(pr != '')
                this.showPrev = true;
        },
        isFull(iF) {
            if(!iF) this.rotationCSS = ''
            else 
            {
                this.rotate(false, (this.audio.currentTime+((this.playing) ? 0.1 : 0))/this.audio.duration * 1080);
                if(this.playing)
                    setTimeout(this.rotate, 100, true, 1080, this.audio.duration - this.audio.currentTime);
            }
        },
        playing(playing) {
            //console.log(this.rotationCSS)
            if(!this.isDragging)
                if(this.rotationCSS != 'transform: rotate(0deg);')
                    this.updateRotation(playing);
                else
                {
                    this.rotate(false, 0.1/this.audio.duration * 1080);
                    setTimeout(this.updateRotation, 100, playing);
                }
            //console.log(this.audio.currentTime + ' ' + this.audio.duration + ' ' + this.rotationCSS);
        }
    },
    
    methods: {
        refresh(link) {
            this.nextEnvelopeLogo = link;
        },
        nextLogoClick() {
            this.$bus.$emit('queue-opened');
        },
        startAnimation() {
            setTimeout(this.endAnimation, 800);
            this.mainToPrevLogoAnimation += 'left: -75px; height: 150px; width: 150px; top: 100px; transition: left 0.8s, height 0.3s, width 0.3s, top 0.3s;';
            this.nextToMainLogoAnimation = {right: '165px', transition: 'right 0.8s'}; 
            setTimeout(this.startExpandingNextToMain, 500);
            
            this.prevEnvelopeAnimation = {top: '100px', opacity: '1.0', transition: 'top 0.3s, opacity 0.3s'};
            this.prevLogoAnimation = 'left: -200px; opacity: 0.0; transition: left 0.5s, opacity 0.5s;';
            this.nextLogoAnimation = 'right: -200px; opacity: 0.0; transition: all 0.0s';
            setTimeout(this.moveNextEnvelope, 500);
        },
        endAnimation() {
            
            this.nextEnvelopeLogo = this.nextLogoLink;
            this.prevLogo = this.prevLogoLink;
            this.mainToPrevLogoAnimation = 'visibility:hidden;';
            this.nextToMainLogoAnimation = 'visibility:hidden;'
            this.mainLogoAnimation = '';
            //this.prevEnvelopeAnimation = 'visibility:hidden;';
            this.prevEnvelopeAnimation.opacity = 0.0;
            this.prevEnvelopeAnimation.transition = 'opacity 0.15s';
            setTimeout(this.hidePrevEnvelope, 150);
            this.prevLogoAnimation = '';
            this.nextLogoAnimation = '';
            this.nextEnvelopeAnimation = 'visibility:hidden;';
        },
        hidePrevEnvelope() {
            this.logo = this.logoLink;
            this.prevEnvelopeAnimation = 'visibility:hidden;';
        },
        startExpandingNextToMain(){
            this.nextToMainLogoAnimation.transition += ', top 0.3s, height 0.3s, width 0.3s';
            this.nextToMainLogoAnimation.top = '40px';
            this.nextToMainLogoAnimation.height = '270px';
            this.nextToMainLogoAnimation.width = '270px';
        },
        moveNextEnvelope() {
            this.nextEnvelopeAnimation.top = '0px';
            this.nextEnvelopeAnimation.opacity = '0.0';
            this.nextEnvelopeAnimation.transition = 'all 0.3s';
            this.nextLogoAnimation = 'transition: right 0.5s, opacity 0.5s;';
        },
        click() {
            this.$emit('likepressed');
        },
        onMouseEnterMain() {
            if(this.isLiked === false)
                this.showLike = true;
        },
        onMouseLeaveMain() {
            if(this.isLiked === false)
                this.showLike = false;
        },
        updateRotation(playing){
            if(this.isFull)
            {
                if(playing)
                    this.rotate(true, 1080, this.audio.duration - this.audio.currentTime);
                else
                    this.rotate(false, this.audio.currentTime/this.audio.duration * 1080);
            }
        },
        rotate(animation, angle, time=0) {
            if(this.isFull)
                this.rotationCSS = 'transform: rotate(' + angle + 'deg);' + ((animation) ? 'transition: transform ' + time + 's linear;' : '');
        }
    }
}
</script>

<style scoped>
.main-logo {
    width: 56px;
	height: 56px;
	/*box-shadow: 0px 4px 28px black/*#64bdf5;;*/
	/*right: 115px;*/
	right: 210px;
	position: absolute;
    z-index: 15;
    top: 0;
    bottom: 0;
    margin: auto;
}

.main-logo:hover {
    right: 209px;
	width: 58px;
	height: 58px;
}

.like {
    z-index: 5;
    opacity: 0.8;
    width: 70%;
    height: 70%;
}

.logo {
    width: 100%;
	height: 100%;
	/*box-shadow: 0px 4px 28px black/*#64bdf5;;*/
    opacity: 0.9;
	z-index: 0;
	visibility: visible;
    padding: 0;
}

.vinyl {
    display: none;
}

.next-logo {
	display: none;
}

.prev-logo {
	top: -50%;
    left: 0;
	opacity: 0.3;
	width: 25%;
	height: 25%;
    visibility: hidden;
}

.main-to-prev-logo {
	display: none;
}

.next-to-main-logo {
	display: none;
}

.prev-envelope {
	display: none;
}

.next-envelope {
	display: none;
}
</style>