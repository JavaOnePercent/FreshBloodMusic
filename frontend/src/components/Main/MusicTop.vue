<template>
  <div class="music-top">
    <div id="next-page" class="next-page"></div>
    <div id="previous-page" class="previous-page"></div>
    <div class="infotrack" :key="index" v-for="(infotrack, index) in infotracks">
    <img class="img" :src="infotrack.image_alb" alt="обложка">
    <div class="text">
            <label>Лучшая в этом месяце</label>
            <p>{{ infotrack.name_per}} - {{ infotrack.name_trc}}</p>
                <p>Понравилась: {{ infotrack.rating_trc}} пользователям</p>
                <div class="play">
                    <i class="fa fa-play fa-4x" aria-hidden="true"></i>
                </div>
                <div class="turn">
                    <i class="fa fa-align-justify fa-4x" aria-hidden="true"></i>
                </div>
    </div>
    </div>
</div>
</template>

<script>
export default {
    name: 'music-top',
    data: function() {
        return{
          infotracks: []
        }
    },
    methods: {
        showMonth: function() {
            this.$http.get('top_month/').then(function(response){
                //console.log(response);
                this.infotracks = response.data;
                /*this.infotracks.forEach(function(item, i, arr) {
                    item[2] = "/media/albums/" + item[2];
                });*/
                //alert(this.infotracks);
            }, function(error){
            })
        },
    },
    created: function() {
        this.showMonth()
    }
}
</script>

<style scoped>
.img /*обложка лучшей композиции*/
{
    padding: 15px 15px 15px 3.82%;
    display: block;
    height: 320px;
    width: 320px; 
    position: absolute;
    float: left;
}
.music-top, .compositor-top
{
    text-align: center;
    color: white;
    flex-basis: 400px;
}
.next-page:hover, .previous-page:hover
{
    background-color: rgba(255, 254, 255, 0.10);
}
.next-page, .previous-page
{
    cursor: pointer;
    border: none;
    background: transparent;
    display: block;
    z-index: 110;
    width: 10%;
    height: 350px;
    position: relative;
}
.next-page
{
    
    opacity: 0.4;
    background-size: 35px;
    background-position: left center;
    background-repeat:no-repeat;
    background-image:url(/static/mainapp/images/left.png);
    float: left;
}
.previous-page
{
    background-size: 35px;
    opacity: 0.4;
    background-position: right center;
    background-repeat:no-repeat;
    background-image:url(/static/mainapp/images/right.png);
    float: right;
}
.text
{
    left:45%;
    text-align: left;
    position: relative;
}
.music-top
{
    
    display: inline-block;
    background-color: rgb(85, 85, 85);
    flex-grow: 0.3; 
}
.music-top p
{
    position: relative;
    font-size: 20px;
}
.music-top label
{
    
    position: relative;
    font-size: 25px;
    line-height:60px;
}
</style>