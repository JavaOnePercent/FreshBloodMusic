<template>
    <div class="compositor-top">
        <label>
            Лучшие исполнители
        </label>
        <div class="compositors" id="compositors">
            <div class="compositor" :key="index" v-for="(compositor, index) in compositors">
                <img class="compositor-avatar" :src="compositor.image_per" alt="обложка">
                <label class="compositor-name">{{ compositor.name_per}}</label>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'performer-top',
    data: function() {
        return{
          compositors: []
        }
    },
    methods: {
        showBest: function() {
            this.$http.get('best_performer/').then(function(response){
                //console.log(response);
                this.compositors = response.data;
                /*this.compositors.forEach(function(item, i, arr) {
                    item[1] = "/static/mainapp/performer_sources/" + item[1];
                });*/
                //alert(this.compositors);
            }, function(error){
            })
        },

    },

    created: function() {
        this.showBest()
    }
}
</script>

<style scoped>
.compositor-top
{   
    z-index: 70;
    display: flex;
    flex-direction: column;
    color:black;
    background-color: rgb(140, 140, 140);
    font-size: 20px;
    box-shadow:  0 -2px 4px rgba(0, 0, 0, .3), /*тут бы поиграть с тенями*/
    -23px 0 20px -23px rgba(0, 0, 0, .8),
    23px 0 20px -23px rgba(0, 0, 0, .8),
    0 0 40px rgba(0, 0, 0, .1) inset;
}
.compositor
{
    cursor: pointer;
    background-color: rgb(115, 115, 115);
    flex-basis: 80.6666667px;
    line-height:80.6666667px;
    font-size: 25px;
    margin-bottom: 16px;
}
.compositor label
{
    cursor: pointer;
}
.compositor:hover
{
    color: white;
    background-color: rgba(51, 51, 51,0.8);
    box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
}
.compositor-avatar
{
    padding: 0;
    height: 80.6666667px;
    width: 80.6666667px;
    float: left
}
.compositor-top label
{
    line-height:60px;
}
</style>