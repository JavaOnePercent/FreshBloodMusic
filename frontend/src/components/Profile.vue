<template>
    <div class="ProfileConteiner" id="body">
        <div class="profile">
            <div v-if="error" class="error-cont profile-row">
                <div class="error">
                    <img class="errorImg" src="/static/mainapp/images/Yoda.png" alt="">
                    <label> Это не тот пользователь которого вы ищите</label>
                </div>
            </div>
            <div v-if="!error">
                <div class="profile-row">
                    <div class="leftColumn">
                    <div class="ProfileLable Lblock" >
                        <img :src="logo" alt="аватарка" class="ProfileImg" />
                        <router-link to="/settings" v-if="myPerformerID === performerID">
                            <div class="ProfileNastr" @click="nastrClick">
                                <label>Настройки</label>
                                <img src="/static/mainapp/images/settings-cogwheel-button.svg" alt="настройки"/>
                            </div>
                        </router-link>
                    </div>
                    <!-- <div class="VK Lblock">
                        <label>В контакте</label>
                        <img src="/static/mainapp/images/vk.svg" alt="настройки"/>
                    </div> -->
                    <div class="LikeMusic Lblock">
                        <label title="Понравившаяся музыка">Понравившаяся музыка({{ likes.length }})</label>
                        <hr>
                        <div @click="playClick(like.id)" class="likedMusic" :key="index" v-for="(like, index) in likes">
                            <!--<div class="likedMusicHover"></div>-->
                            <div class="musicLable" :style="backgroundImage(like.logo)"></div>
                            <div class="musicLablecontrol" style="background-image: url(/static/mainapp/images/play-arrow.svg)"></div>
                            {{ like.performer }} - {{ like.name }}
                        </div>
                    </div>
                    <!--<div class="subscribers Lblock">
                        <label>Подписки (+число)</label>
                        <hr>
                        <div class="sub-cont">
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        <div class="sub"> чел </div>
                        </div>
                    </div>-->
                    </div>       
                    <div class="rightColumn">
                        <div class="ProfileName Rblock">
                            <label>{{ name }}</label>
                        </div>
                        <div class="ProfileDescription Rblock">
                            <label>Описание</label>
                            <p>{{ description }}</p>
                        </div>
                        <!--<div class="favoriteAlbum Rblock">
                            <label>Любимый Альбом</label>
                            <p>Тут любимый альбом</p>
                        </div>-->
                        <div class="MyAlbums Rblock">
                            <label>Издания</label>

                            <div class="MyAlbums-conteiner" :key="i" v-for="(album, i) in albums">
                                <div class="MyAlbum">
                                    <img class="MyAlbum-lable" :src="album.image_alb" alt="настройки"/>
                                    <div class="Albom-Description">
                                        <span style="width:90%; overflow-x: hidden"> {{ album.name_alb }}</span>
                                        <img title="Удалить альбом" @click="deleteAlbum(i)" class="albumDel" src="/static/mainapp/images/closeDropdown.svg"/>
                                        <div @click="playAlbum(album.tracks)" class="playAll"> 
                                            <img src="/static/mainapp/images/play-arrow.svg"/>
                                            <span> Проигрывать весь альбом </span>
                                        </div>
                                        <label> жанр: {{ album.genre + " / " + album.style }}</label>
                                        <label> дата выхода: {{ album.date_alb }}</label>
                                        <span class="more"> подробнее... </span>
                                    </div>
                                    <div class="MyAlbum-music">
                                        <div class="Mymusic-conteiner">
                                            <div @click="playClick(track.id)" class="MyMusic" :key="j" v-for="(track, j) in album.tracks">
                                                <!--<div class="likedMusicHover"></div>-->
                                                <div class="MyMusiccontrol" style="background-image: url(/static/mainapp/images/play-arrow.svg)"></div>
                                                <div :title="track.name_trc" class="trackName">
                                                    {{ track.name_trc }}
                                                </div>
                                                <div class="control" >
                                                <img style="float:right" title="Удалить композицию" @click="deleteTrack(i, j)" class="MyMusiccontrol MyMusicDel" src="/static/mainapp/images/xiomi.png"/>
                                                <span style="float:right;position:absolute;left:27px; font-size:80%;">{{ track.likes }}</span>
                                                <img  class="liked" src="/static/mainapp/images/likeOren.svg"/>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>    
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>  
</template>

<script>
export default {
  name: 'profile',
  data() {
        return {
            albums: [],
            likes: [],
            error:false,
            name: '',
            logo: null,
            description: '',
        }
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
        playAlbum(tracks) {
            for(var i = 1; i < tracks.length; i++)
            {
                this.$bus.$emit('track-to-queue', tracks[i])
            }
            this.$bus.$emit('play-track', tracks[0])
            
        },
        deleteTrack(i, j) {
            this.$http.delete('../api/tracks/' + this.albums[i].tracks[j].id, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(
                response => {
                    this.albums[i].tracks.splice(j, 1)
                }
            )
        },
        deleteAlbum(i) {
            this.$http.delete('../api/albums/' + this.albums[i].id, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(
                response => {
                    this.albums.splice(i, 1)
                }
            )
        },
        receiveData() {
            var id = this.$route.params.id;
            this.$http.get('../api/performers/' + id).then(function(response){
                //console.log(response.body)
                /*for(var i = 0; i < response.body.albums.length; i++)
                {
                    var tracks = [];
                    for(var j = 0; j < response.body.albums[i].tracks.length; j++)
                    {
                        tracks.push(response.body.albums[i].tracks[j]);
                    }
                    this.$set(this.albums, i, { name: response.body.albums[i].name_alb,
                                                logo: response.body.albums[i].image_alb,
                                                genre: response.body.albums[i].genre + ' / ' + response.body.albums[i].style,
                                                date: response.body.albums[i].date_alb,
                                                tracks: tracks});
                }*/
                //  if(response.body.image_per === null )
                //     {
                //         response.body.image_per = "/static/mainapp/images/cat.jpg"
                //     }
                this.albums = response.body.albums
                this.$store.commit('performerID', response.body.id);
                /*this.$store.commit('performerName', response.body.name_per);
                this.$store.commit('performerLogo', response.body.image_per);
                this.$store.commit('performerDescription', response.body.about_per);*/
                this.name = response.body.name_per
                this.logo = response.body.image_per + '?' + Math.random()
                this.description = response.body.about_per
                this.error=false;
            }, function(error){
                this.error=true;
            });
            this.$http.get('../api/likes', {params: {performer: id}}).then(function(response){
                this.likes = []
                for(var i = 0; i < response.body.length; i++)
                {
                    this.likes.push({name: response.body[i].name_trc, performer: response.body[i].name_per, logo:response.body[i].image_alb, id:response.body[i].trc_id})
                }
            });
        },
        backgroundImage(url) {
            return 'background-image: url('+ url +')';
        },
        nastrClick() {
            this.logo = ''
        },
        toQueueClick: function(index) {
            //this.$emit('trackclicked');
            this.$bus.$emit('track-to-queue', {
				id: index
			});
        },
        playClick: function(index) {
            //this.$emit('trackclicked');
            this.$bus.$emit('play-track', {
				id: index
			});
        },
    },
}
</script>

<style scoped>

html, body
{
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    font-family: Arial,Helvetica,sans-serif;
    background-color: rgb(222, 222, 115);
}
.profile-row:after
{
    content: "";
    display: table;
    clear: both;
}
.profile-row
{
    padding-bottom:69px; 
    padding-top: 70px; 
    margin: 0 auto;
}
.ProfileConteiner
{
    background-color: rgba(70, 57, 78, 0.281);
    /* background: linear-gradient(0deg, rgba(255, 255, 153, .2), rgba(36, 87, 189, 0.2)); */
    font-size: 110%;
    /* padding-top: 55px; */
    position: absolute;
    width: 100%;
    min-height: 100%;
    /*width: 60%;*/
}
.profile
{ 
    padding-left: 15px;
    padding-right: 15px;
    margin: 0 auto;
    max-width: 1143px; 
    min-width: 915px; 
}
.Rblock
{
    padding: 1%;
    background-color: #fff;
    display: block;
    box-sizing: border-box;
    margin-bottom: 2%;
    box-shadow: 0 5px 12px rgba(0,0,0,0.15), 0 3px 3px rgba(0,0,0,0.12);
}
/*то что справа*/
.rightColumn
{
    float: left;
    width: 73.5%;
}
.ProfileName
{
    font-size: 190%;
}
.ProfileDescription
{
    font-size: 130%;
}
.ProfileDescription p
{
    margin-bottom: 8px;
    margin-top: 15px;
    padding: 0;
    font-size: 80%;
}
.favoriteAlbum
{
    font-size: 130%;
}
.MyAlbums
{
    font-size: 110%;
}
.MyAlbums-conteiner
{
    display: flex;
    flex-direction: column;
    width: 100%;
    flex-basis: 100%;
}
.MyAlbums-conteiner:not(:nth-child(2)) .MyAlbum
{
    margin-top: 1.5%; 
}
.MyAlbum
{
    min-height: 176.78px;
    height: auto;
    /*display: flex;*/
    flex-basis: 25%;
    padding: 1%;
    background-color: rgba(217, 217, 217,0.3);
}
.Albom-Description, .MyAlbum-lable
{
    float: left;
}
.MyAlbum-lable
{
    margin: auto;
    height: 30%;
    width: 30%;
    margin-right: 2%;
}
.Albom-Description
{
    cursor: default;
    position: relative;
    height: 20%;
    float: left;
    width: 66%;
    margin-right: 1.7%;
    display: flex;
    flex-direction: column;
}
span
{
    cursor: default;
}
.more
{
    cursor: pointer;
    color: cornflowerblue;
    font-size: 70%;
}
.Albom-Description label
{
    font-size: 70%;
}
.MyAlbum-music
{
    float: left;
    width: 66%;
}
.Mymusic-conteiner
{
    max-height: 163px;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 8px;
    width: 95%;
    height: 83%;
    margin: 1.5% 1.5%;
    background-color: rgba(255, 255, 255,0.5);
    box-shadow: 0 0 23px rgba(0, 0, 0, .1) inset; 
}
.MyMusic
{
    margin: auto;
    position: relative;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    padding: 3px;
    line-height: 43px;
    height: 43px;
    cursor: pointer;
}
.MyMusic:hover
{
    background-color: rgba(252, 177, 39, 0.2);
}
.MyMusiccontrol
{
    margin: 5px 5px 5px 0px; 
    width: 35px;
    height: 35px;
    float: left;
}

/*то что слева*/

.leftColumn
{

    float: left;
    margin-right: 1.5%; 
    width: 25%;
}
.Lblock
{

    padding: 2%;
    margin-bottom: 5%;
    display: block;
    background-color: #fff;
    box-sizing: border-box;
    box-shadow: 0 5px 12px rgba(0,0,0,0.15), 0 3px 3px rgba(0,0,0,0.12);
}
.ProfileImg
{
    /*margin: 0 auto;*/
    display: block;
    width: 100%;
    height: auto;
    margin-bottom: 2.5%;
}
.ProfileNastr
{
    color: black;
    font-size: 110%;
    line-height: 43px;
    text-align: center;
    padding: 1.7%;
    /*padding-left: 5%; */
    height: 43px;
    position: relative;
    display: block;
}
a
{
    text-decoration: none;
}
.ProfileNastr:hover
{
    cursor: pointer;
    /* background: linear-gradient(0deg, rgba(228, 170, 11, 0.4), rgba(84, 84, 85, 0.1));; */
    background-color: rgba(252, 177, 39, 0.2)
    /* background-color: rgba(153, 153, 153,0.3) */
}
.ProfileNastr img
{
    padding-top: 5px; 
    width: 33px;
    height: auto;
    float: right;
}
.ProfileNastr label
{
    margin-left: 33px;
    cursor: pointer;
}
.VK
{
    font-size: 110%;
    cursor: pointer;
    text-align: center;
    background-color: rgb(69, 102, 142);
    color: #fff;
    font-weight: 500;
    line-height: 33px;
    height: 43px;
}
.VK img
{
    width: 33px;
    float: right;
}
.VK label
{
    cursor: pointer;
    margin-left: 33px;
}
.LikeMusic
{
    white-space: nowrap;
    text-overflow: ellipsis;
    cursor: pointer;
    min-height: 37.38px;
    max-height: 316.38px;
    overflow: hidden;
    overflow-y: scroll;
}
.likedMusic:hover
{
    background-color: rgba(252, 177, 39, 0.2);
    /* background-color: rgb(235, 235, 235) */
}
.likedMusic:hover  .musicLable
{
    opacity: 0.1;
}
.likedMusic:hover .musicLablecontrol
{
    display: block;
}
.musicLable
{
    image-rendering: -webkit-optimize-contrast;
    image-rendering: optimize-contrast;
    background-size: cover;
    float: left;
    display: block;
    margin-right: 4px; 
    margin-top: 3px; 
    width: 45px;
    height: 45px;
}
.musicLablecontrol
{
    background-image: url(/playButton.svg);
    margin-left: 4.5px; 
    margin-top: 10px;
    z-index: 110;
    display: block;
    width: 20px;
    height: 20px;
    padding: 7.5px;
    background-size: cover;
    position: absolute;
    background-repeat: no-repeat;
    background-position: center center;
    display: none;
}
.LikeMusic label
{
    cursor: pointer;
    /*line-height: 25px;*/
    width: 100%;
}
.LikeMusic hr
{
    margin: 2px;
}
.likedMusic
{
    box-sizing: border-box;
    overflow-x:hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    line-height: 50.59px;
    padding: 1.8px;
    /* background-color: rgb(204, 204, 204); */
    margin-top: 5px;
}
.subscribers
{
    min-height: 37.38px;
    max-height: 225.88px;
}
.subscribers hr
{
    margin: 2px;
    margin-bottom: 5px;
}
.sub-cont
{
    overflow: hidden;
    display: flex;
    flex-wrap: wrap;
    flex-basis: 22.75%;
    justify-content: end;
    max-height: 181.124px;
}
.sub
{
    width: 22.75%;
    height: auto;
    background-color: rgb(204, 204, 204);
    margin-bottom: 25px;
}
.sub::before {
	content: "";
	display: block;
	padding-top: 67.1%; /* С помощью этого padding мы задаем высоту равную ширине блока */
}
.sub:nth-child(4n+2)
{
    margin-right: 3%;
    margin-left: 3%;
}
.sub:nth-child(4n+3)
{
    margin-right: 3%;
}

.error-cnt
{
    min-height: 100%;
    position: relative;
    width: 100%;

}
.error
{
    line-height: 250px;
    max-width: 1143px; 
    min-width: 915px; 
    position: relative;
    top:0;left: 0;right: 0; bottom: 0;
    margin: 10% auto;
}
.errorImg
{
    width: 20%;
    float: left;
}
.error label
{
    width: 80%;
    font-size: 200%;
    font-weight: 600; 
    float: left;
}
.albumDel
{
    position: absolute;
    cursor: pointer;
    width: 25px;
    height: 25px;
    top:1%;
    left: 97%;
}
.albumDel:hover
{
    transform: scale(1)
}
.playAll
{
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    margin-top:5px;
    margin-bottom: 5px; 
    padding: 5px;
    height: 30px;
    cursor: pointer;
    line-height: 30px;
    font-size: 75%;
    font-weight: 600;
    border: solid;
    background-color: rgb(255, 181, 43);
    border-color: rgba(255, 255, 255, 0);
    /* transform: skew(-10deg); */
    width: 233.656px;
    display: flex;
}
.playAll img
{
    /* transform: skew(10deg); */
    width: 30px;
    height: 30px;
    padding-right:5px; 
}
.playAll span
{
    cursor: pointer;
    /* transform: skew(10deg); */
}
.playAll:active
{
    background-color: rgb(226, 160, 38);
}
.MyMusicDel
{   
    position: absolute;
    margin-left: 15px; 
    opacity: 60;
    width: 30px;
    height: 30px;
    left: 54%; 
}
.liked
{   
    position: absolute;
    opacity: 60%;
    width: 25px;
    height: 25px;
    margin-top: 9px;
}
.control
{
    float: right;
    height: 49px;
    width: 20%;
    position: relative;
}
.trackName
{
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    float: left;
    margin: 0px;
    width: 70%;
}
/* .MyMusic:hover .control
{
    display: block;
} */
</style>
