<template>
    <div class="ResultConteiner">
        <div v-if="$route.path === '/search'" class="header">
            <h1> Результаты по запросу </h1>
            <p> {{search}} </p>
        </div>
        <div v-else class="header">
            <h1> Похожее на</h1>
            <p> {{similarName}} </p>
        </div>
        <div v-if="result.performer.length > 0" class="performers">
            <h2> Исполнители </h2>
            <div class="performer-cont">
                <div class="performer" @click="gotoPerformer(el.id)" :key="index" v-for="(el, index) in result.performer">
                    <img :src="'/media/' + el.image">
                    <span class="name" > {{el.name}} </span>
                </div>
                <div v-if="nextPageUrl.performer.length > 0" class="performer" @click="updatePage('performer', nextPageUrl.performer)">
                    <div class="more">
                        <span> Показать больше </span>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="result.track.length > 0" class="tracks">
            <h2> Композиции </h2>
            <div class="track-cont">
                <trackComp :tracks='result.track'> </trackComp>
                <div v-if="nextPageUrl.track.length > 0" class="track track-more" @click="updatePage('track', nextPageUrl.track)">
                    <div class="more">
                        <span> Показать больше </span>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="result.album.length > 0" class="albums">
            <h2> Альбомы </h2>
            <div class="album-cont">
                <div class="album" @click="choseAlbum=index; showAlbum=true" :key="index" v-for="(el, index) in result.album">
                    <img :src="'/media/' + el.image">
                    <span class="name" > {{el.name}} </span>
                </div>
                <div v-if="nextPageUrl.album.length > 0" class="album" @click="updatePage('album', nextPageUrl.album)">
                    <div class="more">
                        <span> Показать больше </span>
                    </div>
                </div>
            </div>
        </div>
            <div v-if="showAlbum">
                <div class="album-modal">
                    <TrackList @close="showAlbum=false" style="height: 80%; top:-15px; position: relative;" :albumType="'album'" :albumId="result.album[choseAlbum].id" :lable="'/media/' + result.album[choseAlbum].image"
                    :AlbumStatus='true' > </TrackList>
                </div>
                <div id='bg' class='bg' @click="showAlbum=false"></div>
            </div>
    </div>
</template>

<script>
import trackComp from '../track/track'
import TrackList from '../NewProfile/TrackList/TrackList.vue'
export default {
    name: 'Result',
    data() {
        return {
            search: '',
            similar: null,
            similarName: '',
            result: {
                performer: [],
                album: [],
                track: []
            },
            nextPageUrl: {
                performer: '',
                album: '',
                track: ''
            },
            choseAlbum: null,
            showAlbum: false
        }
    },
    components: {
        trackComp,
        TrackList
    },
    created() {
        this.$bus.$on('Search', data => {this.search = data})
        this.$bus.$on('Similar', data => {this.similar = data})
        this.$bus.$on('SimilarName', data => {this.similarName = data})
    },
    mounted() {
        this.search = this.$store.state.search
        this.similar = this.$store.state.similar
        this.similarName = this.$store.state.similarName
    },
    watch: {
        '$route': 'getResult',
        search: 'getResult',
        similar: 'getResult'
    },
    methods: {
        getResult() {
            var url = ''
            if (this.$route.path === '/search')
                url = '../api/search?query=' + this.search.toLowerCase()
            else 
                url = '../api/search?track=' + this.similar
            this.$http.get(url).then(function(response){
                this.result = { 
                    performer: [],
                    album: [],
                    track: []
                }
                this.nextPageUrl = {
                    performer: '',
                    album: '',
                    track: ''
                }
                this.showAlbum = false
                var self = this
                if (response.body.next !== null)
                    this.checkOnNextPage(response.body.next, 'all')
                response.body.results.map(function(item){
                    switch(item.type)
                    {
                        case 'performer':
                            self.result.performer.push(item)
                            break
                        case 'album':
                            self.result.album.push(item)
                            break
                        case 'track':
                            self.result.track.push(item)
                            break
                    }
                });
                if (this.$route.path === '/similar')
                    self.result.track.shift()
                console.log(response.body)
                // this.result = response.body
                // this.tips.reverse()
            });
        },
        gotoPerformer(id) {
            this.$router.push('/performers/' + id)
        },
        checkOnNextPage(url, type) {
            console.log('checkOnNextPage')
            this.$http.get(url.replace('http://localhost:8000/', '../')).then(function(response){
                var self = this
                var obj = {
                    performer: '',
                    album: '',
                    track: ''
                }
                response.body.results.map(function(item){
                    switch(item.type)
                    {
                        case 'performer':
                            obj.performer = url.replace('http://localhost:8000/', '../')
                            break
                        case 'album':
                            obj.album = url.replace('http://localhost:8000/', '../')
                            break
                        case 'track':
                            obj.track = url.replace('http://localhost:8000/', '../')
                            break
                    }
                });
                if(type === 'all')
                    self.nextPageUrl = obj
                else switch(type)
                {
                    case 'performer':
                        self.nextPageUrl.performer = obj.performer
                        break
                    case 'album':
                        self.nextPageUrl.album = obj.album
                        break
                    case 'track':
                        self.nextPageUrl.track = obj.track
                        break
                }
                console.log(response.body)
            });
        },
        updatePage(type, url) {
            this.$http.get(url).then(function(response){
                var self = this
                if (response.body.next !== null)
                    this.checkOnNextPage(response.body.next, type)
                else switch(type)
                {
                    case 'performer':
                        self.nextPageUrl.performer = ''
                        break
                    case 'album':
                        self.nextPageUrl.album = ''
                        break
                    case 'track':
                        self.nextPageUrl.track = ''
                        break
                } 
                response.body.results.map(function(item){
                    if (item.type === type)
                    {
                        switch(type)
                        {
                            case 'performer':
                                self.result.performer.push(item)
                                break
                            case 'album':
                                self.result.album.push(item)
                                break
                            case 'track':
                                self.result.track.push(item)
                                break
                        }
                    }
                });
                console.log(response.body)
            });
        },
    },
    
}
</script>

<style scoped src="./Result.css">
</style>