<template>
    <div class="app" id="app">
        <header-container></header-container>
        <div v-if="showLoader" class="modal" id="myModal" >
            <div class="modal-content">
                <loader></loader>
            </div>
        </div>
        <!-- <user-playlists> </user-playlists> -->
        <div style="position: relative; top: calc(50% - 55px);" class="loading" v-if="loading">
        <div class="Loaderplay"><span class="cssload-main"><span class="cssload-main-inner"></span></span></div>
        <h2> Подождите, нам надо подготовиться. </h2>
        </div>
        <router-view v-if="!loading" @login="loadFromHistory" ></router-view>
        <top-player></top-player>
    </div>
</template>

<script>
import headerContainer from './components/Header.vue'
import profile from './components/Profile.vue'
import settings from './components/Settings.vue'
import mainCompilation from './components/Main.vue'
import loader from './components/Loader.vue'
import topPlayer from './components/TopPlayer.vue'

import NewProfile from './components/NewProfile/NewProfile.vue'
// import userPlaylists from './components/userPlaylists/userPlaylists.vue'

export default {
    name: 'app',
      data() {
        return {
            loading: true,
        }
    },
    components: {
        headerContainer,
        profile,
        settings,
        mainCompilation,
        loader,
        topPlayer,
        NewProfile,
        // userPlaylists
    },
    created() {
        this.loading = true,
        console.log(this.$store.state)
        var self = this
        this.$http.get('../api/login').then(function(response){
            self.$store.commit("username", response.data.username)
            self.$store.commit('myPerformerID', response.data.per_id)
        });
        this.$http.get('../api/token').then(function(response){
        });
        this.loadFromHistory()
    },
    computed: {
        showLoader () {
            return this.$store.state.showLoader
        }
    },
    methods: {
        loadFromHistory() {
            var self = this
            this.$http.get('../api/history').then(response => {
            //console.log(response.data)
            if(response.data[0])
            {
                //self.$store.commit('currentTrack', response.data[0].id)
                for(var i = 1; i < response.data.length; i++)
                {
                    self.$store.commit('truePushHistoryTrack', response.data[i])
                }
                this.$bus.$emit('set-current-track', response.data[0].id)
            }
            else
                this.$bus.$emit('set-current-track', null)
            this.loading = false
        }, error => {this.$bus.$emit('set-current-track', null)});
        }
    }
}
</script>

<style >
html, body
{
    /*font-family:"Rex Bold";*/
    display: inline-block;
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    font-family: Arial,Helvetica,sans-serif;
    position: fixed;
    overflow-y: scroll;
    overflow-x: hidden;
}
html {
    overflow: hidden;
}
.app
{
    height: 100%;
}
.modal
 {
    pointer-events: all;
    position: fixed;
    z-index: 900;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.8);
    overflow: -moz-scrollbars-none; 
    -ms-overflow-style: none; 
 }
 .modal-content
 {
    margin: 0 auto 100px auto;
 }
.modal::-webkit-scrollbar {
    display: none;
}
/* стили скроллбара */
.ps__thumb-y {
    background-color: rgb(255, 181, 43) !important; 
    border-radius: 6px;
    position: absolute;
}
.ps__rail-y {  
    background-color: rgba(255, 181, 43, 0) !important;
}
/* стили скроллбара */
.loading
{
    width: 100%;
}
.loading h2
{
    margin: 0 auto;
    text-align: center;
    display: block;
    cursor: default;
}

.cssload-main {
    top: 25px;
	display: block;
    margin:0 auto;
    margin-bottom: 30px;
	width: 25px;
	height: 25px;
	position: relative;
	border: 5px solid rgb(0,0,0);
	animation: cssload-main 2.3s infinite ease;
    -o-animation: cssload-main 2.3s infinite ease;
    -ms-animation: cssload-main 2.3s infinite ease;
    -webkit-animation: cssload-main 2.3s infinite ease;
    -moz-animation: cssload-main 2.3s infinite ease;
}

.cssload-main-inner {
	vertical-align: top;
	display: inline-block;
	width: 100%;
	background-color: rgb(70, 70, 70);
	animation: cssload-main-inner 2.3s infinite ease-in;
		-o-animation: cssload-main-inner 2.3s infinite ease-in;
		-ms-animation: cssload-main-inner 2.3s infinite ease-in;
		-webkit-animation: cssload-main-inner 2.3s infinite ease-in;
		-moz-animation: cssload-main-inner 2.3s infinite ease-in;
}

@keyframes cssload-main {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-o-keyframes cssload-main {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-ms-keyframes cssload-main {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-webkit-keyframes cssload-main {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-moz-keyframes cssload-main {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@keyframes cssload-main-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-o-keyframes cssload-main-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-ms-keyframes cssload-main-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-webkit-keyframes cssload-main-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-moz-keyframes cssload-main-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}
</style>
