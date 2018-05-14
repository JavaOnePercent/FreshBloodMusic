<template>
    <div id="compilation-top">
        <div class="recommendations">
            <div class="sortirovka">
                <label class="sortirovka-name">Рекомендации</label>
                <div class="sort">
                    <label>Отсортировать по:</label>
                    <a class="time" id="button" @click="showGenre(genre, 'time')">времени</a>
                    <a class="topic" id="button" @click="showGenre(genre, 'popular')">популярности</a>
                </div>
            </div>
            <div class="music-style">
                <a class="janr" name="" @click="showGenre('all')">Все</a>
                <a class="janr" name="" @click="showGenre('rec')">Рекомендации</a>
                <a class="janr" name="" @click="showGenre('fav')">Избранное</a>
                <div class="gen" :key="index" v-for="(gen, index) in genreandstyles">
                    <a class="janr" :name="gen.id" @click="showGenre(gen.id)">{{gen.name_gnr}}</a>
                </div>
            </div>
        </div>
        <div class="compilation convert" ref="list">
            <div class="music" :key="index" v-for="(compilation, index) in compilations">
                <img class="cover" :src="compilation.image_alb" alt="обложка" @click="trackClick(index)">
                <img class="disk" :src="compilation.image_alb" alt="disk">
                <span :title="compilation.name_trc" class="group-name">{{ compilation.name_trc}}</span>
                <span class="music-name" >{{ compilation.name_per}}</span>
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
            genreandstyles:[],
            url: 'track?genre=all&bool=0',
            loading: false,
            sort: '',
            genre: '',
          //hoverClass: 'disk'
        }
    },
    mounted(){
        document.body.addEventListener("scroll", this.onScroll, false);
    },
    methods: {
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
        showGenre: function(message1 = null, message2 = null) {
          this.loading = true;
          var obj = {};
          this.sort = 'popular';
          if(message1 != null)
          {
            this.url = 'track';
            this.compilations = [];
            this.genre = message1;
            if(message2 != null)
                this.sort = message2;

            obj = {params: {gen: this.genre, bool: this.sort}}
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
            this.$http.get('genre').then(function(response){
                this.genreandstyles = response.data;
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
    height: 80px;
    width: 100%;
    margin: 0 auto;
    position: relative;
    display: flex;
    flex-direction: column;
}
.recommendations .sortirovka, .recommendations .music-style
{
    flex-basis: 100px;
    display: flex;
    height: 40px;
    font-size: 20px;
    justify-content: center;
    line-height:40px;
}
/*сортировка*/
.sortirovka-name, .sort
{
    flex-basis: 305px;
    padding: 0 15px;
}
.sortirovka-name
{
    font-size: 30px;
}
.sort
{
    flex-grow: 0.4;
}
.sort a
{
    padding: 6px;
}
.sort a:hover
{
    cursor: pointer;
    background-color: rgba(192,192,192,0.8);
    border-bottom: 2px solid currentColor;
    line-height: 0.85
}
.sort a:before
{
    font-family: "FontAwesome";
    content: "\f017";
    margin-right:5px; 
}
.sort a:nth-child(3)::before
{
    font-family: "FontAwesome";
    content: "\f06d";
    margin-right:5px; 
}
/*рекомендации*/
.music-style
{
    color: white;
    background-color: rgb(85, 85, 85);
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
    line-height: 1.5;
    box-shadow: 0 6px 12px rgba(0,0,0,0.25), 0 5px 5px rgba(0,0,0,0.22);
}
/*подборка*/

.compilation
{
    max-width: 1143px;
    margin: 0 auto;
    position: relative;
    padding-top: 25px;
    align-items: flex-end;
    display: flex;
    flex-wrap: wrap;
}

.compilation .music
{
    
    position: relative;
    padding-right: 2.5%;
    padding-left: 2.5%;
    padding-bottom: 20px;
    flex-basis: 20%;
    overflow: hidden;
    min-height: 195px;
    max-height: 300px;
    text-align: center;
}

.cover
{
    
    border: none;
    image-rendering: -webkit-crisp-edges;
    backface-visibility: hidden;
    transition: 1.4s transform;
    position:relative;
    z-index: 50;
    top: 0; right: 0; bottom: 0; left: 0;
    display: block;
    height: auto;
    width: 100%; 
    padding: 0;
}
.disk
{
    border-radius: 50%;
    margin: 0 auto auto auto;
    transition: 1s transform;
    backface-visibility: hidden;
    position:absolute;
    z-index: 40;
    top: 0.8%; right: 0; bottom: 0; left: 0;
    display: block;
    height: auto;
    width: 76%; 
    padding: 0;

}
.cover:hover + .disk
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
.cover:hover~span
{
    transition-duration: .7s;
    transform: /*scale(1.05)*/ translateX(8.3%) /*translateY(5px)*/;
}
.group-name
{
    cursor: pointer;
    backface-visibility: hidden;
    transition: 1.4s transform;
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
    backface-visibility: hidden;
    transition: 1.4s transform;
    overflow-x:hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: grey;
    display: block;
    font-size:18px; 
}
.cover:hover 
{
    image-rendering:  auto;
    z-index: 60;
    padding:0;
    filter:sepia(50%);
    height: auto;
    top: 0; right: 0; bottom: 0; left: 0;
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
</style>