<template>
<transition name="fade" mode="in-out">
    <div id="music-top" class="music-top" @mouseenter="stopFlipping" @mouseleave="startFlipping">
        <div id="next-page" class="next-page" @click="show"></div>
        <div id="previous-page" class="previous-page" @click="show"></div>

        <transition :name="animation" mode="in-out">
            <div class="infotrack" v-show="showDiv" v-if="infotracks[0]">
                <img class="img" :src="infotracks[0].image_alb" alt="обложка">
                <div class="text">
                    <span>Лучший трек этого месяца</span>
                    <p>{{ infotracks[0].name_per}} <br> {{ infotracks[0].name_trc}}</p>
                    <div class="play btn" @click="playClick(infotracks[0].id)"><img title="Воспроизвести" class="playIm"  src="/static/mainapp/images/Wplay.svg" alt="play"></div>
                    <div class="turn btn" @click="toQueueClick(infotracks[0].id)"><img title="В очередь" class="turnIm" src="/static/mainapp/images/Wplaylist.svg" alt="turn"></div>
                    <p>Понравилась: {{ infotracks[0].rating_trc}} пользователям</p>
                    <P>Жанр: {{ infotracks[0].name_gnr}} / {{ infotracks[0].name_stl}}</p>
                </div>
            </div>
        </transition>
        <transition :name="animation" mode="out-in">
            <div class="infotrack" v-show="!showDiv" v-if="infotracks[1]">
                <img class="img" :src="infotracks[1].image_alb" alt="обложка">
                <div class="text">
                    <span>Лучший трек этой недели</span>
                    <p>{{ infotracks[1].name_per}} <br> {{ infotracks[1].name_trc}}</p>
                    <div class="play btn" @click="playClick(infotracks[1].id)"><img title="Воспроизвести" class="playIm"  src="/static/mainapp/images/Wplay.svg" alt="play"></div>
                    <div class="turn btn" @click="toQueueClick(infotracks[1].id)"><img title="В очередь" class="turnIm" src="/static/mainapp/images/Wplaylist.svg" alt="turn"></div>
                    <p>Понравилась: {{ infotracks[1].rating_trc}} пользователям</p>
                    <P>Жанр: {{ infotracks[1].name_gnr}} / {{ infotracks[1].name_stl}}</p>
                </div>
            </div>
        </transition>
    </div>
</transition>
</template>

<script>
export default {
    name: 'music-top',
    data: function() {
        return{
            infotracks: [],
            animation: "",
            showDiv: true,
            isTimeout: false,
            autoFlip: null
        }
    },
    methods: {
        updatePosts: function () {
            if(!this.isTimeout)
            {
                this.isTimeout = true
                var self = this
                setTimeout(function() { self.isTimeout=false }, 500);
                this.showDiv=!this.showDiv
                this.animation = "animation";
            }
        },
        show(e){
            if(!this.isTimeout)
            {
                if(e)
                {
                    if(e.target.id== "previous-page")
                        this.animation = "animation";
                    else
                        this.animation = "animation1";
                }
                this.isTimeout = true;
                var self = this
                setTimeout(function() { self.isTimeout=false }, 500);
                //this.animation = "";
                this.showDiv=!this.showDiv
                clearInterval(this.autoFlip)
                this.autoFlip = setInterval(this.updatePosts, 7000);
            }
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
        startFlipping() {
            clearInterval(this.autoFlip)
            this.autoFlip = setInterval(this.updatePosts, 7000);
        },
        stopFlipping() {
            clearInterval(this.autoFlip)
        },
    },
    created: function() {
        this.autoFlip = setInterval(this.updatePosts, 7000);
        this.$http.get('api/tracks', {params: {filter: 'popular', limit: 1, interval: 31}}).then(function(response){
                this.$set(this.infotracks,0,response.data[0]);
            })
        this.$http.get('api/tracks', {params: {filter: 'popular', limit: 1, interval: 7}}).then(function(response){
                this.$set(this.infotracks,1,response.data[0]);
            })
    }
}
</script>

<style scoped>
@media (max-width: 984px)   {
    .music-top 
    {
        width: 540px;
        float: left;
        color: white;
        text-align: center;
    }
    .img /*обложка лучшей композиции*/
    {
        object-position: center;
        max-width: 100%;
        padding: 15px 15px 15px 0px;
        display: block;
        height: 250px;
        width: 250px; 
        position: absolute;
        margin: auto 0;
        top: 30px; right: 0; bottom: 0; left: 0;
        float: left;
    }
     .text
    {
        left: 265px;
        width: 265px;
        text-align: left;
        position: relative;
    }
    .music-top span
    {
        white-space: nowrap;
        width: 300px;
        position: relative;
        right: 50%;
        font-size: 22px;
        line-height:60px;
    }
    .text :nth-child(5)
    {
        margin-top:29.3px;
    }
    .text :nth-child(2)
    {
        margin: 0;
    }
    .btn
    {
        margin-top:29.3px;
    }
    .previous-page
    {
        left: 93.5%;
    }
    .next-page
    {
        /* left: -15px; */
    }
}

@media (min-width: 985px) {
    .music-top
    {
        float: left;
        text-align: center;
        color: white;
        width: calc(100% - 280px);
    }
    .img /*обложка лучшей композиции*/
    {
        max-width: 100%;
        padding: 15px 15px 15px 0px;
        display: block;
        height: 320px;
        width: 320px; 
        position: relative;
        float: left;
    }
    .text
    {
        float: left;
        width: 45%;
        text-align: left;
        position: relative;
    }
    .music-top span
    {
        white-space: nowrap;
        position: relative;
        font-size: 22px;
        line-height:60px;
    }
    .text :nth-child(5)
    {
        margin-top:37.3px;
    }
    .btn
    {
        margin-top:37.3px;
    }
    .previous-page
    {
        right: 0;
    }

}
.infotrack
{
    width: 100%;
    height: 325px;
    position: absolute;
}
.music-top:hover .next-page,.music-top:hover .previous-page
{
    display: block;
}
/* .next-page:hover, .previous-page:hover
{
    background-color: rgba(255, 254, 255, 0.10);
} */
.next-page, .previous-page
{
    display: block;
    cursor: pointer;
    border: none;
    background: transparent;
    z-index: 70;
    width: 35px;
    height: 350px;
    position: absolute;
}
.next-page
{  
    background:url(/static/mainapp/images/left.png), linear-gradient(90deg, rgba(0, 0, 0, 0.5), rgba(255, 255, 255, 0.0));
    display: none;
    /* opacity: 0.4; */
    background-size: 35px;
    background-position: left center;
    background-repeat:no-repeat;
    /* background-image:url(/static/mainapp/images/left.png); */
}
.previous-page
{
    background:url(/static/mainapp/images/right.png), linear-gradient(90deg,rgba(255, 255, 255, 0.0), rgba(0, 0, 0, 0.5) );
    display: none;
    background-size: 35px;
    /* opacity: 0.4; */
    background-position: right center;
    background-repeat:no-repeat;
    /* background-image:url(/static/mainapp/images/right.png); */
}
.music-top
{
    overflow: hidden;
    /* background-color: rgb(60, 60, 60); */
    transition: 100ms all;
    height: 350px;
    position: relative;
    display: inline-block;
    /* background-color: rgba(55, 55, 55,0);  */
}
.music-top p
{
    cursor:default;
    position: relative;
    font-size: 20px;
}
.text :nth-child(2)
{
    height: 46px;
}
.text :nth-child(5),.text :nth-child(6)
{
    font-size: 15px;
}
.btn
{
    width: 60px;
    height: 60px;
    display: inline-block;
}
.playIm
{
    width: 60px;
    height: 60px;
}
.turnIm
{
    position: absolute;
    top: 0;right: 0;left: 0;bottom: 0;
    margin: 10px auto 0 auto;
    width: 70px;
    height: 70px;
}
.play
{
    position: relative;
    cursor: pointer;
    margin-right: 20px;
}
.turn
{
    margin-top: 10px;
    position: relative;
    cursor: pointer;
    width: 70px;
    height: 70px;
}


.animation-enter-active, .animation-leave-active {
  transition: all 0.5s;
}
.animation-enter, .animation-leave-active {
  opacity: 0;
}
.animation-enter {
  transform: translateX(100%);
}
.animation-leave-active {
  transform: translateX(-100%);
}

.animation1-enter-active, .animation1-leave-active {
  transition: all 0.5s;
}
.animation1-enter, .animation1-leave-active {
  opacity: 0;
}
.animation1-enter {
  transform: translateX(-100%);
}
.animation1-leave-active {
  transform: translateX(100%);
}


</style>