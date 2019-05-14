<template>

<div style="height: calc(100% - 55px);">
<vue-custom-scrollbar class="scroll-area"  :settings="settings">
    
    <div class="userAlbumsConteiner">
        <span class="category-name"> Издания </span>
        <div class="music" >
            <div :key="index" v-for="(album, index) in albums" :class='{chousen:(albumId==album.album.id && type=="album")}' class="album"
            @click='openAlbum("album", album.album.id, album.album.image_alb, album.album.name_alb, index, album.album.genre, album.album.style, album.album.date_alb)'>
                <img :class='{dead:album.isDeleted}'  :src="album.album.image_alb">
                <span class="album-name"> {{album.album.name_alb}} </span>
            </div>
        </div>
        <span class="category-name"> Понравившаяся </span>
        <div :class='{chousen:albumId==="liked"}' class="album" @click='openAlbum("liked")'>
            <img src="/static/mainapp/images/LikeAlbum.png">
            <span class="album-name"> Мне нравится </span>
        </div>
        <span class="category-name"> Плейлисты </span>
        <div class="music">
            <div :class='{chousen:albumId==="AddPlaylist"}' class="album" @click='openAlbum("AddPlaylist")'>
                <img class="addPlaylist" src="/static/mainapp/images/plus.svg">
                <span class="album-name"> Создать плейлист </span>
            </div>
            <div :key="index" v-for="(playlist, index) in playlists" :class='{chousen:(albumId==playlist.playlist.id && type=="playlist")}' class="album"
                @click='openAlbum("playlist", playlist.playlist.id, playlist.playlist.image, playlist.playlist.title, index)'>
                <img :class='{dead:playlist.isDeleted}'  :src="playlist.playlist.image">
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
            settings: {
                maxScrollbarLength: 60,
                wheelPropagation: true,
                wheelSpeed: 0.2,
            },
        }
    },
    watch: {
        // в случае изменения маршрута запрашиваем данные вновь
        '$route': 'getAlbums',
        deleted: 'deleteAlbum',
        playlist_created: 'getPlaylist'
    },
    created() {
        this.getAlbums();
        this.getPlaylist()
    },
    computed: {
        performerID() {
            return this.$store.state.performer.performerID;
        },
    },
    methods: {
        getAlbums() {
            var id = this.$route.params.id;
            var self = this
            this.$http.get('../api/albums?performer=' + id).then(function(response){
                console.log(response.body)
                self.albums = []
                response.body.map(function(item){
                    var obj = {album: item, isDeleted: false}
                    self.albums.push(obj)
                });
                this.openAlbum('album', this.albums[0].album.id, this.albums[0].album.image_alb, this.albums[0].album.name_alb, 0,
                    this.albums[0].album.genre, this.albums[0].album.style,this.albums[0].album.date_alb); //выбирает первый альбом по умолчанию
                console.log(this.albums)
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
        openAlbum(type ,id, lable, name, index, genre, style, date) {
            this.choseIndex = index
            this.type = type
            if(type === 'liked')
            {
                this.albumId = type
                this.$emit('changeAlbumType', type)
                this.$emit('changeAlbumLable', '/static/mainapp/images/LikeAlbum.png')
                this.$emit('changeAlbumName', 'Мне нравится')
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
            else if (this.albumId !== id)
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
            console.log('a')
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
        }
    }
}
</script>

<style scoped src="./UserAlbums.css">
</style>