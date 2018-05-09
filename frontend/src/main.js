import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import Vuex from 'vuex'

import profile from './components/Profile.vue'
import settings from './components/Settings.vue'
import main from './components/Main.vue'

Vue.use(VueRouter)

//var VueResource = require('vue-resource');

Vue.use(VueResource);

Vue.use(Vuex)

Vue.config.productionTip = false

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken')

Object.defineProperty(Vue.prototype,"$bus",{
	get: function() {
		return this.$root.bus;
	}
});

Vue.http.interceptors.push(function(request) {
    request.headers.set('X-CSRFToken', csrftoken);
}); //эта штука перехватывает все запросы на Vue и преобразует их в запрос с csrf token'ом

const store = new Vuex.Store({ //глобальное хранилище vuex
  state: {
      currentTime: 0,
      duration: 0,
      playing: false,
      volume: 100,
      isDragging: false,
      showLoader: false,
      showProfile: false,
      performerName: '',
      performerLogo: '',
      performerDescription: '',
      performerID: 0
  },
  mutations: {
      currentTime (state, val) {
          state.currentTime = val;
      },
      duration (state, val){
          state.duration = val;
      },
      showLoader(state, val) 
      {
          state.showLoader = val
      },
      showProfile(state) 
      {
          state.showProfile = !state.showProfile;
      },
      switchPlaying (state) {
          state.playing = !state.playing;
      },
      playing(state, val){
          state.playing = val;
      },
      volume (state, val){
          state.volume = val;
      },
      isDragging(state, val){
          state.isDragging = val;
      },
      performerName(state, val) {
          state.performerName = val;
      },
      performerLogo(state, val) {
          state.performerLogo = val;
      },
      performerDescription(state, val) {
          state.performerDescription = val;
      },
      performerID(state, val) {
          state.performerID = val;
      },
  }
})

const router = new VueRouter({
  routes: [
      { path: '/performers/:id', name: 'performer', component: profile },
      { path: '/settings', component: settings },
      { path: '/', component: main },
  ],
  linkActiveClass: 'router-link-noob',
  linkExactActiveClass: 'router-link-noob'
});

new Vue({
    data: {
        bus: new Vue({})
    },
    store,
    router,
    render: h => h(App)
}).$mount('#app')
