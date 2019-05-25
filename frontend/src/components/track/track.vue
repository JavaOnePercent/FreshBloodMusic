<template>
    <div>
        <div :class="{currentTrc:current_trc===index}" class="track" :key="index" v-for="(track, index) in tracks">
            <div v-if="track.image" class="trc-logo"> 
                <img :src="'/media/' + track.image" alt="">
            </div>
            <img v-else class="play" src="/static/mainapp/images/orange-arrow.svg" alt="">
            <span class="track-name" >{{track.performer}} — {{track.name}}</span>
            <span class="time"> {{getCorrectTime(track.duration)}} </span>
            <div class="trc-controll">
                <span class="trc-controll-btn like" @click.stop="likeTrack(track, index)">
                    <img v-if="!track.is_liked" src="/static/mainapp/images/empty-heart.svg" title="мне нравится">
                    <img v-else src="/static/mainapp/images/heart.svg" title="мне нравится">
                </span>
                <span class="trc-controll-btn like" @click.stop="gotoSimilar(track.id, track.name)">
                    <img src="/static/mainapp/images/similar.svg" title="показать похожие" >
                </span>
                <span class="trc-controll-btn add-to-playlist" @click.stop="current_trc=current_trc===index?null:index">
                    <img src="/static/mainapp/images/plus.svg" title="добавить в плейлист" >
                </span>
            </div>
            <user-playlists @close="current_trc=null" :trc_id='track.id' v-click-outside="changeUser_playlists" v-if="current_trc===index"> </user-playlists>
        </div>
    </div>
</template>

<script>
import userPlaylists from '../userPlaylists/userPlaylists'
export default {
    name: 'trackComp',
    props: ['tracks'],
    data() {
        return {
            current_trc: null
        }
    },
    components: {
        userPlaylists,
    },
    methods: {
        likeTrack(track, index) {
            if(!track.is_liked)
                this.like(track, index)
            else
                this.dislike(track, index)
        },
        like(track, index) {
            this.$http.put('../api/likes', {}, {
                params: {track_id: track.id},
            }).then(function(response){
                this.tracks[index].is_liked = true
                this.$bus.$emit('likeNot', 'вам понравилась песня ' +  this.tracks[index].name)
            }); 
        },
        dislike(track, index) {
            this.$http.delete('../api/likes', {
                params: {track_id: track.id},
            }).then(function(response){
                this.tracks[index].is_liked = false
                this.$bus.$emit('likeNot', 'вам больше не нравится ' + this.tracks[index].name) 
            }); 
        },
        changeUser_playlists() {
            this.current_trc = null;
        },
        getCorrectTime(sec) {
            var m = Math.floor(sec / 60)
            var s = sec % 60
            if(s < 10) {s= '0' + s}
            return m + ':' + s
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

<style scoped>
.track
{
    width: calc(100% - 15px);
    height: 45px;
    position: relative;
    display: flex;
    justify-content: flex-start;
    margin-bottom: 6px;
    padding-right: 15px;
}
.play
{
    width: 35px;
    height: 100%;
    padding-left:15px;
    padding-right: 15px;  
    position: relative;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
}
.trc-logo img
{
    width: 45px;
    height: 45px;
    padding-left:15px;
    padding-right: 15px;  
    position: relative;
    display: block;
}
.track-name
{
    line-height: 45px;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    white-space: nowrap;
    padding-right: 50px;
}
.track:hover
{
    cursor: pointer;
    background-color: rgba(189, 176, 208, 0.3)
}
.track:hover .trc-logo img, .currentTrc .trc-logo img
{
    opacity: 0.4;
    filter: grayscale(100%);
}
.trc-logo::before
{
    width: 35px;
    height: 35px;
    top: 5px;
    left: 23px;
    bottom: 0;
    right: 0;
    position: absolute;
    content: ' ';
    background-image: url(/static/mainapp/images/orange-arrow.svg);
    background-size: cover;
    background-position: 50% 50%;
    z-index: 50;
    display: none;
}
.track:hover .trc-logo::before, .currentTrc .trc-logo::before
{
    display: block;
}
.time
{
    font-size: 13px;
    width: 40px;
    line-height: 45px;
    float: right;
    color: rgb(45, 45, 45);
    text-align: right;

}
.trc-controll
{
    position: relative;
    float: right;
    display: none;
}
.track:hover .trc-controll
{
    display: flex;
}
.trc-controll-btn
{
    width: 40px;
    position: relative;
}
.trc-controll-btn img
{
    width: 20px;
    position: absolute;
    margin: auto;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    opacity: 0.6;
}
.like:hover img, .add-to-playlist:hover img, .trash:hover img
{
    opacity: 1;
}
.currentTrc
{
  background-color: rgba(189, 176, 208, 0.3)
}
.currentTrc .trc-controll
{
    display: flex;
}
</style>