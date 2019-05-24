<template>

<div style="height: calc(100% - 55px);">
<vue-custom-scrollbar class="scroll-area"  :settings="settings">
    
    <div class="userAlbumsConteiner">
        <span v-if="albums.length != 0" class="category-name"> Издания </span>
        <div class="music" >
            <div :key="index" v-for="(album, index) in albums" :class='{chousen:(albumId==album.album.id && type=="album")}' class="album"
            @click='openAlbum("album", album.album.id, album.album.image_alb, album.album.name_alb, index, album.album.genre, album.album.style, album.album.date_alb)'>
                <img :class='{dead:album.isDeleted}'  :src="album.album.image_alb">
                <span class="album-name"> {{album.album.name_alb}} </span>
            </div>
        </div>
        <span class="category-name"> Понравившаяся </span>
        <div class="music">
            <div :class='{chousen:albumId==="liked"}' class="album" @click='openAlbum("liked")'>
                <img src="/static/mainapp/images/LikeAlbum.png">
                <span class="album-name"> Мне нравится </span>
            </div>
            <div :key="playlistlike.id" v-for="(playlistlike, index) in playlistsLikes" :class='{chousen:(albumId==playlistlike.id && type=="playlistsLikes")}' class="album"
            @click='openAlbum("playlistsLikes", playlistlike.id, playlistlike.image, playlistlike.title, index)'>
                <img :src="playlistlike.image">
                <span class="album-name"> <span style="font-size: 12px; color: rgb(95, 95, 95)">Плейлист</span> <br> {{playlistlike.title}} </span>
            </div>
            <div :key="albumLike.id" v-for="(albumLike, index) in albumsLikes" :class='{chousen:(albumId==albumLike.id && type=="albumsLikes")}' class="album"
            @click='openAlbum("albumsLikes", albumLike.id, albumLike.image, albumLike.title, index)'>
                <img v-if="albumLike.image" :src="albumLike.image">
                <img v-else src="/static/mainapp/images/playlist.png" alt="">
                <span class="album-name"> <span style="font-size: 12px; color: rgb(95, 95, 95)">Альбом</span> <br> {{albumLike.title}} </span>
            </div>
        </div>
        <span class="category-name"> Плейлисты </span>
        <div class="music">
            <div :class='{chousen:albumId==="AddPlaylist"}' class="album" @click='openAlbum("AddPlaylist")'>
                <img class="addPlaylist" src="/static/mainapp/images/plus.svg">
                <span class="album-name"> Создать плейлист </span>
            </div>
            <div :key="index" v-for="(playlist, index) in playlists" :class='{chousen:(albumId==playlist.playlist.id && type=="playlist")}' class="album"
                @click='openAlbum("playlist", playlist.playlist.id, playlist.playlist.image, playlist.playlist.title, index)'>
                <img v-if="playlist.playlist.image" :class='{dead:playlist.isDeleted}'  :src="playlist.playlist.image">
                <img v-else :class='{dead:playlist.isDeleted}' src="/static/mainapp/images/playlist.png" alt="">
                <span class="album-name"> {{playlist.playlist.title}} </span>
            </div>
        </div>
    </div>

</vue-custom-scrollbar>
</div>

</template>

<script>
import vueCustomScrollbar from 'vue-custom-scrollbar'
export default {
    name: 'UserAlbums',
    props: ['deleted', 'playlist_created'],
    components: {
        vueCustomScrollbar
    },
    data() {
        return {
            albums: [],
            albumId: null,
            choseIndex: null,
            type: '',
            playlists: [],
            playlistsLikes: [],
            albumsLikes: [],
            settings: {
                maxScrollbarLength: 60,
                wheelPropagation: true,
                wheelSpeed: 0.5,
            },
            updateLiked: false
        }
    },
    watch: {
        // в случае изменения маршрута запрашиваем данные вновь
        '$route': 'getData',
        deleted: 'deleteAlbum',
        playlist_created: 'getPlaylist',
        updateLiked: 'refreshLiked'
    },
    created() {
        this.$bus.$on('updateLiked', data => {this.updateLiked = data} )
        this.getData()
    },
    computed: {
        performerID() {
            return this.$store.state.performer.performerID;
        },
    },
    methods: {
        getData() {
            this.getAlbums();
            this.getPlaylist();
            this.getPlayListLikes();
            this.getAlbumsLikes()
        },
        getAlbums() {
            var id = this.$route.params.id;
            var self = this
            this.$http.get('../api/albums?performer=' + id).then(function(response){
                self.albums = []
                response.body.map(function(item){
                    var obj = {album: item, isDeleted: false}
                    self.albums.push(obj)
                });
                if (self.albums.length >0)
                this.openAlbum('album', this.albums[0].album.id, this.albums[0].album.image_alb, this.albums[0].album.name_alb, 0,
                    this.albums[0].album.genre, this.albums[0].album.style,this.albums[0].album.date_alb); //выбирает первый альбом по умолчанию
                else
                    this.openAlbum('liked') 
            }, function(error){
                this.openAlbum('liked') 
            });
        },
        getPlaylist() {
            var id = this.$route.params.id;
            var self = this
            this.$http.get('../api/playlists?performer=' + id).then(function(response){
                this.playlists = []
                response.body.map(function(item){
                    var obj = {playlist: item, isDeleted: false}
                    self.playlists.push(obj)
                });
                self.playlists.reverse()
                if (this.playlist_created) {
                    this.$emit('playlist_created', false)
                    this.openAlbum("playlist",this.playlists[0].playlist.id, this.playlists[0].playlist.image, this.playlists[0].playlist.title, 0)
                }
            });
        },
        getPlayListLikes() {
            var id = this.$route.params.id;
            var self = this
            this.$http.get('../api/playlist_likes?performer=' + id).then(function(response){
                this.playlistsLikes = []
                response.body.map(function(item){
                    self.playlistsLikes.push(item)
                });
            });
        },
        getAlbumsLikes() {
            var id = this.$route.params.id;
            var self = this
            this.$http.get('../api/album_likes?performer=' + id).then(function(response){
                this.albumsLikes = []
                response.body.map(function(item){
                    self.albumsLikes.push(item)
                });
            });
        },
        openAlbum(type ,id, lable, name, index, genre, style, date) {
            this.choseIndex = index
            this.type = type

            if (type === 'liked')
            {
                this.albumId = type
                this.$emit('changeAlbumType', type)
                this.$emit('changeAlbumLable', '/static/mainapp/images/LikeAlbum.png')
                this.$emit('changeAlbumName', 'Мне нравится')
                this.$emit('changeAlbumStatus', false)
            }
            else if (type === 'playlistsLikes' || type === 'albumsLikes')
            {
                this.albumId = id
                this.$emit('changeAlbumType', this.type)
                this.$emit('changeAlbum', id)
                this.$emit('changeAlbumLable', lable)
                this.$emit('changeAlbumName', name)
                this.$emit('changeAlbumStatus', false)
            }
            else if (type === 'AddPlaylist')
            {
                this.albumId = type
                this.$emit('changeAlbumType', type)
            }
            else if (type === 'playlist')
            {
                this.albumId = id;
                this.$emit('changeAlbumType', type)
                this.$emit('changeAlbum', id)
                this.$emit('changeAlbumLable', lable)
                this.$emit('changeAlbumName', name)
                this.$emit('changeAlbumStatus', this.playlists[index].isDeleted)              
            }
            else if (type === 'album')
            {
                this.albumId = id;
                this.$emit('changeAlbumType', type)
                this.$emit('changeAlbum', id)
                this.$emit('changeAlbumLable', lable)
                this.$emit('changeAlbumName', name)
                this.$emit('changeAlbumGenre', genre)
                this.$emit('changeAlbumStyle',style)
                this.$emit('changeAlbumDate', date)
                this.$emit('changeAlbumStatus', this.albums[index].isDeleted)
            }
        },
        deleteAlbum() {
            var mass = []
            switch (this.type) {
                case 'album':
                    mass = this.albums
                    break;
                case 'playlist':
                    mass = this.playlists
                    break;
                }
            if( this.deleted !== null )
            mass[this.choseIndex].isDeleted = true;
        },
        refreshLiked() {
            if(!this.updateLiked)
                return
            else {
                if(this.type === 'playlistsLikes' || this.type === 'albumsLikes')
                    this.openAlbum('liked')
                this.getPlayListLikes();
                this.getAlbumsLikes();
                this.updateLiked = false
            }
        },
    }
}
</script>

<style scoped src="./UserAlbums.css">
</style>