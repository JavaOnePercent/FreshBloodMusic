Object.defineProperty(Vue.prototype, '$bus', {
	get() {
		return this.$root.bus;
	}
});

var bus = new Vue({});

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
          this.$http.get('track',{params: {genre: message}}).then(function(response){
              //console.log(JSON.parse(response.bodyText));
              this.compilations = JSON.parse(response.bodyText);
              this.compilations.forEach(function(item) {
                  item.image_alb = "/static/mainapp/album_sources/" + item.image_alb;
              });
              //console.log(this.compilations);
                //alert(this.compilations);
          }, function(error){
            })
        },
        trackClick: function(index) {
            //this.$emit('trackclicked');
            this.$bus.$emit('trackclicked', {
				id: this.compilations[index].id
			});
        }
    },
    created: function() {
        this.showGenre('all')
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
            this.$http.get('top_month/').then(function(response){
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
            this.$http.get('best_performer/').then(function(response){
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

Vue.component('main-compilation', {
	template: '#main',
    data() {
	    return {
            message: 'сообщение',
            hoverClass: 'disk'
        }
    },
    methods: {

    }
});