<template>
        <!--<link rel="stylesheet" type="text/css" href="{% static 'mainapp/css/audio.css' %}" />
        <link id="playerCSS" rel="stylesheet" type="text/css" :href="CSSRef" />-->
        <div :class="isFull ? 'full-player' : 'player'" @mouseenter="onMouseEnter" @mouseleave="onMouseLeave">
            <div :class="isFull ? 'full-player-container' : 'player-container'" :style="containerMove">
                <buttons :isFull="isFull" @nextclick="playNextTrack" @prevclick="prevClick" @dropdownclick="switchPlayerView"></buttons>
                <logos ref="logos" v-bind="logos" @likepressed="onLikePressed" :isFull="isFull"></logos>
                <menu-more :performerID="performerID" :isLiked="logos.isLiked" @likepressed="onLikePressed" @show-performer="isFull = false" :isFull="isFull"></menu-more>
                <track-performer :performerID="performerID" v-bind="trackPerformer" :isFull="isFull"></track-performer>
                <volume-controller ref="volumeController" :isFull="isFull"></volume-controller>
                <audio-player ref="audioPlayer" v-bind="audio" @playingended="playingEnded" :isFull="isFull"></audio-player>
                <queue :isFull="isFull"></queue>
                    <!--<img class="Button Player" id="previousButton" src="" draggable="false" />-->
            </div>
                
            <progress-bar :isPlayerHovered="isHovered" :isFull="isFull" :style="containerMove"></progress-bar>
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
            containerMove: {left: 0, right: 0},
            performerID: 0,
            track: {
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
        //this.loadNextTrack();
        this.$bus.$on('track-to-queue', event => {
            //this.playNow(event.id);
            this.pushQueue(event.id);
            
        });
        this.$bus.$on('play-track', event => {
            //this.playNow(event.id);
            this.playNow(event.id);
            
        });
        this.$bus.$on('queue-opened', event => {
            //this.playNow(event.id);
            this.moveContainer('left');
            
        });
        this.$bus.$on('history-opened', event => {
            //this.playNow(event.id);
            this.moveContainer('right');
            
        });
        this.$bus.$on('set-current-track', event => {
            //this.playNow(event.id);
            //console.log(this.historyTracks[0])
            if(this.historyTracks[0])
            {
                this.logos.logoLink = this.historyTracks[0].image_alb
                this.logos.prevLogoLink = this.historyTracks[0].image_alb
                this.$refs.logos.prevLogo = this.historyTracks[0].image_alb
            }
            if(!event) event = 'next'
            var self = this
            this.$http.get('../api/tracks/' + event, {
                    responseType: 'json'
                }).then(response => {
                    self.$store.commit('pushQueueTracks', response.data)
                    self.$http.put('../api/history', {}, {
                        responseType: 'json',
                        params: { track_id: response.data.id },
                        headers: {'X-CSRFToken': this.$root.csrftoken}
                        }).then(response => { self.loadNextTrack() }, error => { self.loadNextTrack(); });
                });
            
        });
        
    },
    computed: {
        queueTracks: {
            get() {
                return this.$store.state.queueTracks
            }
        },
        historyTracks() {
            return this.$store.state.historyTracks
        },
        current: {
            get() {
                return this.$store.state.currentTrack
            },
            set(data) {
                this.$store.commit('currentTrack', data)
            }
        }
    },
    watch: {
        queueTracks() {
            if(this.queueTracks[0])
            {
                this.logos.nextLogoLink = this.queueTracks[0].image_alb;
                this.$refs.logos.refresh(this.logos.nextLogoLink);
            }
        },
        isFull(iF) {
            if(iF)
            {
                window.addEventListener('resize', this.updateContainer);
            }
            else
            {
                window.removeEventListener('resize', this.updateContainer);
                this.containerMove = {}
            }
        },
        '$route': function() {
            this.isFull = false
        }
    
    },
    methods: {

        prevClick() {
            if(this.historyTracks.length > 0 && !this.isTimeout)
            {
                this.isTimeout = true;
                var self = this
                setTimeout(function() { self.isTimeout = false }, 1000);
                this.$store.commit('unshiftQueueTracks', this.current)

                this.$http.get('../api/tracks/' + this.historyTracks[0].id, {
                    responseType: 'json'
                }).then(response => {
                    var current = response.body
                    this.setCurrentTrackAttrs(current);
                    this.current = current
                    this.$store.commit('removeFirstHistoryTracks')
                    this.logos.prevLogoLink = this.historyTracks[0] ? this.historyTracks[0].image_alb : ''
                    this.logos.logoLink = current ? current.image_alb : ''
                    this.logos.nextLogoLink = this.queueTracks[0].image_alb
                    //this.logos.nextLogoLink = this.queueTracks[0].image_alb
                    //this.$refs.logos.refresh()
                    this.$bus.$emit('prev-click', this.logos);
                });
                
            }
        },  
        playingEnded() {
            this.playNextTrack()
        },
        moveContainer(prop) {
            if (prop === 'left')
            {
                if(this.containerMove.left === 0)
                {
                    this.setContainer(prop);
                    this.containerMove.right = 0;
                }
                else
                    this.containerMove.left = 0;
            }
            else if (prop === 'right')
                if(this.containerMove.right === 0)
                {
                    this.setContainer(prop);
                    this.containerMove.left = 0;
                }
                else
                    this.containerMove.right = 0;
        },
        updateContainer() {
            if (this.containerMove.left !== 0)
            {
                this.setContainer('left');
            }
            if (this.containerMove.right !== 0)
            {
                this.setContainer('right');
            }
        },
        setContainer(prop) {
            var dist = document.body.offsetWidth / 2 - 675;
            var offset = (dist < 0) ? (((dist-30) * 2) + 'px') : '0'
            //this.$set(this.containerMove, prop, offset)
            //this.containerMove[prop] = offset
            if (prop == 'left')
                this.containerMove.left = offset
            else
                this.containerMove.right = offset
        },
        pushQueue(id) {
            var isNotInQueue = true
            for(var i = 0; i < this.queueTracks.length; i++)
            {
                if(this.queueTracks[i].id === id)
                {
                    isNotInQueue = false
                    break
                }
            }
            if(isNotInQueue)
            {
                this.$http.get('../api/tracks/' + id, {
                    responseType: 'json'
                }).then(response => {
                    this.$store.commit('pushQueueTracks', response.data)
                    
                    //this.logos.nextLogoLink = this.queueTracks[0].image_alb;
                    //this.$refs.logos.refresh(this.queueTracks[0].image_alb);
                    
                    //this.track.nextID = id;
                    //this.loadNextTrack();
                });
            }
        },
        playNow(id) {
            if(this.current.id !== id)
                this.$http.get('../api/tracks/' + id, {
                    responseType: 'json'
                }).then(response => {
                    //this.$store.commit('pushHistoryTracks', this.track.current)
                    this.$store.commit('unshiftQueueTracks', response.data)

                    //this.logos.nextLogoLink = this.queueTracks[0].image_alb;
                    //this.$refs.logos.refresh(this.queueTracks[0].image_alb);
                    
                    //this.track.nextID = id;
                    this.playNextTrack();
                });
            else
                this.$refs.audioPlayer.startPlaying()
        },
        playNextTrack() {
            //this.queue.tracks[0]
            if(!this.isTimeout)
            {
                this.isTimeout = true;
                setTimeout(this.nextTrackTimeout, 1000);
                this.$store.commit('pushHistoryTracks', this.current)
                var first =  this.queueTracks[0]
                if (this.isFull) this.$refs.logos.prepareForImmediateAnimating();
                //this.$store.commit('removeFirstQueueTracks')
                
                var self = this
                this.$http.put('../api/history', {}, {
                    responseType: 'json',
                    params: { track_id: first.id },
                    headers: {'X-CSRFToken': this.$root.csrftoken}
                }).then(response => { self.loadNextTrack(); }, error => { self.loadNextTrack(); });
            }
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
                    this.$http.put('../api/likes', {}, {
                        //headers: {"X-CSRFToken": csrftoken},
                        params: varData,
                        headers: {'X-CSRFToken': this.$root.csrftoken}
                    }).then(this.successfulLikeFunc); //добавление
                else
                    this.$http.delete('../api/likes', {
                        //headers: {"X-CSRFToken": csrftoken},
                        params: varData,
                        headers: {'X-CSRFToken': this.$root.csrftoken}
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
        loadNextTrack() {
            var self = this
            if(this.queueTracks[1])
            {
                this.nextTrackSuccessFunc()
            }
            else
                this.$http.get('../api/tracks/next', {responseType: 'json'}).then(response => {
                    var track = response.data
                    track.auto = true
                    self.$store.commit('pushQueueTracks', track)
                    //console.log(track)
                    self.nextTrackSuccessFunc()
                })
        },
        nextTrackSuccessFunc() {         //функция успеха после получения следующего трека
            //console.log(data.body)
            
            var current = this.queueTracks[0];
            var next = this.queueTracks[1];
            this.current = current

            var logo = this.logos.logoLink;
            this.setCurrentTrackAttrs(current);
            //console.log(current, next)
            //this.track.nextID = next.id;
            this.$store.commit('removeFirstQueueTracks')     
            this.logos.prevLogoLink = logo;
            this.logos.nextLogoLink = this.queueTracks[0].image_alb;
            
            this.$bus.$emit('next-track-load', this.logos);
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
    z-index: 901;
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

