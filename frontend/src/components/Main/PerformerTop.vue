<template>
    <div class="performer-top" @mouseenter="mouseEnter" @mouseleave="mouseLeave">
        
        <div class="prev-button" v-show="isHovered" @click="show('prev')"></div>
        <div class="next-button" v-show="isHovered" @click="show('next')"></div>
        <div class="performers">
            <transition :name="animation" mode="in-out">
                <div v-if="compositors[0]" v-show="showDiv" @click="goToPerformer(compositors[0].id)" class="performer">
                    <label class="performer-text">
                        Лучший исполнитель этого месяца
                    </label>
                    <img class="performer-image" :src="compositors[0].image_per" alt="обложка">
                    <label class="performer-name">{{ compositors[0].name_per}}</label>
                </div>
            </transition>
            <transition :name="animation" mode="out-in">
                <div v-if="compositors[1]" v-show="!showDiv" @click="goToPerformer(compositors[1].id)" class="performer">
                    <label class="performer-text">
                        Лучший исполнитель этого месяца
                    </label>
                    <img class="performer-image" :src="compositors[1].image_per" alt="обложка">
                    <label class="performer-name">{{ compositors[1].name_per}}</label>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
export default {
    name: 'performer-top',
    data() {
        return{
            compositors: [],
            performers: [],
            isHovered: false,
            animation: "",
            showDiv: true,
            isTimeout: false,
            autoFlip: null
        }
    },
    watch: {
        showDiv(sD) {
            setTimeout(this.carousel, 500, sD);
        }
    },
    methods: {
        carousel(sD) {
            if(sD)
                if(this.compositors[0] === this.performers[this.performers.length - 1])
                    this.compositors[1] = this.performers[0]
                else if(this.compositors[1] === this.performers[this.performers.length - 1])
                    this.compositors[1] = this.performers[1]
                else
                    this.compositors[1] = this.performers[this.performers.indexOf(this.compositors[1]) + 2]
            else
                if(this.compositors[1] === this.performers[this.performers.length - 1])
                    this.compositors[0] = this.performers[0]
                else if(this.compositors[0] === this.performers[this.performers.length - 1])
                    this.compositors[0] = this.performers[1]
                else
                    this.compositors[0] = this.performers[this.performers.indexOf(this.compositors[0]) + 2]
        },
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
                if(e === 'next')
                    this.animation = "animation";
                else if(e === 'prev')
                    this.animation = "animation1";
                this.isTimeout = true;
                var self = this
                setTimeout(function() { self.isTimeout=false }, 500);
                //this.animation = "";
                this.showDiv=!this.showDiv
                clearInterval(this.autoFlip)
                this.autoFlip = setInterval(this.updatePosts, 7000);
            }
        },
        mouseEnter() {
            this.isHovered = true
        },
        mouseLeave() {
            this.isHovered = false
        },
        showBest() {
            this.$http.get('api/performers').then(response => {
                //console.log(response.data)
                this.compositors = [response.data[0], response.data[1]]
                this.performers = response.data
            })
        },

        goToPerformer(id) {
            this.$router.push({ path: '/performers/' + id})
        }
    },

    created() {
        this.showBest()
        var self = this
        setTimeout(function() { self.autoFlip = setInterval(self.updatePosts, 7000); }, 3500);
        
    }
}
</script>

<style scoped>
@media (max-width: 985px) {
    .performer-top
    {
        display: block;
        height: 100%;
        float: left;
        text-align: center;
        color: white;
        width: 330px;
        overflow: hidden;
    }
}

@media (min-width: 984px) {
    .performer-top
    {
        display: block;
        height: 100%;
        float: right;
        text-align: center;
        color: white;
        width: 280px;
        overflow: hidden;
    }
}
.performer-top
{   
    z-index: 100;
    color:black;
    background-color: white;
    font-size: 20px;
    box-shadow: 0 0 40px rgba(0, 0, 0, .1) inset;
    /*box-shadow:  0 -2px 4px rgba(0, 0, 0, .3),
    -23px 0 20px -23px rgba(0, 0, 0, .8),
    23px 0 20px -23px rgba(0, 0, 0, .8),
    0 0 40px rgba(0, 0, 0, .1) inset;*/
    position: relative;
}
.performer
{
    cursor: pointer;
    /*background-color: rgb(115, 115, 115);*/
    margin-bottom: 16px;
    width: 100%;
    height: 100%;
    position: absolute;
    
}
.performer-image
{
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    width: 240px;
    height: 240px;
    position: absolute;
    margin: auto;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
}

.prev-button 
{
    position: absolute;
    top: 0;
    width: 100%;
    height: 35px;
    z-index: 50;
    background: url(/static/mainapp/up.svg), linear-gradient(180deg, rgba(0, 0, 0, 0.5), rgba(255, 255, 255, 0.0));
    background-size: 35px;
    background-position: top center;
    background-repeat: no-repeat;
    border: none;
    cursor: pointer;
}

.next-button 
{
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 35px;
    z-index: 50;
    background:url(/static/mainapp/down.svg), linear-gradient(0deg, rgba(0, 0, 0, 0.5), rgba(255, 255, 255, 0.0));
    background-size: 35px;
    background-position: bottom center;
    background-repeat: no-repeat;
    cursor: pointer;
}

.performer-name
{
    font-size: 25px;
    line-height:40px;
    position:absolute;
    width: 90%;
    height: 40px;
    margin: auto;
    left: 0;
    right: 0;
    bottom: 10px;
    text-align: center;
    overflow-x:hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    cursor: pointer;
}

.performer-text
{
    top: 5px;
    position: absolute;
    margin: auto;
    width: 90%;
    height: 40px;
    left: 0;
    right: 0;
    cursor: pointer;
}

.animation-enter-active, .animation-leave-active {
  transition: all 0.5s;
}
.animation-enter, .animation-leave-active {
  opacity: 0;
}
.animation-enter {
  transform: translateY(100%);
}
.animation-leave-active {
  transform: translateY(-100%);
}

.animation1-enter-active, .animation1-leave-active {
  transition: all 0.5s;
}
.animation1-enter, .animation1-leave-active {
  opacity: 0;
}
.animation1-enter {
  transform: translateY(-100%);
}
.animation1-leave-active {
  transform: translateY(100%);
}
</style>