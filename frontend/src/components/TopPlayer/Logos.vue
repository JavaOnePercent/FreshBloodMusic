<template>
    <div>
        <div :class="isFull ? 'full-main-logo' : 'main-logo'" @click="click" @mouseenter="onMouseEnterMain" @mouseleave="onMouseLeaveMain" :style="mainLogoAnimation">
            <!--<img :class="isFull ? 'full-vinyl' : 'vinyl'" src="/static/mainapp/images/redVinyl.png">-->
            <img :class="isFull ? 'full-logo' : 'logo'" :src="logoLink" draggable="false" :style="rotationCSS"/>
            <img :class="isFull ? 'full-like' : 'like'" v-show="showLike" src="/static/mainapp/images/like.svg" draggable="false"/>
        </div>
        <img :class="isFull ? 'full-main-to-prev-logo' : 'main-to-prev-logo'" :src="mainToPrevLogo" draggable="false" :style="mainToPrevLogoAnimation"/>
        <img :class="isFull ? 'full-next-to-main-logo' : 'next-to-main-logo'" :src="nextToMainLogo" draggable="false" :style="nextToMainLogoAnimation"/>
        <img :class="isFull ? 'full-prev-envelope' : 'prev-envelope'" :src="prevEnvelopeLogo" draggable="false" :style="prevEnvelopeAnimation"/>
        <img :class="isFull ? 'full-prev-logo' : 'prev-logo'" @click="prevLogoClick" :src="prevLogo" v-show="showPrev" draggable="false" :style="prevLogoAnimation"/>
        <img :class="isFull ? 'full-next-logo' : 'next-logo'" @click="nextLogoClick" :src="nextLogo" draggable="false" :style="nextLogoAnimation"/>
        <img :class="isFull ? 'full-next-envelope' : 'next-envelope'" :src="nextEnvelopeLogo" draggable="false" :style="nextEnvelopeAnimation"/>
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
            prevEnvelopeLogo: '',
            prevLogo: '',
            nextLogo: '',
            lastRotation: '',
            wasPlaying: false,
            nextEnvelopeLogo: '',
            mainToPrevLogo: '',
            nextToMainLogo: '',
            isAnimating: false
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
            this.lastRotation = this.audio.currentTime/this.audio.duration * 1080;
            this.wasPlaying = this.playing;
            this.isAnimating = true;
            this.nextLogo = event.nextLogoLink
            this.mainToPrevLogo = event.prevLogoLink
            this.nextToMainLogo = event.logoLink
            this.prevEnvelopeLogo = event.prevLogoLink
            if(this.isFull)
            {this.nextEnvelopeAnimation = {opacity: 1.0, transition: 'opacity 0.1s'};
            this.nextLogoAnimation = 'visibility: hidden;';
            this.mainLogoAnimation = 'visibility: hidden;';
            this.mainToPrevLogoAnimation = 'transform: rotate(' + this.lastRotation + 'deg);';
            setTimeout(this.startAnimation, 100);}
        });
        this.$bus.$on('prev-click', event => {
            this.lastRotation = this.audio.currentTime/this.audio.duration * 1080;
            this.wasPlaying = this.playing;
            this.isAnimating = true;
            //this.prevEnvelopeLogo = event.logoLink
            this.nextToMainLogo = event.logoLink
            this.mainToPrevLogo = event.nextLogoLink
            this.nextEnvelopeLogo = event.nextLogoLink
            this.prevLogo = event.prevLogoLink
            if(this.isFull)
            {this.prevEnvelopeAnimation = {opacity: 1.0, transition: 'opacity 0.1s', top: '100px'};
            this.prevLogoAnimation = 'visibility: hidden;';
            this.mainLogoAnimation = 'visibility: hidden;';
            this.mainToPrevLogoAnimation = 'transform: rotate(' + this.lastRotation + 'deg); left: unset; right: 165px;';
            this.nextToMainLogoAnimation = {right: 'unset', left: '-75px', transition: null, top: null, height: null, width: null }
            this.nextEnvelopeAnimation = {top: "0"}
            setTimeout(this.startBackwardsAnimation, 100);}
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
            if(pr !== '')
                this.showPrev = true;
            else
                this.showPrev = false
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
        prepareForImmediateAnimating() {
            this.isAnimating = true;
            this.nextLogoAnimation = 'visibility: hidden;';
            this.nextEnvelopeAnimation = {opacity: 1.0, transition: 'opacity 0.1s'};
        },
        refresh(logo) {
            if(!this.isAnimating)
            {
                this.nextEnvelopeLogo = logo;
                this.nextLogo = logo;
            }
        },
        nextLogoClick() {
            this.$bus.$emit('queue-opened');
        },
        prevLogoClick() {
            this.$bus.$emit('history-opened');
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
        startBackwardsAnimation() {
            
            setTimeout(this.endBackwardsAnimation, 800);
            this.mainToPrevLogoAnimation += 'right: -75px; height: 150px; width: 150px; top: 100px; transition: right 0.8s, height 0.3s, width 0.3s, top 0.3s;';
            this.nextToMainLogoAnimation.left= '165px';  this.nextToMainLogoAnimation.transition= 'left 0.8s' 
            setTimeout(this.startExpandingNextToMain, 500);
            
            this.nextEnvelopeAnimation = {top: '100px', opacity: '1.0', transition: 'top 0.3s, opacity 0.3s'};
            this.nextLogoAnimation = 'right: -200px; opacity: 0.0; transition: right 0.5s, opacity 0.5s;';
            this.prevLogoAnimation = 'left: -200px; opacity: 0.0; transition: all 0.0s';
            setTimeout(this.movePrevEnvelopeBackwards, 500);
        },
        endBackwardsAnimation() {
            
            this.prevEnvelopeLogo = this.prevLogoLink;
            this.nextLogo = this.nextLogoLink;
            this.mainToPrevLogoAnimation = 'visibility:hidden;';
            this.nextToMainLogoAnimation = 'visibility:hidden;'
            this.mainLogoAnimation = '';
            this.nextEnvelopeAnimation.opacity = 0.0;
            this.nextEnvelopeAnimation.transition = 'opacity 0.15s';
            setTimeout(this.hideNextEnvelopeBackwards, 150);
            this.prevLogoAnimation = '';
            this.nextLogoAnimation = '';
            this.prevEnvelopeAnimation = 'visibility:hidden;';
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
        hideNextEnvelopeBackwards() {
            this.prevEnvelopeLogo = this.prevLogoLink;
            this.nextEnvelopeAnimation = 'visibility:hidden;';
            this.isAnimating = false;
        },
        hidePrevEnvelope() {
            this.prevEnvelopeLogo = this.prevLogoLink;
            this.prevEnvelopeAnimation = 'visibility:hidden;';
            this.isAnimating = false;
        },
        startExpandingNextToMain(){
            this.nextToMainLogoAnimation.transition += ', top 0.3s, height 0.3s, width 0.3s';
            this.nextToMainLogoAnimation.top = '40px';
            this.nextToMainLogoAnimation.height = '270px';
            this.nextToMainLogoAnimation.width = '270px';
        },
        movePrevEnvelopeBackwards() {
            this.prevEnvelopeAnimation.top = '0px';
            this.prevEnvelopeAnimation.opacity = '0.0';
            this.prevEnvelopeAnimation.transition = 'all 0.3s';
            this.prevLogoAnimation = 'transition: left 0.5s, opacity 0.5s;';
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
.full-main-logo {
    top: 40px;
    width: 270px;
    height: 270px;
    border-radius: 50%;
	box-shadow: 0px 4px 28px rgba(0, 0, 0, .5)/*#64bdf5;*/;
    right: 0;
    left: 0;
    margin: auto;
	position: absolute;
	visibility:visible;
    z-index:15;
    
}
.full-main-logo:hover {
    top: 37px;
	width: 276px;
	height: 276px;
	box-shadow: 0px 0px 30px #C732B1;
}

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
    cursor: pointer;
}

.main-logo:hover {
    right: 209px;
	width: 58px;
	height: 58px;
}

.full-like {
    z-index: 5;
    opacity: 0.8;
    width: 90px;
    height: 90px;
    position: absolute;
    margin: auto;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
}

.like {
    z-index: 5;
    opacity: 0.8;
    width: 70%;
    height: 70%;
    position: absolute;
    margin: auto;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
}

.full-logo {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    z-index:0;
    position: absolute;
    
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

.full-next-logo {
	top: 100px;
    right: -75px;
	opacity: 0.6;
	width: 150px;
    height: 150px;
    transition: opacity 0.2s;
    position: absolute;
    margin: auto;
}

.full-next-logo:hover {
    opacity: 1;
}

.next-logo {
	display: none;
}

.full-prev-logo {
	top: 100px;
    left: -75px;
	opacity: 0.6;
	width: 150px;
    height: 150px;
    transition: opacity 0.2s;
    position: absolute;
    margin: auto;
}

.full-prev-logo:hover {
    opacity: 1;
}

.prev-logo {
	top: -50%;
    left: 0;
	opacity: 0.3;
	width: 25%;
	height: 25%;
    visibility: hidden;
}

.full-main-to-prev-logo {
	top: 40px;
    z-index:0;
    width: 270px;
    height: 270px;
    border-radius: 50%;
    left: 165px;
    margin: auto;
    position: absolute;
}

.main-to-prev-logo {
	display: none;
}

.full-next-to-main-logo {
	top: 100px;
    z-index:0;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    right: -75px;
    opacity: 1.0;
    margin: auto;
    position: absolute;
}

.next-to-main-logo {
	display: none;
}

.full-prev-envelope {
	top: 0px;
    left: -75px;
	opacity: 0.0;
	width: 150px;
    height: 150px;
    z-index: 20;
    margin: auto;
    position: absolute;
}

.prev-envelope {
	display: none;
}

.full-next-envelope {
	top: 100px;
    right: -75px;
	opacity: 0.6;
	width: 150px;
    height: 150px;
    z-index: 20;
    margin: auto;
    position: absolute;
}

.next-envelope {
	display: none;
}
</style>