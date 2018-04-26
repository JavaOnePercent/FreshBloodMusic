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

function toStatic(link)
{
    return '/media/albums/' + link;
}

var bus = new Vue();

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
        performerDescription: ''
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
        showProfile(state, val) 
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
    }
})