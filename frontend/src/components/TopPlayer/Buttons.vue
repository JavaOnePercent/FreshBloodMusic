<template>
    <div>
        <img src="/static/mainapp/images/previousButton.svg" :class="isFull ? 'full-previous-button' : 'previous-button'" @click="prevClick" draggable="false" />
        <img :src="playSrc" :class="isFull ? 'full-play-button' : 'play-button'" @click="playClick" draggable="false" />
        <img src="/static/mainapp/images/nextButton.svg" :class="isFull ? 'full-next-button' : 'next-button'" @click="nextClick" draggable="false" />
        <img :src="dropdownSrc" :class="isFull ? 'full-dropdown-button' : 'dropdown-button'" @click="dropdownClick" draggable="false" />
    </div>
</template>

<script>
export default {
    name: 'buttons',
    props: [ 'isFull' ],
    data() {
        var playSrcs = {play: '/static/mainapp/images/playButton.svg', pause: '/static/mainapp/images/pauseButton.svg'};
        var dropdownSrcs = {drop: '/static/mainapp/images/dropdown.svg', close: '/static/mainapp/images/closeDropdown.svg'};
        return {
            playSrcs: playSrcs,
            dropdownSrcs: dropdownSrcs,
            playSrc: playSrcs.play,
            dropdownSrc: dropdownSrcs.drop
        }
    },
    methods: {
        playClick() {
            this.$store.commit('switchPlaying');
        },
        prevClick() {
            this.$emit('prevclick');
        },
        nextClick(){
            this.$emit('nextclick');
        },
        dropdownClick(){
            this.$emit('dropdownclick');
        }
    },
    computed: {
        playing() {
            return this.$store.state.playing;
        },
        isDragging() {
            return this.$store.state.isDragging;
        }
    },
    watch: {
        playing(pl){
            (pl || this.isDragging) ?
                this.playSrc = this.playSrcs.pause :
                this.playSrc = this.playSrcs.play;
        },
        isFull(iF){
            (iF) ?
                this.dropdownSrc = this.dropdownSrcs.close :
                this.dropdownSrc = this.dropdownSrcs.drop;
        }
    }
}
</script>

<style scoped>

.full-play-button {
	top: 452px;
	width: 50px;
	height: 50px;
    left: 0;
    right: 0;
    margin: auto;
	position: absolute;
    cursor: pointer;
}

.full-play-button:hover {
    top: 451px;
	width: 52px;
	height: 52px;
}

.play-button {
	width: 30px;
	height: 30px;
    left: 90px;
    margin: auto;
	position: absolute;
    z-index: 10;
    top: 0;
    bottom: 0;
    cursor: pointer;
}

.play-button:hover {
    left: 89px;
	width: 32px;
	height: 32px;
}

.full-previous-button {
    top: 457px;
    width: 40px;
    height: 40px;
    left: -230px;
    right: 0;
    margin: auto;
    position: absolute;
    cursor: pointer;
}

.full-previous-button:hover {
    top: 456px;
	width: 42px;
	height: 42px;
}

.previous-button {
    width: 30px;
    height: 30px;
    left: 30px;
    margin: auto;
	position: absolute;
    z-index: 10;
    top: 0;
    bottom: 0;
    cursor: pointer;
}

.previous-button:hover {
    left: 29px;
	width: 32px;
	height: 32px;
}

.full-next-button {
    top: 457px;
    width: 40px;
    height: 40px;
    right: -230px;
    left: 0;
    margin: auto;
	position: absolute;
    cursor: pointer;
}
.full-next-button:hover {
    top: 456px;
    /*right: 164px;*/
	width: 42px;
	height: 42px;
}

.next-button {
    width: 30px;
    height: 30px;
    left: 150px;
    margin: auto;
	position: absolute;
    z-index: 10;
    top: 0;
    bottom: 0;
    cursor: pointer;
}

.next-button:hover {
    left: 149px;
	width: 32px;
	height: 32px;
}

.full-dropdown-button {
    margin: auto;
	position: fixed;
    width: 30px;
    height: 30px;
    right: 40px;
    top: 84px;
    cursor: pointer;
}
.full-dropdown-button:hover {
    top: 83px;
    right: 39px;
	width: 32px;
	height: 32px;
}

.dropdown-button {
    margin: auto;
	position: absolute;
    width: 30px;
    height: 30px;
    right: 30px;
    top: 0;
    bottom: 0;
    cursor: pointer;
}

.dropdown-button:hover {
    right: 29px;
	width: 32px;
	height: 32px;
}

</style>