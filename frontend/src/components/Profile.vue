<template>
    <div class="ProfileConteiner" id="body">
        <div class="profile-row">
            <div class="leftColumn">
            <div class="ProfileLable Lblock" >
                <img :src="logo" alt="аватарка" class="ProfileImg" />
                <router-link to="/settings">
                    <div class="ProfileNastr" @click="nastrClick">
                        <label>Настройки</label>
                        <img src="/static/mainapp/images/settings-cogwheel-button.svg" alt="настройки"/>
                    </div>
                </router-link>
            </div>
            <div class="VK Lblock">
                <label>В контакте</label>
                <img src="/static/mainapp/images/vk.svg" alt="настройки"/>
            </div>
            <div class="LikeMusic Lblock">
                <label title="Понравившаяся музыка">Понравившаяся музыка({{ likes.length }})</label>
                <hr>
                <div class="likedMusic" :key="index" v-for="(like, index) in likes">
                    <!--<div class="likedMusicHover"></div>-->
                    <div class="musicLable" :style="backgroundImage(like.logo)"></div>
                    <div class="musicLablecontrol" style="background-image: url(/static/mainapp/play-arrow.svg)"></div>
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
                    <label>Мои издания</label>

                    <div class="MyAlbums-conteiner" :key="index" v-for="(album, index) in albums">
                        <div class="MyAlbum">
                            <img class="MyAlbum-lable" :src="album.logo" alt="настройки"/>
                            <div class="Albom-Description">
                                <span> {{ album.name }}</span>
                                <label> жанр: {{ album.genre }}</label>
                                <label> дата выхода: {{ album.date }}</label>
                                <span class="more"> подробнее... </span>
                            </div>
                            <div class="MyAlbum-music">
                               <div class="Mymusic-conteiner">
                                    <div class="MyMusic" :key="index" v-for="(track, index) in album.tracks">
                                        <!--<div class="likedMusicHover"></div>-->
                                        <div class="MyMusiccontrol" style="background-image: url(/static/mainapp/play-arrow.svg)"></div>
                                        {{ track.name }}
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
            likes: []
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
        name() {
            return this.$store.state.performerName;
        },
        logo() {
            return this.$store.state.performerLogo;
        },
        description() {
            return this.$store.state.performerDescription;
        }
    },
    methods: {
        receiveData() {
            var id = this.$route.params.id;
            this.$http.get('performers/' + id).then(function(response){
                console.log(response.body)
                for(var i = 0; i < response.body.albums.length; i++)
                {
                    var tracks = [];
                    for(var j = 0; j < response.body.albums[i].tracks.length; j++)
                    {
                        tracks.push({name: response.body.albums[i].tracks[j].name_trc, id: response.body.albums[i].tracks[j].id});
                    }
                    this.$set(this.albums, i, { name: response.body.albums[i].name_alb,
                                                logo: response.body.albums[i].image_alb,
                                                genre: response.body.albums[i].genre + ' / ' + response.body.albums[i].style,
                                                date: response.body.albums[i].date_alb,
                                                tracks: tracks});
                }
                //  if(response.body.image_per === null )
                //     {
                //         response.body.image_per = "/static/mainapp/images/cat.jpg"
                //     }
                this.$store.commit('performerID', response.body.id);
                this.$store.commit('performerName', response.body.name_per);
                this.$store.commit('performerLogo', response.body.image_per);
                this.$store.commit('performerDescription', response.body.about_per);
            });
            this.$http.get('likes').then(function(response){
                //console.log(response.body)
                for(var i = 0; i < response.body.length; i++)
                {
                    this.$set(this.likes, i, {name: response.body[i].name_trc, performer: response.body[i].name_per, logo:response.body[i].image_alb})
                }
            });
        },
        backgroundImage(url) {
            return 'background-image: url('+ url +')';
        },
        nastrClick() {
            this.$emit('nastr-clicked');
        }
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
    padding-top: 15px; 
    margin: 0 auto;
}
.ProfileConteiner
{
    padding-bottom: 69px; 
    background: linear-gradient(0deg, rgba(255, 255, 153, .2), rgba(0, 85, 255,0.2));
    font-size: 110%;
    top: 55px;
    position: relative;
    padding-left: 15px;
    padding-right: 15px;
    margin: 0 auto;
    max-width: 1280px;
    /*width: 60%;*/
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
.Albom-Description, .MyAlbum-lable, .MyAlbum-music
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
    height: 20%;
    float: left;
    width: 66%;
    margin-right: 1.7%;
    display: flex;
    flex-direction: column;
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
    width: 66%;
    display: block;
}
.Mymusic-conteiner
{
    max-height: 164.95px;
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
    background-color: rgba(230, 230, 230,0.5);
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
    background-color: rgba(153, 153, 153,0.3)
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
}
.likedMusic:hover
{
    background-color: rgb(235, 235, 235)
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




</style>
