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
    return '/static/mainapp/album_sources/' + link;
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
        isDragging: false
    },
    mutations: {
        currentTime (state, val) {
            state.currentTime = val;
        },
        duration (state, val){
            state.duration = val;
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
        }
    }
})