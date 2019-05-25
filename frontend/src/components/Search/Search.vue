<template>
    <div class="searchConteiner">
        <input id="Search" v-model="search" class="search" type="text"  placeholder="Назваине трека, испольнителя" autocomplete="off"
        @focus="GetHistory(), GetTips() ; currentTip=-1; showTips=true" @blur="showTips=false" @input="GetTips"
        @keydown.down="control($event,'down')" @keydown.up="control($event,'up')" @keydown.enter="control($event,'enter')"/>
        <img title="поиск" src="/static/mainapp/images/lupa.svg" @click="goTolocalStorage">
        <!-- <div v-if="showTips && history.length>0 "> -->
        <div v-if="showTips && history.length>0 && tips.length === 0 " class="tips-cont">
            <div class="row">
                <div v-if="showTips && history.length>0 && tips.length === 0 " class="tips">
                    <div :class="{'current':currentTip===index}" class="tip"  :key="index" v-for="(el, index) in filteredList"
                    @mouseover="currentTip=index" @mousedown="SearchFrocus" @mouseleave="currentTip=-1" @click="search=el; goTolocalStorage()">
                        <span> {{el}} </span>
                    </div>
                </div>
            </div>
        </div>
        <div v-else  class="tips-cont">
            <div class="row">
                <div v-if="showTips && tips.length !== 0 "  class="tips">
                    <div :class="{'current':currentTip===index}" class="tip"  :key="index" v-for="(el, index) in tips"
                    @mouseover="currentTip=index" @mousedown="SearchFrocus" @mouseleave="currentTip=-1" @click="search=el.name; goTolocalStorage()">
                        <img v-if="el.image" :src="'/media/' + el.image">
                        <span> {{el.name}} <span style="color:rgb(184, 184, 184)"> {{type(el.type)}} </span></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'search',
    data() {
        return {
            search: '',
            currentTip: -1,
            showTips:false,
            history: [],
            tips: []
        }
    },
    computed: {
        filteredList() {
        return this.history.filter(el => {
            return el.toLowerCase().includes(this.search.toLowerCase())
            })
        }
    },
    methods:{
        control(e, contoll) {
            // console.log(this.curId)
            var mass = []
            e.preventDefault();
            if (this.tips.length === 0)
                mass = this.history
            else
                mass = this.tips
            if(contoll === 'enter')
            {
                if(this.currentTip == -1)
                {
                    this.goTolocalStorage()
                    // document.getElementById('Search').blur()
                    return
                }
                this.search = mass[this.currentTip].name || mass[this.currentTip]
                document.getElementById('Search').blur()
                this.goTolocalStorage()
                this.curId = -1
                return
            }
            if (contoll === 'down')
                this.currentTip += 1
            else if (contoll === 'up')
                this.currentTip -= 1
            if (this.currentTip+1 > mass.length)
                this.currentTip = -1
            else if (this.currentTip < -1)
                this.currentTip = mass.length-1
            // if (this.currentTip > this.history.length-1)
            //     this.currentTip = -1
            // if (this.currentTip < 0)
            //     this.currentTip = this.history.length-1
        },
        goTolocalStorage() {
            if(this.search.length===0)
            {
                return
            }
            document.getElementById('Search').blur()
            var mas = []
            if (JSON.parse(localStorage.getItem("history"))){
                mas = JSON.parse(localStorage.getItem("history"))
                if(mas.length > 10)
                mas.shift()
            }
            for(let i = 0; i < mas.length; i++) {
                if (mas[i] === this.search)
                    mas.splice(i, 1)
            }
            mas.push(this.search)
            var serial = JSON.stringify(mas);
            localStorage.setItem("history", serial);
            this.$router.push('/search')
            this.$store.commit("updateSearchRec", this.search)
            this.$bus.$emit('Search', this.search)
        },
        GetHistory() {
            this.history=[]
            if (JSON.parse(localStorage.getItem("history"))){
                this.history = JSON.parse(localStorage.getItem("history"))
                this.history.reverse()
            }
        },
        SearchFrocus(e){
            e.preventDefault()
            return false;
        },
        GetTips() {
            if(this.search.length===0)
            {
                this.tips = []
                return
            }
            this.$http.get('../api/search?query=' + this.search.toLowerCase() + '&suggest=true').then(function(response){
                console.log(response.body)
                this.tips = response.body.results
                this.tips.reverse()
            });
        },
        type(type) {
            switch(type)
            {
                case 'performer':
                    return 'исполнитель'
                case 'album':
                    return 'альбом'
                case 'track':
                    return 'композиция'
            }
        },
    }
}
</script>

<style scoped>
    .searchConteiner
    {
        /* position: absolute; */
        /* left: 245px; */
        position: relative;
        float: left;
        height: 100%;
        width: 300px;
    }
    .search
    {
        top: 8.5px;
        height: 28px;
        padding: 2.5px 5px;
        width: 285px;
        padding-right: 25px;
        position: absolute;
        border: 1px solid rgb(204, 204, 204);
    }
    .row
    {
        position: relative;
        margin: auto;
        display: block;
        max-width: 1280px;
        min-width: 915px;
        left: 245px;
        transform: translateX(0%);
        /* right: 0;
        left: 0; */
    }
    .searchConteiner img
    {
        width: 18px;
        position: absolute;
        top: 17.5px;
        left: 295px;
        opacity: 0.5;
    }
    .searchConteiner img:hover
    {
        opacity: 1;
        cursor: pointer;
    }
    *:focus, *:hover
    {
        outline: none;
    }
    .tips-cont
    {
        position: fixed;
        top: 55px;
        background-color:rgb(255, 255, 255);
        border-top: 1px solid rgb(204, 204, 204);
        width: 100%;
        height: auto;
        left: 0;
        box-shadow: 0 15px 15px -15px #333;
    }
    .tips
    {
        height: auto;
        /* max-height: 200px; */
        top: 55px;
        /* position: absolute; */
        /* min-width: 100%; */
        width: auto;
        max-width: 500px;
        z-index: 1;
    }
    .tips:nth-last-child(1)
    {
        margin-bottom: 7px;
    }
    .tip
    {
        display: block;
        position: relative;
        width: 100%;
        padding: 5px;
        height: 35px;
        line-height: 25px;
        box-sizing: border-box
    }
    .tip:hover
    {
        cursor: pointer;
    }
    .tip img
    {
        position:absolute;
        width: 30px;
        opacity: 1;
        left: 0;
        top:2px;
    }
    .tip img+span
    {
        left: 30px;
        position: relative
    }
    .current
    {
        border-bottom: 1px solid rgb(255, 181, 43);
        background-color: rgba(210,210,210, 0.4)
    }
</style>