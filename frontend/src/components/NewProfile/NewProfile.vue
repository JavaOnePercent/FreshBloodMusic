<template>
    <div v-if="!error" style="width:100%; height:calc(100% - 55px); background-color: rgb(215, 215, 240);top:55px; position: relative">
        <div class="ProfileConteiner">
            <div style="width: 350px; background-color: rgba(255, 255, 255,0.6);"> 
                <UserAlbums @changeAlbum="albumId=$event" @changeAlbumLable="albumLable=$event"
                @changeAlbumName="albumName=$event" @changeAlbumGenre="albumGenre=$event" @changeAlbumDate="albumDate=$event"
                @changeAlbumStyle='albumStyle=$event' @changeAlbumType='albumType=$event'
                :deleted='deleted' @changeAlbumStatus='AlbumStatus=!$event' :playlist_created='playlist_created'
                @playlist_created='playlist_created=$event'> </UserAlbums>
            </div>
            <div class="rightColumn">
                <About :logo="logo" :name="name" :description="description"> </About>
                <TrackList  v-if="albumType !== 'AddPlaylist'" style="height: calc(100% - 275px); padding-left:15px" :albumType="albumType" :albumId="albumId" :lable="albumLable" :albumName='albumName'
                :albumGenre='albumGenre' :albumStyle='albumStyle' :albumDate='albumDate' :name='name'
                @changeDeleted='deleted=$event' :AlbumStatus='AlbumStatus'> </TrackList>
                <CreatePlayList @playlist_created='playlist_created=$event' v-else> </CreatePlayList>
            </div>
        </div>
    </div>
    <div v-else style="width:100%; height:calc(100% - 55px); background-color: rgb(215, 215, 240);top:55px; position: relative" class="error">
        <h1>Ты забрался так далеко, и ради чего?</h1>
    </div>
</template>

<script>
import UserAlbums from './UserAlbums/UserAlbums.vue'
import About from './About/About.vue'
import TrackList from './TrackList/TrackList.vue'
import CreatePlayList from './CreatePlayList/CreatePlayList.vue'
export default {
    name: 'NewProfile',
    data() {
        return {
            // albums: [],
            likes: [],
            error:false,
            name: '',
            logo: null,
            description: '',
            albumId: null,
            albumLable: null,
            albumName: '',
            albumGenre: '',
            albumStyle: '',
            albumDate: new Date(),
            albumType: '',
            deleted: null,
            AlbumStatus: true,
            playList: false,
            playlist_created: false,
        }
    },
    components: {
        UserAlbums,
        About,
        TrackList,
        CreatePlayList
    },
    watch: {
        // в случае изменения маршрута запрашиваем данные вновь
        '$route': 'receiveData'
    },
    created() {
        this.receiveData();
    },
    computed: {
        performerID() {
            return this.$store.state.performer.performerID;
        },
        myPerformerID() {
            return this.$store.state.myPerformerID;
        }
    },
    methods: {
        receiveData() {
            var id = this.$route.params.id;
            this.$http.get('../api/performers/' + id).then(function(response){
                console.log(response.body)
                // this.albums = response.body.albums
                this.$store.commit('performerID', response.body.id);
                this.name = response.body.name_per
                this.logo = response.body.image_per + '?' + Math.random()
                this.description = response.body.about_per
                this.error=false;
            }, function(error){
                this.error=true;
            });
        },
    },
}
</script>

<style scoped>
.ProfileConteiner
{
    height: 100%;
    max-width: 1143px;
    min-width: 775px;
    position: relative;
    /* top: 55px; */
    margin: 0 auto;
    display: flex;
    justify-content: center;
}
.rightColumn
{
    height: auto;
    display: flex;
    /* width: 793px; */
    padding-bottom: 55px;
    width: 60%;
    flex-direction: column;
}
.error h1
{
    margin: 0;
    top: 45px;
    display: block;
    text-align: center;
    position: relative;
}
</style>