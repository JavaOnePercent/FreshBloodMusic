<template>
    <audio id="audio" ref="audio" :src="audioLink" @loadeddata="startPlaying" @ended="endPlaying" preload> <!-- @timeupdate="setCurrentTime" -->
    </audio>
</template>

<script>
export default {
    name: 'audio-player',
    props: [
        'audioLink'
    ],
    /*created() {
        bus.$on('slidermoved', event => {
            this.setCurrentTime(event.value);
        });
        bus.$on('startsliderdragging', event => {
            this.$refs.audio.pause();
        });
        bus.$on('endsliderdragging', event => {
            //this.updateProgress();
            this.$refs.audio.play();
            this.$emit('startplaying');
        });
    },*/
    data() {
        return {
            isFirst: true,
            timer: '',
            //progress: 0.0,
            duration: 0.0
        }
    },
    computed: {
        playing() {
            return this.$store.state.playing;
        },
        isDragging() {
            return this.$store.state.isDragging;
        },
        volume() {
            return this.$store.state.volume;
        },
        newTime: {
            get() { return this.$store.state.currentTime }
        },
        
    },
    watch: {
        newTime(val) {
            if(this.$store.state.isDragging)
            {
                this.$refs.audio.currentTime = val;
            }
        },
        playing(pl){
            if(pl)
            {
                this.$refs.audio.play();
                this.timer = setInterval(this.updateProgress, 500); //таймер для обновления прогресса воспроизведения
            }
            else
            {
                clearInterval(this.timer);
                this.$refs.audio.pause();
            }
        },
        volume(vol){
            this.$refs.audio.volume = this.volume / 100;
        },
        isDragging(isDragging){
            if(!isDragging)
            {
                this.$store.commit('playing', true);
                this.$refs.audio.play();
            }
        }
    },
    methods: {
        /*setCurrentTime() {
            if(!this.$store.state.isDragging)
            {
                this.$store.commit('currentTime', this.$refs.audio.currentTime);
            } 
        },*/
        endPlaying() {
            this.$bus.$emit('playingended');
            this.$emit('playingended');
        },
        /*setCurrentTime(val) {
            this.$refs.audio.currentTime = val;
        },*/
        startPlaying() {
            
            this.duration = this.$refs.audio.duration;
            this.$store.commit('duration', this.duration);
            this.updateProgress();
            if(!this.isFirst) {
                this.$store.commit('playing', true);
                this.$refs.audio.play();
                //this.$emit('startplaying');
                this.$bus.$emit('startplaying');
            }
            else
                this.isFirst = false;
        },
        updateProgress() {
            if(!this.$store.state.isDragging)
            {
                this.$store.commit('currentTime', this.$refs.audio.currentTime);
            } 
            /*this.progress = this.$refs.audio.currentTime / this.$refs.audio.duration;
            bus.$emit('progresschanged', {
                progress: this.progress,
                currentTime: this.$refs.audio.currentTime,
                duration: this.$refs.audio.duration
			});*/
        }
    }
}
</script>

<style scoped>

</style>