<template>
    <div>
        <!--<link rel="stylesheet" type="text/css" href="{% static 'mainapp/css/audio.css' %}" />
        <link id="playerCSS" rel="stylesheet" type="text/css" :href="CSSRef" />-->
        <div :class="isFull ? 'full-player' : 'player'" @mouseenter="onMouseEnter" @mouseleave="onMouseLeave">
            <div :class="isFull ? 'full-player-container' : 'player-container'" :style="containerMove">
                <buttons :isFull="isFull" @nextclick="playNextTrack" @dropdownclick="switchPlayerView"></buttons>
                <logos ref="logos" v-bind="logos" @likepressed="onLikePressed" :isFull="isFull"></logos>
                <menu-more :performerID="performerID" :isFull="isFull"></menu-more>
                <track-performer v-bind="trackPerformer" :isFull="isFull"></track-performer>
                <volume-controller ref="volumeController" :isFull="isFull"></volume-controller>
                <audio-player ref="audioPlayer" v-bind="audio" @playingended="playingEnded" :isFull="isFull"></audio-player>
                <queue :isFull="isFull"></queue>
                    <!--<img class="Button Player" id="previousButton" src="" draggable="false" />-->
            </div>
                
            <progress-bar :isPlayerHovered="isHovered" :isFull="isFull" :style="containerMove"></progress-bar>
        </div>
    </div>
</template>

<script>
import buttons from './TopPlayer/Buttons.vue'
import logos from './TopPlayer/Logos.vue'
import menuMore from './TopPlayer/Menu.vue'
import trackPerformer from './TopPlayer/TrackName.vue'
import volumeController from './TopPlayer/Volume.vue'
import audioPlayer from './TopPlayer/Audio.vue'
import queue from './TopPlayer/Queue.vue'
import progressBar from './TopPlayer/ProgressBar.vue'

export default {
    name: "top-player",
    components: {
        buttons,
        logos,
        menuMore,
        trackPerformer,
        volumeController,
        audioPlayer,
        queue,
        progressBar
    },
    data() {
        //var CSSRefs = { small: "/static/mainapp/css/audioSmall.css", full: "/static/mainapp/css/audioFull.css" };
        return {
            //CSSRefs: CSSRefs,
            //CSSRef: CSSRefs.small,
            isFull: false,
            isHovered: false,
            containerMove: '',
            performerID: 0,
            track: {
                current: null,
                currentID: null,
                nextID: null,
                isLiked: false
            },
            logos: {
                logoLink: '',
                nextLogoLink: '',
                prevLogoLink: '',
                isLiked: false,
                nextEnvelopeLogo: ''
            },
            trackPerformer: {
                trackName: '',
                performerName: ''
            },
            audio: {
                audioLink: '',
            },
            HTTPConfig: '',
            isTimeout: false
        }
    },
    mounted() {
        window.addEventListener('resize', this.updateContainer);
    },
    created() {
        this.loadNextTrack();
        this.$bus.$on('trackclicked', event => {
            //this.playNow(event.id);
            this.pushQueue(event.id);
            
        });
        this.$bus.$on('queue-opened', event => {
            //this.playNow(event.id);
            this.moveContainer('left');
            
        });
        this.$bus.$on('history-opened', event => {
            //this.playNow(event.id);
            this.moveContainer('right');
            
        });
        this.$bus.$on('page-changed', event => {
            console.log('piska')
            this.isFull = false;
        });
    },
    computed: {
        queueTracks: {
            get() {
                return this.$store.state.queueTracks
            }
        }
    },
    watch: {
        queueTracks() {
            if(this.queueTracks[0])
            {
                this.logos.nextLogoLink = this.queueTracks[0].image_alb;
                this.$refs.logos.refresh(this.queueTracks[0].image_alb);
            }
        }
    },
    methods: {        
        playingEnded() {
            this.playNextTrack()
        },
        moveContainer(prop) {
            if (this.containerMove === '')
            {
                this.setContainer(prop);
            }
            else
                this.containerMove = '';
        },
        updateContainer() {
            if (this.containerMove != '')
                this.setContainer('left');
        },
        setContainer(prop) {
            var dist = document.body.offsetWidth / 2 - 675;
            this.containerMove = (dist < 0) ? (prop + ': ' + ((dist-30) * 2) + 'px') : 'left: 0';
        },
        pushQueue(id) {
            this.$http.get('track_attr', {
                responseType: 'json',
                params: { id: id }
            }).then(response => {
                this.$store.commit('pushQueueTracks', response.data)

                //this.logos.nextLogoLink = this.queueTracks[0].image_alb;
                //this.$refs.logos.refresh(this.queueTracks[0].image_alb);
                
                //this.track.nextID = id;
                //this.loadNextTrack();
            });
        },
        playNextTrack() {
            //this.queue.tracks[0]
            this.$store.commit('pushHistoryTracks', this.track.current)
            var first =  this.queueTracks[0]
            this.loadNextTrack(first);
            this.$refs.logos.prepareForImmediateAnimating();
            this.$store.commit('removeFirstQueueTracks')
            
            this.$http.put('history', {}, {
                responseType: 'json',
                params: { track_id: first.id }
            }).then(response => {  });
        },
        switchPlayerView() {
            this.isFull = !this.isFull;
        },
        onLikePressed() {
            this.logos.isLiked = !this.logos.isLiked;
            this.likeTrack();
        },
        likeTrack() {
            //if(this.logos.isLiked != this.track.isLiked)
            //{   
                var varData = {
                    track_id: this.track.currentID
                };
                if(this.logos.isLiked)
                    this.$http.put('likes', {}, {
                        //headers: {"X-CSRFToken": csrftoken},
                        params: varData
                    }).then(this.successfulLikeFunc); //добавление
                else
                    this.$http.delete('likes', {
                        //headers: {"X-CSRFToken": csrftoken},
                        params: varData
                    }).then(this.successfulLikeFunc); //удаление
            //}
        },
        successfulLikeFunc(data) {
            //тут надо обрабатывать статусы
        },
        onMouseEnter() {
            this.isHovered = true;
        },
        onMouseLeave() {
            this.isHovered = false;
        },
        nextTrackTimeout() {
            this.isTimeout = false;
        },
        loadNextTrack(first = this.queueTracks[0]) {
            if(!this.isTimeout)
            {
                this.isTimeout = true;
                setTimeout(this.nextTrackTimeout, 1000);
                //this.likeTrack();
                var varData = {
                    current_track: this.track.currentID,
                    next_track: (first === undefined) ? '' : first.id
                };
                this.$http.get('next', {
                    responseType: 'json',
                    params: varData
                }).then(this.nextTrackSuccessFunc);
            }
        },
        nextTrackSuccessFunc(data) {         //функция успеха после получения следующего трека
            //console.log(data.body)
            
            var current = data.body.current;
            var next = data.body.next;

            this.track.current = current

            next.auto = true
            if(this.queueTracks.length === 0) this.queueTracks.push(next)

            var logo = this.logos.logoLink;
            this.setCurrentTrackAttrs(current);
            
            //this.track.nextID = next.id;
                       
            this.logos.prevLogoLink = logo;
            this.logos.nextLogoLink = this.queueTracks[0].image_alb;
            
        },
        setCurrentTrackAttrs(track) {
            this.trackPerformer.trackName = track.name_trc;
            this.trackPerformer.performerName = track.name_per;
            this.performerID = track.per_id;
            this.audio.audioLink = track.audio_trc;
            this.track.currentID = track.id;
            document.getElementById('title').innerHTML = track.name_per + " - " + track.name_trc;
            this.logos.logoLink = track.image_alb;
            this.track.isLiked = !!(track.is_liked);
            this.logos.isLiked = this.track.isLiked;
            this.$bus.$emit('next-track-load');
        }
    }
}
</script>

<style scoped>
.full-player-container {
	/*width: 450px;
    height: 450px;*/
    width: 600px;
    height: 650px;
    top: 0;
    bottom: 20%;
    right: 0;
    position:absolute;
    left: 0;
    margin: auto;
    transition: left 0.3s, right 0.3s;
}

.player-container {
	width: 100%;
    height: 65px;
    right: 0;
    position:absolute;
    left: 0;
    margin: auto;
}

.full-player {
    z-index: 116;
    right: 0;
    left: 0;
    margin: auto;
    top: 55px;
    /*height: 450px;*/
    /*width: 70%;*/
    width: 100%;
    height: 100%;
    position: fixed;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15), 0 10px 10px rgba(0,0,0,0.13);
    background-color: rgba(245, 245, 245, 0.95);
}

.player {
    /*position: relative;*/
    z-index: 70;
    margin: auto;
    height: 65px;
    bottom: 0px;
    left: 0;
    right: 0;
    width: 90%;
    position: fixed;
    box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
    background-color: rgba(245, 245, 245, 0.95);
}

.player:hover {
    background-color: rgba(235, 235, 235, 0.95);
}
</style>

