<template>
    <div v-if="status==='alive'" class="trackListConteiner">
        <div class="album-header" >
            <div class="blur" :style="{backgroundImage: getUrlAlbum()}"> 
            </div>
            <div class="about">
                <img v-if="lable" class="lable" :src="lable" alt="">
                <img v-else class="lable" src="/static/mainapp/images/playlist.png" alt="">
                <div style="display:flex; flex-direction: column; left: 30px; position:relative; width: calc(100% - 183px);">
                    <span class="name"> {{albumName}} </span>
                    <span v-if="albumType === 'album' || albumType === 'albumsLikes'" class="genre"> {{albumGenre}} • {{albumStyle}} </span>
                    <span v-else class="author">Автор плейлиста: {{name}} </span>
                    <span v-if="albumType === 'album' || albumType === 'albumsLikes'" class="date">Исполнитель: {{name}} • {{getCorrectDate(albumDate)}} </span>
                    <span v-else class="date"> </span>
                    <span class="more"> {{length}} </span>
                    <div style="display:flex; position:relative; height: 50px;">
                        <div @click="playAlbum(album)" class="playAll"> 
                            <span> Проигрывать весь альбом </span>
                        </div>
                        <div v-if="albumType !== 'liked'" class="heart" :class="{AlbumLiked:Liked}" @click="LikeAlbumAndPlaylist()"> 
                            <img v-if='!Liked' src="/static/mainapp/images/white-heart.svg">
                            <img v-else src="/static/mainapp/images/orange heart.svg">
                        </div>
                        <div v-if="albumType !== 'liked' && albumType !== 'playlistsLikes' && albumType !== 'albumsLikes' && this.$route.path !== '/' && this.$route.params.id == this.$store.state.myPerformerID " v-click-outside="changeShowMenu" id="menu" style="display:flex; position:relative; height: 50px;">
                            <img class="menu" src="/static/mainapp/images/menu.svg" alt="больше" @click="showMenu = !showMenu">
                            <div v-show="showMenu">
                                <ul  class="menu-dropdown" :key="index" v-for="(elem, index) in menu" >
                                    <li @click="DelateConfirmation">
                                        {{albumType==='album'?'Удалить альбом':'Удалить плейлист'}}
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <vue-custom-scrollbar id='father' class="scroll-area"  :settings="settings">
            <div class="music">
                <span style="width: 100%; text-alaight:center; display: block; text-align: center;" v-if="album.length === 0 && albumType === 'liked'">
                    Неужели вам ничего не нравится? <br> Просто нажмите на сердечко рядом с понравившейся вам копозицией!
                </span>
                <div :class="{currentTrc:current_trc===index}" class="track" :key="index" v-for="(track, index) in album" @click="playClick(track.id)">
                    <div v-if="track.img_trc" class="trc-logo"> 
                        <img :src="track.img_trc" alt="">
                    </div>
                    <img v-else class="play" src="/static/mainapp/images/orange-arrow.svg" alt="">
                    <span class="track-name" > {{track.performer || name}} — {{track.name_trc}}</span>
                    <span class="time"> {{getCorrectTime(track.duration)}} </span>
                    <div class="trc-controll">
                        <span class="trc-controll-btn like" @click.stop="likeTrack(track, index)">
                            <img v-if="!track.is_liked && albumType !== 'liked'" src="/static/mainapp/images/empty-heart.svg" title="мне нравится">
                            <img v-else src="/static/mainapp/images/heart.svg" title="мне нравится">
                        </span>
                        <span class="trc-controll-btn like" @click.stop="gotoSimilar(track.id, track.name_trc); $emit('close')">
                            <img src="/static/mainapp/images/similar.svg" title="показать похожие" >
                        </span>
                        <span class="trc-controll-btn add-to-playlist" @click.stop="current_trc=current_trc===index?null:index">
                            <img src="/static/mainapp/images/plus.svg" title="добавить в плейлист" >
                        </span>
                        <span class="trc-controll-btn trash" v-if="albumType === 'playlist'" @click.stop="deleteTrcOfPlaylist(track.id, index)">
                            <img src="/static/mainapp/images/trash.svg" title="удалить">
                        </span>
                    </div>
                    <user-playlists @close="current_trc=null" :trc_id='track.id' v-click-outside="changeUser_playlists" v-if="current_trc===index"> </user-playlists>
                </div>
            </div>
        </vue-custom-scrollbar>
        <DelateConfirmation v-if="showDelateConfirmation" @close="showDelateConfirmation = false"
        :albumType="albumType" :albumName='albumName' :albumId='albumId' @changeStatus="status=$event"> </DelateConfirmation>
        <svg style="display: none" xmlns="http://www.w3.org/2000/svg"  version="1.1">
            <defs>
                <filter id="blur">
                    <feGaussianBlur stdDeviation="25"/>
                </filter>
            </defs>
        </svg>
    </div>
    <div v-else style="width:100%; position:relative;">
        <img class="smile" src="/static/mainapp/images/dead_icon.svg" alt="">
        <span style="width:100%; font-size: 25px; text-align: center; display:block; cursor: default"> {{getAlbumName}} был удалён </span>
    </div>
</template>

<script>
import DelateConfirmation from './DelateConfirmation/DelateConfirmation.vue'
import userPlaylists from '../../../components/userPlaylists/userPlaylists.vue'
import vueCustomScrollbar from 'vue-custom-scrollbar'
export default {
    name: 'trackList',
    props: ['albumType', 'albumId', 'lable', 'AlbumStatus', 'albumName'],
    data() {
        return {
            album: [],
            length: null,
            menu : [
                { name: 'Удалить альбом', event: DelateConfirmation},
            ],
            showMenu: false,
            showDelateConfirmation: false,
            status: 'alive',
            user_playlists: false,
            current_trc: null,
            settings: {
                maxScrollbarLength: 60,
                wheelPropagation: true,
                wheelSpeed: 0.2,
            },
            _albumName: this.albumName,
            name: '',
            albumGenre: '',
            albumStyle: '',
            albumDate: new Date(),
            Liked: false
        }
    },
    computed: {
        getAlbumName() {
            var str =''
            switch (this.albumType) {
                case 'album':
                    str = 'Альбом '
                    break;
                case 'playlist':
                    str = 'Плейлист '
                    break;
                }
            return str + '\"' + this.albumName + '\"'
        },
    },
    components: {
        DelateConfirmation,
        userPlaylists,
        vueCustomScrollbar
    },
    watch: {
        albumType: 'getData',
        albumId: 'getData',
        status: 'changeDeleted'
    },
    created() {
        this.current_trc = null
        if (this.AlbumStatus)
        {
            this.getData();
        }
    },
    methods: {
        getData() {
            console.log('чо')
            this.status = 'alive'
            if (!this.AlbumStatus)
            {
                this.status = 'dead'
                return
            }
            switch (this.albumType) {
                case 'album':
                    this.albumType = 'album'
                    this.getAlbum()
                    break;
                case 'liked':
                    this.albumType = 'liked'
                    this.getLiked()
                    break;
                case 'playlist':
                    this.albumType = 'playlist'
                    this.getPlaylist()
                    break;
                case 'playlistsLikes':
                    this.albumType = 'playlistsLikes'
                    this.getPlaylist()
                    break;
                case 'albumsLikes':
                    this.albumType = 'albumsLikes'
                    this.getAlbum()
                    break;
                }
        },
        getAlbum() {
            var self = this
            this.$http.get('../api/albums/' + this.albumId).then(function(response){
                    this.albumGenre = response.body.genre
                    this.albumStyle = response.body.style
                    this.albumDate = response.body.date_alb
                    this.albumName = response.body.name_alb
                    this.name = response.body.name_per
                console.log('music',response.body)
                self.album = []
                self.Liked = response.body.is_liked
                response.body.tracks.map(function(item){
                    self.album.push(item)
                });
                this.albumLength(self.album)
                console.log(self.album)
            }, function(error){});
        },
        getLiked() {
            var id = this.$route.params.id;
            this.$http.get('../api/likes', {params: {performer: id}}).then(function(response){
                this.albumName = 'Мне нравится'
                this.name = this.$store.state.username
                console.log(response.body)
                this.album = []
                for(var i = 0; i < response.body.length; i++)
                {
                    this.album.push({name_trc: response.body[i].name_trc, performer: response.body[i].name_per,
                    logo:response.body[i].image_alb, id:response.body[i].trc_id, img_trc: response.body[i].image_alb,
                    duration: response.body[i].duration, is_liked: response.body[i].is_liked})
                }
                this.albumLength(this.album)
                console.log(this.album)
            });
        },
        getPlaylist() {
            var self = this
            console.log('playlists')
            this.$http.get('../api/playlists/' + this.albumId).then(function(response){
                console.log(response.body)
                this.albumName = response.body.title
                this.name = response.body.name_per
                self.Liked = response.body.is_liked
                self.album = []
                response.body.tracks.map(function(item) {
                    self.album.push({name_trc: item.track.name_trc, performer: item.track.name_per,
                    logo: item.track.image_alb, id: item.track.id, img_trc: item.track.image_alb, duration: item.track.duration,
                    trc_playlist_id:item.id, is_liked: item.track.is_liked})
                });
                this.albumLength(self.album)
            });
        },
        getUrlAlbum() {
            if (this.lable)
                return 'url(' + this.lable + ')'
            else 
                return 'url(/static/mainapp/images/playlist.png)'
        },
        albumLength(mass) {
            if (mass.length > 1)
                this.length = mass.length + ' композиции'
            else if (mass.length >= 5 && mass.length<=19)
                this.length = mass.length + ' композиций'
            else if (mass.length % 10 === 0)
                this.length = 'нет композиций'
            else if (mass.length % 10 === 1)
                this.length = mass.length + ' композиция'
        },
        getCorrectDate(date) {
            var months = ['января', 'февраля', 'марта', 'апреля','мая', 'июня', 'июля', 'августа','сентября', 'октября', 'ноября', 'декабря'];
            var D = new Date(date)
            return D.getDate() + ' ' + months[D.getMonth()] + ' ' + D.getFullYear()
        },
        playAlbum(tracks) {
            console.log(tracks)
            for(var i = 1; i < tracks.length; i++)
            {
                this.$bus.$emit('track-to-queue', tracks[i])
            }
            this.$bus.$emit('play-track', tracks[0])
            
        },
        changeShowMenu() {
            this.showMenu = false
        },
        DelateConfirmation() {
           this.showDelateConfirmation=true 
        },
        changeDeleted() {
            // this.$emit('updateLiked', true)
            if(this.status == 'dead')
            this.$emit('changeDeleted', this.albumId)
        },
        getCorrectTime(sec) {
            var m = Math.floor(sec / 60)
            var s = sec % 60
            if(s < 10) {s= '0' + s}
            return m + ':' + s
        },
        playClick: function(index) {
            console.log(index)
            this.$bus.$emit('play-track', {
				id: index
			});
        },
        changeUser_playlists() {
            this.current_trc = null;
        },
        deleteTrcOfPlaylist(trac_id, index) {
            var self = this
            this.$http.delete('../api/playlist_tracks?playlist=' + this.albumId + '&track=' + trac_id).then(function(response){
                console.log('спасибо папаша')
                this.$bus.$emit('likeNot', 'вы удалили песню из плейлиста ' + this.albumName)
                this.album.splice(index, 1)
                this.albumLength(this.album)
            });
        },
        likeTrack(track, index) {
            switch (this.albumType) {
                case 'liked':
                    this.dislike(track, index)
                    if (this.$route.params.id == this.$store.state.myPerformerID)
                        this.album.splice(index, 1)

                    this.albumLength(this.album)
                    break;
                default:
                    if(!track.is_liked)
                        this.like(track, index)
                    else
                        this.dislike(track, index)
            }
        },
        like(track, index) {
            this.$http.put('../api/likes', {}, {
                params: {track_id: track.id},
            }).then(function(response){
                this.album[index].is_liked = true
                this.$bus.$emit('likeNot', 'вам понравилась песня ' + this.album[index].name_trc) //лайк
            }); 
        },
        dislike(track, index) {
            this.$http.delete('../api/likes', {
                params: {track_id: track.id},
            }).then(function(response){
                this.album[index].is_liked = false
                this.$bus.$emit('likeNot', 'вам больше не нравится ' + this.album[index].name_trc) //лайк
            }); 
        },
        LikeAlbumAndPlaylist() {
            var url
            switch (this.albumType) {
                case 'album':
                    url = '../api/album_likes?album='
                    break;
                case 'playlist':
                    url = '../api/playlist_likes?playlist='
                    break;
                case 'albumsLikes':
                    url = '../api/album_likes?album='
                    break;
                case 'playlistsLikes':
                    url = '../api/playlist_likes?playlist='
                    break
            }
            if (this.Liked)
                this.AlbumDislike(url)
            else
                this.AlbumLiked(url)

        },
        AlbumLiked(url) {
            this.$http.post(url + this.albumId)
            .then(function(response){
                this.Liked = true
                // this.$emit('updateLiked', true)
                this.$bus.$emit('updateLiked', true)
                this.$bus.$emit('likeNot', 'вам понравился плейлист ' + this.albumName) //лайк
            }); 
        },
        AlbumDislike(url) {
            this.$http.delete(url + this.albumId)
            .then(function(response){
                this.Liked = false
                // this.$emit('updateLiked', true)
                this.$bus.$emit('updateLiked', true)
                this.$bus.$emit('likeNot', 'вам больше не нравится ' + this.albumName) //лайк
            }); 
        },
        gotoSimilar(id, name) {
            this.$router.push('/similar')
            this.$store.commit("updateSimilar", id)
            this.$store.commit("updateSimilarName", name)
            this.$bus.$emit('Similar', id)
            this.$bus.$emit('SimilarName', name)
        }
    }
}
</script>

<style scoped src="./TrackList.css">
</style>