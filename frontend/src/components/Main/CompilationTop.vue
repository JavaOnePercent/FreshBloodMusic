<template>
    <div id="compilation-top">
        <div class="recommendations">
            <div class="sortirovka-conteiner">
                <div class="sortirovka">
                    <label class="sortirovka-name">Рекомендации</label>
                    <div class="sort" v-if="showsortbutton">
                        <label>Отсортировать по:</label>
                        <span class="time" id="time" @click="showGenre(filter, genre, style, 'time')" @mousedown="checkSort">времени</span>
                        <span class="topic" id="topic" @click="showGenre(filter, genre, style, 'popularity')" @mousedown="checkSort">популярности</span>
                    </div>
                </div>
            </div>
         <div class="music-style-conteiner">
                <img id="next" class="next" @click="leftScrol" src="/static/mainapp/images/left.png"/>
                <div class="leftBevfore"></div>
                <div id="music-style" class="music-style">
                    <a  class="janr gen" name="" @click="showGenre('all')" :class="{'choseJanr':choseGenr==='all'}">Все</a>
                    <a  class="janr gen" :class="{'choseJanr':choseGenr==='recommended'}" name="" @click="showGenre('recommended')">Рекомендации</a>
                    <a  class="janr gen" :class="{'choseJanr':choseGenr==='favorite'}" name="" @click="showGenre('favorite')">Избранное</a>
                    <div class=" janr" :class="{'choseJanr':choseGenr===gen.id}" :key="index" v-for="(gen, index) in genres" >
                        <a style=" white-space: nowrap"  :name="gen.id" @click="showHer(index, gen.id)" >{{gen.name_gnr}}</a>
                    </div>
                </div>
                <img id="previous" class="previous" @click="rightScrol" src="/static/mainapp/images/right.png"/>
                <div class="rightBevfore"></div>
            </div>
          <transition name="style">
                <div v-if="showStyles" class="janrStyles-conteiner">
                <!-- <div  class="janrStyles-conteiner"> -->
                    <div class="janrStyles">
                        <a style=" white-space: nowrap" class="janr gen"  @click="showGenre('genre', genres[cock].id)">Все из {{genres[cock].name_gnr}}</a>
                        <div class=" janr" :key="index" v-for="(sty, index) in styles">
                            <a style=" white-space: nowrap" :name="sty.id" @click="showGenre('style', genre, sty.id)">{{sty.name_stl}}</a>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        <div class="compilation convert" ref="list">
            <div class="music" :key="index" v-for="(compilation, index) in compilations">
             <div class="cover-cont">
                <div class="play btn" @click="playClick(index)"><img src="/static/mainapp/images/playButton.svg" alt="play" title="воспроизвести"></div>
                <div class="turn btn" @click="toQueueClick(index)"><img src="/static/mainapp/images/playlist.svg" alt="tunr" title="в очередь"></div>
                <div class="album btn" @click="toQueueClick(index)"><img src="/static/mainapp/images/album.svg" alt="tunr" title="перейти ко всему альбому"></div>                    
                <img class="cover" :src="compilation.image_alb" alt="обложка">
                <img class="disk" :src="compilation.image_alb" alt="disk">
            </div>
            <div class="name-cont">
                <span :title="compilation.name_trc" class="group-name">{{ compilation.name_trc}}</span>
                <span class="music-name" @click="toPerformerPage(compilation.id_per)">{{ compilation.name_per}}</span>
            </div>
        </div>
    </div>
    </div>
</template>

<script>
export default {
    name: 'main-compilation',
    data: function() {
        return{
            compilation:[],
            compilations:[],
            genres:[],
            styles:[],
            url: 'api/tracks',
            loading: false,
            sort: 'popularity',
            genre: '',
            style: '',
            filter: 'all',
            showsortbutton: true,
            showStyles: false,
            choseGenr: '',
            cock: 0
          //hoverClass: 'disk'
        }
    },
    mounted(){
        document.body.addEventListener("scroll", this.onScroll, false);
    },
    beforeDestroy () { 
        document.body.removeEventListener("scroll", this.onScroll, false);
    },
    methods: {
        showHer(index, id) {
            this.cock = index
            this.showGenre('genre', id)
        },
        leftScrol()
        {
            document.getElementById('music-style').scrollLeft -= 300;
        },
        rightScrol()
        {
            document.getElementById('music-style').scrollLeft += 300;
        },
      
        toPerformerPage(id) {
            this.$router.push({ name: 'performer', params: { id: id }})
        },
        checkSort(e)
        {
            e.preventDefault();
            document.getElementById('time').style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1";
            document.getElementById('topic').style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1";
            e.target.style="background-color: rgba(192,192,192,0.8);border-bottom: 2px solid currentColor;line-height: 0.85;color: rgb(0,0,0)";
        },
        onScroll: function(event) {
            var wrapper = event.target;
            var list = document.getElementById('main');
            var scrollTop = wrapper.scrollTop;
            var wrapperHeight = wrapper.offsetHeight;
            var listHeight = list.offsetHeight;

            var diffHeight = listHeight - wrapperHeight;

            //console.log(diffHeight, scrollTop);
            if(diffHeight <= scrollTop && !this.loading) {
                if(this.url != null)
                    this.showGenre();
            }

        },
        showGenre(filter, genre = null, style = null, sort = null) {
          this.loading = true;
          var obj = {};
          this.filter = filter
          //if(genre != null || style != null)
          //{
            this.url = 'api/tracks';
            this.compilations = [];
            this.choseGenr= filter;
            if(genre !== null) {
                this.genre = genre;
                this.choseGenr=genre;
                if (!(isNaN(this.genre))) {
                    this.getGengeAndStyles(this.genre);
                }
                else {
                    this.getGengeAndStyles()
                }
                this.style = null;
            }
            else
            {
                this.showStyles = false;
            }
            if(style !== null) {
                this.style = style;
            }
            
            if(sort !== null) {
                this.sort = sort;
            }
            if(filter === 'recommended' || filter === 'favorite') {
                this.showsortbutton = false;
            }
            else {
                this.showsortbutton = true;
            }
            obj = {params: {
                filter: this.filter,
                genre: this.genre, 
                style: this.style, 
                sort: this.sort
            }}
          //}
          this.$http.get(this.url, obj).then(function(response){
                this.compilation = response.body.results;
                for(var i = 0; i < this.compilation.length; i++)
                {
                    if(this.compilation[i].image_alb === null)
                    {
                     this.compilation[i].image_alb = "/static/mainapp/images/cat.jpg"
                    }
                }
                this.compilations = this.compilations.concat(this.compilation);
                // console.log(this.compilations);
                if(response.body.next != null)
                {
                    var url = document.createElement('a');
                    url.href = response.body.next;
                    this.url = url.pathname + url.search;
                }
                else 
                {
                    this.url = null;
                }
                //console.log(this.url);
                this.loading = false;
            }, function(error){
                this.loading = false;
            })
        },
        toQueueClick: function(index) {
            //this.$emit('trackclicked');
            this.$bus.$emit('track-to-queue', {
				id: this.compilations[index].id
			});
        },
        playClick: function(index) {
            //this.$emit('trackclicked');
            this.$bus.$emit('play-track', {
				id: this.compilations[index].id
			});
        },
        //для Илюши
        getGengeAndStyles: function (message = null) {
            this.$http.get('api/genre', {params: {id: message}}).then(function(response){
                // console.log(response.data)
                if(message == null) {
                    this.genres = response.data;
                    this.styles = null;
                }
                else
                    this.styles = response.data;
                    if(this.styles!=null && this.styles.length!=0 )
                    {
                        this.showStyles=true;
                    }
                    else
                    {
                        this.showStyles=false;
                    }
            }, function(error){
            })
        }
    },
    created: function() {
        this.showGenre('all'),
        this.getGengeAndStyles()
    }
}
</script>

<style scoped>
.recommendations
{
    height: auto;
    width: 100%;
    margin: 0 auto;
    position: relative;
    display: flex;
    flex-direction: column;
}
.recommendations .music-style, .recommendations .janrStyles
{
    flex-basis: 100px;
    display: flex;
    height: 40px;
    font-size: 20px;
    justify-content: flex-start;
    line-height:40px;
}
/*сортировка*/
.sortirovka-conteiner
{
    top: 0px;
    left: 0px;
    height: 40px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    justify-content: center;
}
.sortirovka
{

    position: relative;
    height: 40px;
    padding-left: 15px;
    padding-right: 15px;
    box-sizing: border-box;
    margin: 0 auto;
    max-width: 1143px; 
    min-width: 915px; 
}
.sortirovka-name
{
    line-height: 40px;
    float: left;
    width: 30%;
    font-size: 30px;
}
.sort
{
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    /* color: rgba(0,0,0,0.55); */
    font-size: 20px;
    line-height: 40px;
    width: 70%;
    float: left;
}
.sort label
{
    margin-right: 5px;
}
.sort span
{
    margin-right:5px; 
    padding: 4px;
}
.sort span:hover, .sort span:active
{
    cursor: pointer;
    background-color: rgba(192,192,192,0.8);
    border-bottom: 2px solid currentColor;
    line-height: 0.85
}
.time:before
{
    font-family: "FontAwesome";
    content: "\f017"; 
    content: '🕒';
    margin-right:5px; 
}
.topic:before
{
    font-family: "FontAwesome";
    content: "\f06d";
    content: '⚡';
    margin-right:5px; 
}
.topic
{
    background-color: rgba(192,192,192,0.8);
    border-bottom: 2px solid currentColor;
    line-height: 0.85;color: rgb(0,0,0)
}
/*рекомендации*/
.music-style-conteiner
{
    background-color: rgb(255, 181, 43);
    /* background-color: rgb(85, 85, 85); */
    top: 0px;
    left: 0px;
    height: 40px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    display: block;
    justify-content: center; 
}
.music-style
{ 
    scroll-behavior: smooth;
    display: block;
    /* background-color: rgb(85, 85, 85); */
    position: relative;
    height: 40px;
    /* padding-left: 15px;
    padding-right: 15px; */
    box-sizing: border-box;
    margin: 0 auto;
    max-width: 1143px; 
    min-width: 775px;
    color: white;
    overflow-x: scroll;
    white-space: nowrap;
    -ms-overflow-style: none;
}
.music-style::-webkit-scrollbar { display: none; }

.janrStyles-conteiner
{
    /* box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    -webkit-box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    -moz-box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset; */
    background-color: rgb(211, 147, 29);
    /* background-color: rgb(55, 55, 55); */
    top: 0px;
    left: 0px;
    height: 40px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    justify-content: center;
}

.janrStyles
{
    justify-content:unset;
    position: relative;
    height: 40px;
    /* padding-left: 15px;
    padding-right: 15px; */
    box-sizing: border-box;
    margin: 0 auto;
    max-width: 1143px; 
    min-width: 915px; 
    color: white;
}
.janrStyles .janr:hover
{
    background-color: rgb(151, 106, 23);
}
.janr
{
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    /* padding: 0 15px; */
}
.janr a
{
    padding: 0 15px;
    position: relative;
    width: 110%;
    height: 100%;
    display: block;
}
.janr:hover
{
    height: 100%;
    cursor: pointer;
    background-color: rgb(250, 174, 32);
    /* background-color: rgba(192,192,192,0.8); */
    border-bottom: 5px solid rgb(126, 50, 44);
    box-sizing: border-box; 
    line-height: 1.8;
    box-shadow: 0 3px 6px rgba(0,0,0,0.25)
    /* box-shadow: 0 6px 12px rgba(0,0,0,0.25), 0 5px 5px rgba(0,0,0,0.22); */
}
.choseJanr
{
    border-bottom: 5px solid rgb(126, 50, 44);
    box-sizing: border-box; 
    line-height: 1.8;
}
.gen
{
    padding: 0 15px;
}
.janr:focus
{
    background-color: rgba(192,192,192,0.8);
}
/*подборка*/

.compilation
{
    padding-left: 15px;
    padding-right: 15px; 
    min-width: 915px; 
    max-width: 1113px;
    margin: 0 auto;
    position: relative;
    padding-top: 25px;
    display: flex;
    flex-wrap: wrap;
}

.compilation .music
{
    position: relative;
    padding-bottom:68px;
    flex-basis: 22%;
    /* overflow: hidden; */
    text-align: center;
}
.compilation .music:nth-child(4n+2)
{
    margin-right: 4%;
    margin-left: 4%;
}
.compilation .music:nth-child(4n+3)
{
    margin-right: 4%;
}
/* .compilation .music::before
{
    content:url(/static/mainapp/images/playButton.svg);
    position: absolute;
    top: 0;left: 0; right: 0; bottom: 0;
    margin: auto;
    width: 25%;
    height: 20%;
    z-index: 70;
} */
.cover-cont
{
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    display: block;
    min-height: 195px;
    max-height: 300px; 
    width: 100%;
    height: auto;
    position: relative;
    /* overflow:visible; */
}
/* .cover-cont::before
{
    content:url(/static/mainapp/images/playButton.svg);
    position: absolute;
    top: 0;left: 0; right: 0; bottom: 0;
    margin: auto;
    width: 25%;
    height: 20%;
  
}
.cover-cont::after
{
    content:url(/static/mainapp/images/playButton.svg);
    position: absolute;
    top: 0;left: 0; right: 0; bottom: 0;
    margin: auto;
    width: 25%;
    height: 20%;
    z-index: 70;
} */
.cover
{
    image-rendering:  auto;
    border: none;
    object-fit: cover;
    image-rendering: optimizeQuality;
    image-rendering: -webkit-crisp-edges;
    /* backface-visibility: hidden; */
    transition: 1.4s transform;
    position:relative;
    z-index: 50;
    top: 0; right: 0; bottom: 0; left: 0;
    height: auto;
    width: 100%; 
    padding: 0;
}
.disk
{
    border-radius: 50%;
    transition: 1s transform;
    /* backface-visibility: hidden; */
    position:absolute;
    z-index: 40;
    top: 0; right: 0; bottom: 0; left: 0;
    margin: auto;
    height: auto;
    width: 95%; 
    padding: 0;
}
.cover-cont:hover  .disk
{
    z-index: 40;
    transition-duration: .7s;
    transform: translateX(-13.5%) rotate(45deg);
    -o-transform: translateX(-13.5%) rotate(45deg);
    -ms-transform: translateX(-13.5%) rotate(45deg);
    -moz-transform: translateX(-13.5%) rotate(45deg);
    -webkit-transform: translateX(-13.5%) rotate(45deg);
    display: block;
}
.cover-cont:hover~.name-cont
{
    transition-duration: .7s;
    transform: /*scale(1.05)*/ translateX(8.3%) /*translateY(5px)*/;
}
.name-cont
{
    height: 48px;
    width: 100%;
    transition: 1.4s transform;
    position: absolute;
    overflow: hidden;
}
.group-name
{
    cursor: default;
    width:100%; 
    position: relative;
    backface-visibility: hidden;
    display: block;
    overflow-x:hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size:23px; 
}
.hover-music-name
{
    visibility: hidden;
}
.music-name
{
    cursor: pointer;
    position: relative;
    backface-visibility: hidden;
    overflow-x:hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: grey;
    display: block;
    font-size:18px; 
}
.cover-cont:hover .cover
{
    z-index: 60;
    filter:grayscale(.75);
    height: auto;
    -o-transform: translateX(8.3%);
    -ms-transform: translateX(8.3%);
    -moz-transform: translateX(8.3%);
    -webkit-transform: translateX(8.3%);
    transform: /*scale(1.05)*/ translateX(8.3%);
    transition-duration: .7s;
    /*-webkit-filter: invert(100%)*/
    /*box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);*/ 
}
.cover-cont:hover .btn
{
    -o-transform: translateX(25%);
    -ms-transform: translateX(25%);
    -moz-transform: translateX(25%);
    -webkit-transform: translateX(25%);
    transform: translateX(25%);
    display: block;
    transition: 1.4s transform;
    transition-duration: .7s;
}
.btn
{
    opacity: 0.8;
    transition: 1.4s transform;
    display: none;
    cursor: pointer; 
    background-color: rgba(255, 255, 255,0.7);
    padding: 5%;
    border-radius: 50px;
    width: 19%;
    height: 19%;
    z-index: 70;
    position: absolute;
    top: 0;left: 0;right: 0;bottom: 0;
    margin: auto
}
.btn:hover
{
    opacity: 1;
}
.btn:active
{
    box-shadow: 200px 0 0 0 rgba(0,0,0,.3) inset;
}
.btn img
{
    position: absolute;
    top: 0;left: 0;right: 0;bottom: 0;
    margin: auto;
    width: 60%;
    height: 60%;
} 
.play
{
    bottom: 17%;
    right: 35%;
}
.turn
{
    bottom: 17%;
    left:35%;
}
.turn img
{
    top: 15%;
}
.style-enter-active, .style-leave-active {
    transition: all 0.3s;
}
.style-enter, .style-leave-active {
    height: 0px;
}
.album
{
    top: 39.5%;
}
.next
{
    z-index: 50;
    top: 0;
    box-sizing: border-box;
    padding: 7px;
    cursor: pointer;
    position:absolute;
    width: 40px;
    height: 40px;
    background-color: rgb(255, 181, 43);
}
.leftBevfore
{
    z-index: 80;
    left: 30px;
    box-sizing: border-box;
    position:absolute;
    width: 40px;
    height: 40px;
    background: linear-gradient(to left, rgba(66, 160, 189, 0), rgba(255, 181, 43,1));
}
.previous
{
    clear: both;
    text-align: right;
    margin: 0 auto;
    top: 0;
    right: 0;
    box-sizing: border-box;
    padding: 7px;
    cursor: pointer;
    position:absolute;
    width: 40px;
    height: 40px;
    background-color: rgb(255, 181, 43); 
}
.rightBevfore
{
    top: 0;
    right: 30px;
    box-sizing: border-box;
    display: block;
    position:absolute;
    width: 40px;
    height: 40px;
    background: linear-gradient(to right, rgba(66, 160, 189, 0), rgb(255, 181, 43));
}
/* .style-enter {
  transform: translatey(40px);
}
.style-leave-active {
  transform: translatey(40px);
} */
</style>