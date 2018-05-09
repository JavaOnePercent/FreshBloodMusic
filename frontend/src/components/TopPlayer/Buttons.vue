<template>
    <div>
        <img src="/static/mainapp/images/nextButton.png" class="Button previous-button" draggable="false" />
        <img :src="playSrc" class="Button play-button" @click="playClick" draggable="false" />
        <img src="/static/mainapp/images/nextButton.png" class="Button next-button" @click="nextClick" draggable="false" />
        <img :src="dropdownSrc" class="Button dropdown-button" @click="dropdownClick" draggable="false" />
    </div>
</template>

<script>
export default {
    name: 'buttons',
    props: [ 'isFull' ],
    data() {
        var playSrcs = {play: '/static/mainapp/images/playButton.png', pause: '/static/mainapp/images/pauseButton.png'};
        var dropdownSrcs = {drop: '/static/mainapp/images/dropdown.png', close: '/static/mainapp/images/closeDropdown.png'};
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
        nextClick(){
            this.$emit('nextclick');
            this.$bus.$emit('nextclick');
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
.play-button {
	width: 30px;
	height: 30px;
    left: 30px;
    margin: auto;
	position: absolute;
    z-index: 10;
    top: 0;
    bottom: 0;
}
.play-button:hover {
    left: 29px;
	width: 32px;
	height: 32px;
}
.next-button {
    width: 30px;
    height: 30px;
    left: 90px;
    margin: auto;
	position: absolute;
    z-index: 10;
    top: 0;
    bottom: 0;
}
.next-button:hover {
    left: 89px;
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
}
.dropdown-button:hover {
    right: 29px;
	width: 32px;
	height: 32px;
}
</style>