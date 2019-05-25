<template>
    <div class="userPlaylists-Conteiner">
        <vue-custom-scrollbar id="inside" class="scroll-area"  :settings="settings">
            <ul v-if='userPlaylists.length > 0'  class="menu-dropdown">
                <li :key="index" v-for="(userPlaylist, index) in userPlaylists" @click="putToUserPlaylist(userPlaylist.id, index); $emit('close')">
                {{userPlaylist.title}} 
                <span class="tick" v-if='AddedTo(userPlaylist.id)' @click.stop=""> {{userPlaylist.title}} <img src="/static/mainapp/images/tick.svg"> </span>
                <img v-else class="plus" src="/static/mainapp/images/orange_plus.svg">
                </li>
            </ul>
            <ul v-else  class="menu-dropdown"><li @click="$emit('close')">Вы можете создать плейлист в своём профиле в разделе "плейлисты"</li></ul> 
        </vue-custom-scrollbar>
    </div>
</template>

<script>
import vueCustomScrollbar from 'vue-custom-scrollbar'
export default {
    name: 'userPlaylists',
    props: ['trc_id'],
    data() {
        return {
            userPlaylists: [],
            trcPlaylists: [],
            settings: {
                maxScrollbarLength: 60,
                wheelPropagation: true,
                wheelSpeed: 0.2,
            },
        }
    },
    components: {
        vueCustomScrollbar
    },
    created() {
        this.getUserPlaylist();
        this.getTrcPlaylist()
    },
    mounted() {
        this.getCoordinate()
    },
    methods: {
        getUserPlaylist() {  //получение списка плейлистов пользователя
            var id = this.$store.state.myPerformerID;
            var self = this
            this.$http.get('../api/playlists?performer=' + id).then(function(response){
                this.userPlaylists = []
                response.body.map(function(item){
                    self.userPlaylists.push(item)
                });
            });
        },
        putToUserPlaylist(id, index) {
            console.log(this.trc_id)
            var self = this
            this.$http.post('../api/playlist_tracks?playlist=' + id + '&track=' + this.trc_id).then(function(response){
                console.log('спасибо папаша')
                this.$bus.$emit('likeNot', 'вы добавили песню в плейлист ' + this.userPlaylists[index].title)
            });
        },
        getCoordinate() {
            if(document.getElementById('father'))
            {
                var obj = document.getElementById('inside');
                var main = document.getElementById('father'); 
                var luk = main.getElementsByClassName('currentTrc')
                if (175 - luk[0].offsetTop > 0)
                    obj.style.top = '45px'
            }
            else document.getElementById('inside').style.top = '45px'
        },
        getTrcPlaylist() {
            var id = this.$store.state.myPerformerID;
            var self = this
            this.$http.get('../api/playlists?performer=' + id + "&track=" + this.trc_id).then(function(response){
                this.trcPlaylists = []
                response.body.map(function(item){
                    self.trcPlaylists.push(item.id)
                });
            });
        },
        AddedTo(playlist_id) {
            var result = false
            this.trcPlaylists.map(function(item) {
                if (playlist_id === item)
                    result = true
            })
            return result
        },
    }
}
</script>

<style scoped>
.menu-dropdown 
{
    padding: 0;
    margin: 0; 
}
.menu-dropdown li
{
    list-style-type: none;
    padding: 10px 40px 10px 5px;
    cursor: pointer;
    position:relative;
}
.menu-dropdown li:hover
{
    background-color: rgba(189, 176, 208, 0.3);
    background-color: rgba(255, 181, 43, 0.3)
}
.tick
{
    width: 263px;
    height: 100%;
    box-sizing: border-box;
    position: absolute;
    cursor: default;
    top: 0;
    left: 0;
    padding: 10px 40px 10px 5px;
    color: rgba(0,0,0,0.6);
    background-color: white;
    border-bottom: 1.5px solid rgba(255, 181, 43)
}
.tick img, .plus
{
    width: 28px;
    height: 28px;
    position: absolute;
    top: 5px;
    bottom: 0;
    right: 5px;
}
.plus
{
    display: none;
}
.menu-dropdown li:hover .plus
{
    display: block;
}
.tick:hover ~ li
{
    background-color: white;
}
.scroll-area {
    position: absolute;
    /* outline: none; */
    height: auto;
    /* top: auto; */
    overflow: visible;
    visibility: visible; clear:both;
    top: -85px;
    width: 263px;
    padding: 0;
    margin: 0;
    background-color: white;
    right: 10px;
    box-shadow: 0 7px 14px rgba(0,0,0,0.12), 0 7px 7px rgba(0,0,0,0.09);
    z-index: 100000000;
    max-height: 175px;
}
</style>