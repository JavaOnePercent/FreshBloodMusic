<template>
    <div id="compilation-top">
        <div class="recommendations">
            <div class="sortirovka-conteiner">
                <div class="sortirovka">
                    <label class="sortirovka-name">Рекомендации</label>
                    <div class="sort" v-if="showsortbutton">
                        <label>Отсортировать по:</label>
                        <span class="time" id="time" @click="showGenre(genre, style, 'time')" @mousedown="checkSort">времени</span>
                        <span class="topic" id="topic" @click="showGenre(genre, style, 'popular')" @mousedown="checkSort">популярности</span>
                    </div>
                </div>
            </div>
            <div class="music-style-conteiner">
                <div class="music-style">
                    <a class="janr" name="" @click="showGenre('all', null, sort)">Все</a>
                    <a class="janr" name="" @click="showGenre('rec', null, sort)">Рекомендации</a>
                    <a class="janr" name="" @click="showGenre('fav', null, sort)">Избранное</a>
                    <div class="gen janr" :key="index" v-for="(gen, index) in genres">
                        <a  :name="gen.id" @click="showGenre(gen.id, null, sort)">{{gen.name_gnr}}</a>
                    </div>
                </div>
            </div>
            <div class="janrStyles-conteiner">
                <div class="janrStyles gen">
                    <div class="janr" :key="index" v-for="(sty, index) in styles">
                        <a  :name="sty.id" @click="showGenre(null, sty.id, sort)">{{sty.name_stl}}</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="compilation convert" ref="list">
            <div class="music" :key="index" v-for="(compilation, index) in compilations">
             <div class="cover-cont">
                <div class="play btn"><img src="/static/mainapp/images/Wplay.svg" alt="play" title="воспроизвести"></div>
                <div class="turn btn"><img src="/static/mainapp/images/Wplaylist.svg" alt="tunr" title="в очередь"></div>                   
                <img class="cover" :src="compilation.image_alb" alt="обложка" @click="trackClick(index)">
                <img class="disk" :src="compilation.image_alb" alt="disk">
            </div>
            <div class="name-cont">
                <span :title="compilation.name_trc" class="group-name">{{ compilation.name_trc}}</span>
                <span class="music-name" >{{ compilation.name_per}}</span>
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
            url: 'track?genre=all&bool=0',
            loading: false,
            sort: 'popular',
            genre: '',
            style: '',
            showsortbutton: true
          //hoverClass: 'disk'
        }
    },
    mounted(){
        document.body.addEventListener("scroll", this.onScroll, false);
    },
    methods: {
     checkSort(e)
        {
            e.preventDefault();
            if(e.target.style.backgroundColor=="rgba(192, 192, 192, 0.8)")
            {
                document.getElementById('time').style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1";
                document.getElementById('topic').style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1";
                e.target.style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1"
            }
            else
            {
                document.getElementById('time').style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1";
                document.getElementById('topic').style="background-color: rgba(192,192,192,0);border-bottom: none;line-height: 1";
                e.target.style="background-color: rgba(192,192,192,0.8);border-bottom: 2px solid currentColor;line-height: 0.85;color: rgb(0,0,0)";
            }
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
        showGenre: function(message1 = null, message2 = null, message3 = null) {
          this.loading = true;
          var obj = {};
          if(message1 != null || message2 != null)
          {
            this.url = 'track';
            this.compilations = [];
            if(message1 != null) {
                this.genre = message1;
                if (!(isNaN(this.genre))) {
                    this.getGengeAndStyles(this.genre);
                }
                else {
                    this.getGengeAndStyles()
                }
                this.style = null;
            }
            if(message2 != null) {
                this.style = message2;
                this.genre = null;
            }
            if(message3 != null) {
                this.sort = message3;
            }
            if(this.genre === 'rec' || this.genre === 'fav') {
                this.showsortbutton = false;
            }
            else {
                this.showsortbutton = true;
            }
            obj = {params: {gen: this.genre, sty: this.style, bool: this.sort}}
          }
          this.$http.get(this.url, obj/*{params: {genre: message}}*/).then(function(response){
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
        trackClick: function(index) {
            //this.$emit('trackclicked');
            this.$bus.$emit('trackclicked', {
				id: this.compilations[index].id
			});
        },
        //для Илюши
        getGengeAndStyles: function (message = null) {
            this.$http.get('genre', {params: {id: message}}).then(function(response){
                // console.log(response.data)
                if(message == null) {
                    this.genres = response.data;
                    this.styles = null;
                }
                else
                    this.styles = response.data;
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
/*Рекомендации и сортировка*/
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
    color: rgba(0,0,0,0.55);
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
    /* content: '🕒'; */
    margin-right:5px; 
}
.topic:before
{
    font-family: "FontAwesome";
    content: "\f06d";
    /* content: '⚡'; */
    margin-right:5px; 
}
/*рекомендации*/
.music-style-conteiner
{
    background-color: rgb(85, 85, 85);
    top: 0px;
    left: 0px;
    height: 40px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    justify-content: center;
}
.music-style
{
    background-color: rgb(85, 85, 85);
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
.janrStyles-conteiner
{
    box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    -webkit-box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    -moz-box-shadow:0px -2px 6px 2px rgba(0,0,0,0.64)inset;
    background-color: rgb(55, 55, 55);
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
.janr
{
    padding: 0 15px;
}
.janr:hover
{
    cursor: pointer;
    background-color: rgba(192,192,192,0.8);
    border-bottom: 2px solid currentColor;
    line-height: 1.6;
    box-shadow: 0 6px 12px rgba(0,0,0,0.25), 0 5px 5px rgba(0,0,0,0.22);
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
    width:100%; 
    cursor: pointer;
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
    position: relative;
    cursor: pointer;
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
    filter:sepia(50%);
    height: auto;
    -o-transform: translateX(8.3%);
    -ms-transform: translateX(8.3%);
    -moz-transform: translateX(8.3%);
    -webkit-transform: translateX(8.3%);
    transform: /*scale(1.05)*/ translateX(8.3%);
    transition-duration: .7s;
    cursor: pointer;
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
    opacity: 0.6;
    transition: 1.4s transform;
    display: none;
    cursor: pointer; 
    background-color: rgba(85, 85, 85,0.6);
    padding: 5%;
    border-radius: 50px;
    width: 22%;
    height: 22%;
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
    width: 100%;
    height: 100%;
} 
.play
{
    right: 35%;
}
.turn
{
    left:35%;
}
</style>