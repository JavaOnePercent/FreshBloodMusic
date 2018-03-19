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
    data() {
        var CSSRefs = { small: "/static/mainapp/css/audioSmall.css", full: "/static/mainapp/css/audioFull.css" };
        return {
            CSSRefs: CSSRefs,
            CSSRef: CSSRefs.small,
            isFull: false,
            isHovered: false,
            progress: 0.0,
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
                playing: false,
                volume: 100
            },
            progressOptions: {
                playedTime: '',
                trackLength: ''
            }
        }
    },
    created: function() {
        this.loadNextTrack();
    },
    computed: {
        progressValue: function() {
            return this.progress * 100;
        }
    },
    methods: {
        changeProgress: function() {
            this.progressOptions.playedTime = this.$refs.audioPlayer.currentTime;
            this.progressOptions.trackLength = this.$refs.audioPlayer.duration;

            var progress = this.$refs.audioPlayer.progress;
            this.progress = progress;
            if(progress === 1)
                this.loadNextTrack();
        },
        changeVolume: function() {
            this.audio.volume = this.$refs.volumeController.value;
        },
        switchPlayerView: function() {
            if(this.isFull)
                this.CSSRef = this.CSSRefs.small;
            else
                this.CSSRef = this.CSSRefs.full;
            this.isFull = !this.isFull;
        },
        onLikePressed: function() {
            this.logos.isLiked = !this.logos.isLiked;
        },
        likeTrack: function() {
            if(this.logos.isLiked != this.track.isLiked)
            {   
                var varData = {
                    option: "",
                    current_track: this.track.currentID
                };
                varData.option = (this.logos.isLiked) ? "add" : "remove";
                this.sendJSON('like/', JSON.stringify(varData), this.successfulLikeFunc);
            }
        },
        successfulLikeFunc: function (data) {
            if (data.result === "added") {
                console.log('added');
            }
            else if (data.result === "removed") {
                console.log('removed');
            }
        },
        onMouseEnter: function() {
            this.isHovered = true;
        },
        onMouseLeave: function() {
            this.isHovered = false;
        },
        switchPlaying: function() {
            this.audio.playing = !this.audio.playing;
        },
        startPlaying: function() {
            this.audio.playing = true;
            
        },
        loadNextTrack: function() {
            this.likeTrack();
            var varData = {
                current_track: this.track.currentID,
                next_track: this.track.nextID
            };
            var jsonData = JSON.stringify(varData);
            this.sendJSON('next/', jsonData, this.nextTrackSuccessFunc);
        },
        nextTrackSuccessFunc: function (data) {         //функция успеха после получения следующего трека
            this.trackPerformer.trackName = data.body.track_name;
            this.trackPerformer.performerName = data.body.performer_name;
            this.audio.audioLink = data.body.file_link;
            this.track.currentID = data.body.current_id;
            this.track.nextID = data.body.next_id;
            document.getElementById('title').innerHTML = data.body.track_name;

            logo = this.logos.logoLink;
            this.logos.logoLink = data.body.logo_link;
            this.logos.prevLogoLink = logo;
            this.logos.nextLogoLink = data.body.nextlogo_link;

            this.track.isLiked = !!(data.body.is_liked);
            this.logos.isLiked = this.track.isLiked;
        },
        sendJSON: function (Url, jsonData, successFunc) {
            var csrftoken = this.getCookie('csrftoken');
            var config = {
                headers: {"X-CSRFToken": csrftoken}, 
                responseType: 'json'
            };
            this.$http.post(Url, jsonData, config).then(successFunc);
        },
        getCookie: function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }
});

var buttonsComponent = Vue.component('buttons', {
    template: '#buttons',
    props: [ 'playing', 'isFull' ],
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
        playClick: function() {
            this.$emit('playclick');
        },
        nextClick: function(){
            this.$emit('nextclick');
        },
        dropdownClick: function(){
            this.$emit('dropdownclick');
        }
    },
    watch: {
       playing: function(pl){
            (pl) ?
                this.buttons[0].imgSrc = this.playSrcs.pause :
                this.buttons[0].imgSrc = this.playSrcs.play;
        },
        isFull: function(iF){
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
        'progress',
        'isFull'
    ],
    data() {
        return {
            showLike: false,
            showPrev: false
        }
    },
    computed: {
        rotationCSS: function(){
            if(this.isFull)
            {
                var angle = this.progress * 360 * 3;
                return 'transform: rotate(' + angle + 'deg);'
            }
        }
    },
    watch: {
        isLiked: function(shL) {
            this.showLike = shL;
        },
        prevLogoLink: function(pr) {
            if(pr != '')
                this.showPrev = true;
        }
    },
    template: '#logos',
    methods: {
        click: function() {
            this.$emit('likepressed');
        },
        onMouseEnterMain: function() {
            if(this.isLiked === false)
                this.showLike = true;
        },
        onMouseLeaveMain: function() {
            if(this.isLiked === false)
                this.showLike = false;
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
        toggleDrop: function() {
            this.showMenu = !this.showMenu;
        },
        closeDrop: function() {
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
    props: ['isFull', 'defaultValue'],
    data() {
        var smallVolume = {direction: 'vertical', width: 12, height: 150, dotSize: 20, speed: 0.3, tooltip: 'hover'};
        var fullVolume = {direction: 'horizontal', width: 180, height: 12, dotSize: 22, speed: 0.3, tooltip: 'hover'};
        var path = '/static/mainapp/images/';
        var speakerPics = {zero: path + 'speaker0.png', thirty3: path + 'speaker33.png', sixty6: path + 'speaker66.png', hundred: path + 'speaker100.png',};
        return {
            value: this.defaultValue,
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
        isFull: function(iF){
            if(iF)
            {
                this.showVolume = false;
                this.showFullVolume = true;
            }
        },
        value: function(value) {
            localStorage.setItem("volume", this.value);
            this.$emit('volumechanged');
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
    created: function() {
        var vol = localStorage.getItem("volume");
        if(vol)
            this.value = Number(vol);
    },
    methods: {
        clickSpeaker: function() {
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
        refreshFunc: function() {
            this.$refs.fullSlider.refresh();
        },
        mouseLeave: function() {
            if(!this.isFull)
            {
                this.mouseIn = false;
                this.closeSpeaker();
            }
        },
        mouseEnter: function() {
            if(!this.isFull)
            {
                this.mouseIn = true;
            }
        },
        dragEnd: function() {
            if(!this.isFull)
            {
                this.dragging = false;
                this.closeSpeaker();
            }
        },
        dragStart: function() {
            if(!this.isFull)
            {
                this.dragging = true;
            }
        },
        openSpeaker: function() {
            if(!this.isFull)
            {
                this.showVolume = true;
                this.mouseIn = true;
            }
        },
        closeSpeaker: function() {
            if(!this.isFull && !this.dragging && !this.mouseIn)
                this.showVolume = false;
        }
    }
});

var audioComponent = Vue.component('audioPlayer', {
    template: '#audioPlayer',
    props: [
        'audioLink',
        'playing',
        'volume'
    ],
    data() {
        return {
            isFirst: true,
            timer: '',
            progress: 0.0,
            currentTime: '00:00',
            duration: '99:99'
        }
    },
    watch: {
        playing: function(pl){
            if(pl)
            {
                this.$el.play();
                this.timer = setInterval(this.updateProgress, 500); //таймер для обновления прогресса воспроизведения
            }
            else
            {
                clearInterval(this.timer);
                this.$el.pause();
            }
        },
        volume: function(vol){
            this.$el.volume = this.volume / 100;
        }
    },
    methods: {
        startPlaying: function() {
            if(!this.isFirst) {
                this.$el.play();
                this.$emit('startplaying');
            }
            else
                this.isFirst = false;
        },
        updateProgress: function() {
            this.$emit('progresschanged')
            this.progress = this.$el.currentTime / this.$el.duration;
            this.currentTime = this.$el.currentTime;
            this.duration = this.$el.duration;
        }
    }
});

Vue.component('progressBar', {
    template: '#progressBar',
    props: {
        'val': {
            default: 0
        },
        'playedTime': {
            default: ''
        },
        'trackLength': {
            default: ''
        },
        'isPlayerHovered': {}
    },
    computed: {
        pct() {
            var pct = this.val
            pct = pct.toFixed(2)
            return Math.min(pct, 100)
        },
        bar_style() {
            var style = {
                'width': this.pct+'%'
            }
            return style
        },
        showPlayedTime() {
            return this.isPlayerHovered;
        },
        showTrackLength() {
            return this.isPlayerHovered;
        },
        playedTimeTop() {
            return this.toNormalTime(this.playedTime);
        },
        trackLengthTop() {
            return this.toNormalTime(this.trackLength);
        }
    },
    methods: {
        toNormalTime(seconds) {
            mins = Math.floor(seconds / 60);
            secs = (seconds % 60).toFixed()
            return mins + ":" + ((secs < 10) ? '0' + secs : secs)
        }
    }
});

new Vue({
    el: '#VueContainer',
    components: {
        playerComponent
    }
});