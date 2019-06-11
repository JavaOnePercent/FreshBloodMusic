<template>
    <div class="statisticConteiner">
        <div class="row"> 
            <h2 v-if="statisticFor==='performer'"> Общее по профилю </h2>
            <h2 v-if="statisticFor==='album'">
                <img src="/static/mainapp/images/left-arrow.svg" @click="statisticID=$store.state.myPerformerID; statisticFor='performer'">
                Статистика по альбому "{{albumName}}" 
            </h2>
            <h2 v-if="statisticFor==='track'">
                <img src="/static/mainapp/images/left-arrow.svg" @click="statisticID=albums[curAlb].album.id; statisticFor='album'">
                Статистика по композиции "{{trcName}}" 
            </h2>
            <div class="controll">
                <div class="dayBtn" :class="{'current':period==='week'}" @click="period='week'">
                    неделя
                </div>
                <div class="dayBtn" :class="{'current':period==='month'}" @click="period='month'">
                    месяц
                </div>
                <div class="dayBtn" :class="{'current':period==='year'}" @click="period='year'">
                    год
                </div>
                <label>Тип графика:</label>
                <div v-click-outside="()=>{type_opened = false}" class="dropdown" @click="type_opened = !type_opened; data_opened = false">
                    {{grafType[typeId].name}}
                    <img class='arrow' src="/static/mainapp/images/arrow.svg" alt="arrow" :style="arrowRotationType"/>
                    <ul v-if="type_opened" class='dropdown_ul'>
                        <li :key="index" v-for="(type, index) in grafType" @click="typeId=index">
                            {{type.name}}
                        </li>
                    </ul>
                </div>
                <label style="left: -90px;">Тип данных:</label>
                <div v-click-outside="()=>{data_opened = false}" class="dropdown" style="left:-185px;" @click="data_opened = !data_opened; type_opened = false">
                    {{dataType[dataId].name}}
                    <img class='arrow' src="/static/mainapp/images/arrow.svg" alt="arrow" :style="arrowRotationData"/>
                    <ul v-if="data_opened" class='dropdown_ul'>
                        <li :key="index" v-for="(data, index) in dataType" @click="dataId=index">
                            {{data.name}}
                        </li>
                    </ul>
                </div>
            </div>
            <GChart v-if="error === '' && render && chartData != []"
                :type = grafType[typeId].type
                :data="chartData"
                :options="chartOptions"
            />
            <h2 style="top:12px;" v-else>{{error}}</h2>
            <h2 v-if="statisticFor==='performer'"> Издания </h2>
            <div v-if="statisticFor==='performer'" style="display: flex; flex-wrap: wrap; position:reletive">
                <div :key="index" v-for="(album, index) in albums" :class='{chousen:(statisticID==album.album.id && statisticFor=="album")}' class="album"
                @click="statisticFor='album'; statisticID=album.album.id; albumName=album.album.name_alb; curAlb = index">
                    <img :src="album.album.image_alb">
                    <span class="album-name"> {{album.album.name_alb}} </span>
                </div>
            </div>
            <h2 v-if="statisticFor==='album' || statisticFor==='track'"> Композиции </h2>
            <div v-if="statisticFor==='album' || statisticFor==='track'" style="display: flex; flex-wrap: wrap; position:reletive">
                <div :key="index" v-for="(trc, index) in music" :class='{chousen:(statisticID==trc.id && statisticFor=="track")}' class="trc"
                @click="statisticFor='track'; statisticID=trc.id; trcName=trc.name_trc">
                    <span class="trc-name"> {{trc.name_trc}} </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { GChart } from 'vue-google-charts'
export default {
    name: 'statistic',
    data() {
        return {
            type_opened: false,
            data_opened: false,
            addToTable : false,
            curAlb: null,
            render: false,
            albumName: '',
            trcName: '',
            error: '',
            arrow_rotation: {rotation: null},
            chartData: [],
            chartOptions: {
                // chart: {
                //     title: 'Company Performance',
                //     subtitle: 'Sales, Expenses, and Profit: 2014-2017'
                // },
                height: 400,
            },
            grafType: [
                {type: 'AreaChart', name: 'Диаграмма с областями'},
                {type: 'LineChart', name: 'Линейный график'},
                {type: 'ColumnChart', name:'Столбчатая диаграмма'},
                // {type: 'PieChart', name: 'Круговая диаграмма'},
                {type: 'ScatterChart', name: 'Точечная диаграмма'},
                // {type: 'BubbleChart', name: 'Пузырчатая диаграмма'},
                {type: 'Table', name: 'Таблица'},
            ],
            dataType: [
                {type: 'likes', name: 'Лайки'},
                {type: 'plays', name: 'Прослушивания'},
                {type: 'likes + plays', name:'Лайки + Прослушивания'},
            ],
            typeId: 1,
            dataId: 0,
            period: 'week',
            albums: [],
            music: [],
            statisticID: this.$store.state.myPerformerID,
            statisticFor: 'performer',
            }
    },
    watch: {
        typeId: 'getData',
        dataId: 'getData',
        period: 'getData',
        statisticID: 'getStatisticForData',
        statisticFor: 'getStatisticForData'
    },
    computed: {
        arrowRotationType() {
            if(this.type_opened) return 'transform: rotate(-180deg)'
            else return ''
        },
        arrowRotationData() {
            if(this.data_opened) return 'transform: rotate(-180deg)'
            else return ''
        }
    },
    created() {
        this.getData()
        this.getAlbums()
    },
    components: {
        GChart
    },
    methods: {
        getData(){
            if (this.dataType[this.dataId].type === 'likes + plays')
            {
                this.getChartData('plays')
            }
            else this.getChartData()
        },
        getChartData(data = this.dataType[this.dataId].type) {
        this.render = false
        var params = {
            entity: this.statisticFor,
            entity_id: this.statisticID ,
            x: this.getX(),
            y: data,
            days: this.getPeriodDate(),
        }
        this.$http.get('../api/statistics', {params}).then(function(response){
                console.log(response.body)
                this. error = ''
                if (response.body.length === 0 && !this.addToTable)
                {
                    this.error = 'Данных за этот период нет'
                    this.render = true
                    return
                }
                if (this.dataType[this.dataId].type === 'likes + plays' && this.addToTable)
                {
                    this.addToTable = false
                    if(response.body.length===0) {
                        this.render = true
                        return 
                    }
                    this.chartData[0] = [this.getX(false), 'прослушивания', 'лайки']
                    var self = this
                    response.body.map(function(elem) {
                        for (var i = 1; i < self.chartData.length; i++) {
                            console.log(self.chartData[i][0])
                            console.log(elem.date)
                            if (self.chartData[i][0] == (self.period === 'year'?self.getCorrectMonth(elem.month):elem.date))
                            {
                                var prev = self.chartData[i][1]
                                console.log(prev)
                                self.chartData[i] = [self.chartData[i][0], prev, elem.amount]
                            }
                            else if(!self.chartData[i][2] || (self.chartData[i][2]===0)) {
                                var prev = self.chartData[i][1]
                                console.log(prev)
                                self.chartData[i] = [self.chartData[i][0], prev, 0]
                            }
                        self.render = true
                        }
                    });
                }
                else {
                this.chartData = []
                var chartHead = [this.getX(false), this.dataType[this.dataId].type === 'likes'?'лайки':'прослушивания']
                this.chartData.push(chartHead)
                var self = this
                response.body.map(function(elem) {
                    var chartElem = [elem.date || self.getCorrectMonth(elem.month), elem.amount]
                    self.chartData.push(chartElem)
                    self.render = true
                });
                if (this.dataType[this.dataId].type === 'likes + plays')
                    {
                        this.addToTable = true
                        this.getChartData('likes')
                    }
                }
            }, function(error){
            })
        },
        getPeriodDate() {
            switch (this.period) {
            case 'week':
                return 7
            case 'month':
                return 30
            case 'year':
                return 365
            }
        },
        getX(chart=true) {
            if(this.period === 'week' || this.period ==='month')
                return chart?'day':'день'
            else return chart?'month':'месяц'
        },
        getCorrectMonth(id) {
            var months = ['январь', 'февраль', 'март', 'апрель','май', 'июнь', 'июль', 'август','сентябрь', 'октябрь', 'ноябрь', 'декабрь'];
            return months[id]
        },
        getAlbums() {
            var id = this.$store.state.myPerformerID; // берём id адресс из пути url
            var self = this
            this.$http.get('../api/albums?performer=' + id).then(function(response){ //Запос к апи сервера
                self.albums = []
                response.body.map(function(item){
                    var obj = {album: item} //форимируем из ответа объект необходимого формата
                    self.albums.push(obj)  //записываем информацию об альбоме 
                });
            }, function(error){
            });
        },
        getMusic() {
            var self = this
            this.$http.get('../api/albums/' + this.statisticID).then(function(response){
                console.log('music',response.body)
                self.music = []
                response.body.tracks.map(function(item){
                    self.music.push(item)
                });
            }, function(error){});
        },
        getStatisticForData() {
            if (this.statisticFor === 'album')
            {
                this.getMusic()
                this.getData()
            }
            else this.getData()
        }
    },

}
</script>

<style scoped src="./Statistic.css">

</style>