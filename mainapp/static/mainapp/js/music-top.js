Vue.http.interceptors.push(function(request) {
  request.headers.set('X-CSRFToken', csrftoken);
}); //эта штука перехватывает все запросы на Vue и преобразует их в запрос с csrf token'ом

Vue.component('app-compilation',{
    template:'#compilation',
    data: function() {
        return{
            compilations:[],
          //hoverClass: 'disk'
        }
    },
    methods: {
        showGenre: function(message) {
          data = new FormData();
          data.append('genre ', message);
            this.$http.post('change_genre/', data).then(function(response){
                //console.log(response);
                this.compilations = response.data.genre;
                this.compilations.forEach(function(item, i, arr) {
                    item[1] = "/static/mainapp/album_sources/" + item[1];
                });
                //alert(this.compilations);
            }, function(error){
            })
        },
    },
    created: function() {
        this.showGenre(1)
    }
});

Vue.component('app-music-top', {
    template:'#music-top',
    data: function() {
        return{
          infotracks: []
        }
    },
    methods: {
        showMonth: function() {
            this.$http.post('top_month/').then(function(response){
                //console.log(response);
                this.infotracks = response.data.month;
                this.infotracks.forEach(function(item, i, arr) {
                    item[2] = "/static/mainapp/album_sources/" + item[2];
                });
                //alert(this.infotracks);
            }, function(error){
            })
        },
    },
    created: function() {
        this.showMonth()
    }
});

Vue.component('compositor-top', {
    template:'#compositor-top',
    data: function() {
        return{
          compositors: []
        }
    },
    methods: {
        showBest: function() {
            this.$http.post('best_performer/').then(function(response){
                //console.log(response);
                this.compositors = response.data.performers;
                this.compositors.forEach(function(item, i, arr) {
                    item[1] = "/static/mainapp/performer_sources/" + item[1];
                });
                //alert(this.compositors);
            }, function(error){
            })
        },
    },
    created: function() {
        this.showBest()
    }
});

var vm = new Vue ({
	el: '#main',	data: {
        message: 'сообщение',
        hoverClass:'disk'
    },
    methods: {

    }
});