

var playerComponent = Vue.component('topPlayer', {
    template: '#topPlayer',
    /*components:{
        buttonsComponent,
        logosComponent,
        menuMoreComponent,
        trackPerformerComponent,
        volumeControllerComponent,
        progressBarComponent,
        audioComponent
    },*/
    store,
    data() {
        var CSSRefs = { small: "/static/mainapp/css/audioSmall.css", full: "/static/mainapp/css/audioFull.css" };
        return {
            CSSRefs: CSSRefs,
            CSSRef: CSSRefs.small,
            isFull: false,
            isHovered: false,
            containerMove: '',
            track: {
                currentID: null,
                nextID: null,
                isLiked: false
            },
            logos: {
                logoLink: '',
                nextLogoLink: '',
                prevLogoLink: '',
                isLiked: false
            },
            trackPerformer: {
                trackName: '',
                performerName: ''
            },
            audio: {
                audioLink: '',
            },
            queue: {
                tracks: []
            },
            HTTPConfig: '',
            isTimeout: false
        }
    },
    
    created() {
        this.loadNextTrack();
        bus.$on('trackclicked', event => {
            //this.playNow(event.id);
            this.getTrackAttributes(event.id);
            
        });
        /*this.getTrackAttributes(3);
        this.getTrackAttributes(4);
        this.getTrackAttributes(5);
        this.getTrackAttributes(6);
        this.getTrackAttributes(3);
        this.getTrackAttributes(4);
        this.getTrackAttributes(5);
        this.getTrackAttributes(6);
        this.getTrackAttributes(5);
        this.getTrackAttributes(6);*/
    },
    methods: {
        /*playNow(id) {
            this.track.nextID = id;
            this.loadNextTrack();
        },*/
        moveContainer() {
            if (this.containerMove === '')
            {
                var dist = document.body.offsetWidth / 2 - 675;
                this.containerMove = (dist < 0) ? ('left: ' + ((dist-10) * 2) + 'px') : '';
            }
            else
                this.containerMove = '';
        },
        getTrackAttributes(id) {
            var varData = {
                id: id
            };
            this.$http.get('track_attr', {
                responseType: 'json',
                params: varData
            }).then(response => {
                this.queue.tracks.push(response.data);
                this.track.nextID = id;
                this.loadNextTrack();
            });
        },
        switchPlayerView() {
            if(this.isFull)
                this.CSSRef = this.CSSRefs.small;
            else
                this.CSSRef = this.CSSRefs.full;
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
                    this.$http.put('like', {}, {
                        //headers: {"X-CSRFToken": csrftoken},
                        params: varData
                    }).then(this.successfulLikeFunc); //добавление
                else
                    this.$http.delete('like', {
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
        loadNextTrack() {
            if(!this.isTimeout)
            {
                this.isTimeout = true;
                setTimeout(this.nextTrackTimeout, 1000);
                //this.likeTrack();
                var varData = {
                    current_track: this.track.currentID,
                    next_track: this.track.nextID
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

            this.trackPerformer.trackName = current.name_trc;
            this.trackPerformer.performerName = current.name_per;//
            this.audio.audioLink = (current.audio_trc);//toStatic(current.link_trc);
            //console.log(current.audio_file);
            this.track.currentID = current.id;
            this.track.nextID = next.id;
            document.getElementById('title').innerHTML = current.name_per + " - " + current.name_trc;

            logo = this.logos.logoLink;
            this.logos.logoLink = (current.image_alb);
            this.logos.prevLogoLink = logo;
            this.logos.nextLogoLink = (next.image_alb);

            this.track.isLiked = !!(current.is_liked);
            this.logos.isLiked = this.track.isLiked;
            bus.$emit('next-track-load');
        }
    }
});

var buttonsComponent = Vue.component('buttons', {
    template: '#buttons',
    props: [ 'isFull' ],
    data() {
        var playSrcs = {play: '/static/mainapp/images/playButton.png', pause: '/static/mainapp/images/pauseButton.png'};
        var dropdownSrcs = {drop: '/static/mainapp/images/dropdown.png', close: '/static/mainapp/images/closeDropdown.png'};
        return {
            playSrcs: playSrcs,
            dropdownSrcs: dropdownSrcs,
            buttons: [
                {id:'playButton', imgSrc: playSrcs.play, click: this.playClick},
                {id:'nextButton', imgSrc: '/static/mainapp/images/nextButton.png', click: this.nextClick},
                {id:'dropdown', imgSrc: dropdownSrcs.drop, click: this.dropdownClick}
            ]
        }
    },
    methods: {
        playClick() {
            this.$store.commit('switchPlaying');
        },
        nextClick(){
            this.$emit('nextclick');
            bus.$emit('nextclick');
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
                this.buttons[0].imgSrc = this.playSrcs.pause :
                this.buttons[0].imgSrc = this.playSrcs.play;
        },
        isFull(iF){
            (iF) ?
                this.buttons[2].imgSrc = this.dropdownSrcs.close :
                this.buttons[2].imgSrc = this.dropdownSrcs.drop;
        }
    }
});

var logosComponent = Vue.component('logos', {
    props:[
        'logoLink',
        'nextLogoLink',
        'prevLogoLink',
        'isLiked',
        'isFull',
    ],
    template: '#logos',
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
            nextLogo: '',
            prevLogo: '',
            lastRotation: '',
            wasPlaying: false
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
        bus.$on('nextclick', event => {
            this.lastRotation = this.audio.currentTime/this.audio.duration * 1080;
            this.wasPlaying = this.playing;
        });
        bus.$on('playingended', event => {
            this.lastRotation = this.audio.currentTime/this.audio.duration * 1080;
            this.wasPlaying = true;
        });
        bus.$on('startplaying', event => {
            this.rotate(false, 0);
            //console.log(this.rotationCSS);
            if(this.wasPlaying)
            {
                this.rotate(false, 0.1/this.audio.duration * 1080);
                setTimeout(this.rotate, 100, true, 1080, this.audio.duration - this.audio.currentTime);
            }
        });
        bus.$on('next-track-load', event => {
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
        startAnimation() {
            setTimeout(this.endAnimation, 800);
            this.mainToPrevLogoAnimation += 'left: -100%; height: 150px; width: 150px; transition: left 0.8s, height 0.3s, width 0.3s;';
            this.nextToMainLogoAnimation = {right: 0, transition: 'right 0.8s'}; 
            setTimeout(this.startExpandingNextToMain, 500);
            
            this.prevEnvelopeAnimation = {top: '-50%', opacity: '1.0', transition: 'top 0.3s, opacity 0.3s'};
            this.prevLogoAnimation = 'left: -150%; opacity: 0.0; transition: left 0.5s, opacity 0.5s;';
            this.nextLogoAnimation = 'right: -150%; opacity: 0.0;';
            setTimeout(this.moveNextEnvelope, 500);
        },
        endAnimation() {
            
            this.nextLogo = this.nextLogoLink;
            this.prevLogo = this.prevLogoLink;
            this.mainToPrevLogoAnimation = 'visibility:hidden;';
            this.nextToMainLogoAnimation = 'visibility:hidden;'
            this.mainLogoAnimation = '';
            //this.prevEnvelopeAnimation = 'visibility:hidden;';
            this.prevEnvelopeAnimation.opacity = 0.0;
            this.prevEnvelopeAnimation.transition = 'opacity 0.1s';
            setTimeout(this.hidePrevEnvelope, 100);
            this.prevLogoAnimation = '';
            this.nextEnvelopeAnimation = 'visibility:hidden;';
        },
        hidePrevEnvelope() {
            this.logo = this.logoLink;
            this.prevEnvelopeAnimation = 'visibility:hidden;';
        },
        startExpandingNextToMain(){
            this.nextToMainLogoAnimation.transition += ', height 0.3s, width 0.3s';
            this.nextToMainLogoAnimation.height = '250px';
            this.nextToMainLogoAnimation.width = '250px';
        },
        moveNextEnvelope() {
            this.nextEnvelopeAnimation.top = '-90%';
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
                    this.rotate(true, 1080, time=(this.audio.duration - this.audio.currentTime));
                else
                    this.rotate(false, this.audio.currentTime/this.audio.duration * 1080);
            }
        },
        rotate(animation, angle, time=0) {
            if(this.isFull)
                this.rotationCSS = 'transform: rotate(' + angle + 'deg);' + ((animation) ? 'transition: transform ' + time + 's linear;' : '');
        }
    }
});

var menuMoreComponent = Vue.component('menuMore', {
    template: '#menuMore',
    data() {
        return {
            menuElements: ['На страницу исполнителя', 'Добавить в избранное', 'Пожаловаться'],
            showMenu: false
        }
    },
    methods: {
        toggleDrop() {
            this.showMenu = !this.showMenu;
        },
        closeDrop() {
            this.showMenu = false;
        }
    }
});

var trackPerformerComponent = Vue.component('trackPerformer', {
    template: '#trackPerformer',
    props: [
        'trackName',
        'performerName'
    ]
});

var volumeControllerComponent = Vue.component('volumeController', {
    template: '#volumeController',
    props: ['isFull'],
    data() {
        var smallVolume = {direction: 'vertical', width: 12, height: 150, dotSize: 20, speed: 0.3, tooltip: 'hover'};
        var fullVolume = {direction: 'horizontal', width: 180, height: 12, dotSize: 22, speed: 0.3, tooltip: 'hover'};
        var path = '/static/mainapp/images/';
        var speakerPics = {zero: path + 'speaker0.png', thirty3: path + 'speaker33.png', sixty6: path + 'speaker66.png', hundred: path + 'speaker100.png',};
        return {
            value: 100,
            showVolume: false,
            showFullVolume: false,
            sliderprops: smallVolume,
            sliderpropsFull: fullVolume,
            dragging: false,
            mouseIn: false,
            speakerPic: speakerPics.hundred,
            speakerPics: speakerPics
        }
    },
    watch: {
        isFull(iF){
            if(iF)
            {
                this.showVolume = false;
                this.showFullVolume = true;
            }
        },
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
            this.$refs.fullSlider.refresh();
        },
        mouseLeave() {
            if(!this.isFull)
            {
                this.mouseIn = false;
                this.closeSpeaker();
            }
        },
        mouseEnter() {
            if(!this.isFull)
            {
                this.mouseIn = true;
            }
        },
        dragEnd() {
            if(!this.isFull)
            {
                this.dragging = false;
                this.closeSpeaker();
            }
        },
        dragStart() {
            if(!this.isFull)
            {
                this.dragging = true;
            }
        },
        openSpeaker() {
            if(!this.isFull)
            {
                this.showVolume = true;
                this.mouseIn = true;
            }
        },
        closeSpeaker() {
            if(!this.isFull && !this.dragging && !this.mouseIn)
                this.showVolume = false;
        }
    }
});

var audioComponent = Vue.component('audioPlayer', {
    template: '#audioPlayer',
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
            bus.$emit('playingended');
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
                bus.$emit('startplaying');
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
});

Vue.component('progressBar', {
    template: '#progressBar',
    props: [
        'isPlayerHovered',
        'isFull'
    ],
    data() {
        return {
            lastValue: 0,
            //duration: 0.0,
            sliderPropsFull: {
                width: '100%',
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
                    mins = Math.floor(v / 60);
                    secs = (v % 60).toFixed();
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
                    "background-color": "rgb(0,0,0)"
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
                    mins = Math.floor(v / 60);
                    secs = (v % 60).toFixed();
                    return mins + ":" + ((secs < 10) ? '0' + secs : secs);
                    }
            }
        }
    },
    /*created() {
        bus.$on('progresschanged', event => {
            this.progress = event.progress;
            this.duration = event.duration.toFixed();
        });
        bus.$on('startplaying', event => {
            this.$refs.slider.refresh();
        });
    },*/
    /*mounted() {
        var el = this.$refs.slider.$refs.wrap;
        el.setAttribute('style', "width: 100%;");
    },*/
    computed: {
        sliderPropsComputed() {
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
});

Vue.component('queue', {
    template: '#queue',
    props: ['tracks'],
    data() {
        return {
            showQueue: false,
            tracksComputed: []
        }
    },
    methods: {
        image(src) {
            return toStatic(src);
        },
        openQueue() {
            this.$emit('queue-opened');
            this.showQueue = !this.showQueue;
        },
        mouseEnterElement(index) {
            this.tracksComputed[index].text = this.tracks[index].name_per;
            this.tracksComputed[index].style = 'color: white;';
        },
        mouseLeaveElement(index) {
            this.tracksComputed[index].text = this.tracks[index].name_trc;
            this.tracksComputed[index].style = '';
        },
        iterator(item, i, arr) {
            this.$set(this.tracksComputed, i, {img: item.image_alb, text: item.name_trc, style: ''})
            //Vue.set(this.tracksComputed[i], 'img', item.image_alb);
            //Vue.set(this.tracksComputed[i], 'text', item.name_trc);
        }
    },
    watch: {
        tracks(tracks) {
            /*for(var i = 0; i < tracks.length - this.tracksComputed.length; i++)
            {
                this.tracksComputed.push({});
            }*/
            tracks.forEach(this.iterator);
        }
    }
});

new Vue({
    el: '#VueContainer',
    data:{
        menuShow:false,
    },
    store,
        //bus: bus // Here we bind our event bus to our $root Vue model.
    computed: {
        showModel () {
            return this.$store.state.showModel
        }
    },
    methods:
    {
        show() {
            this.$store.commit("showModel", true)
        }
    }
});