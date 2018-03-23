Vue.component('app-compilation',{
    template:'#compilation',
    data: function() {
        return{
          compilation: []
          //hoverClass: 'disk'
        }
    },
    methods: {
        showGenre: function() {
            this.$http.get('change_genre/', {headers: {"X-CSRFToken": csrftoken}}).then(function(response){
                console.log(response);
            }, function(error){
            })
        },
    },
    created: function() {
        this.showGenre()
    }
});

Vue.component('app-music-top', {
    template:'#music-top',
    data: function() {
        return{
          infotrack: []
        }
    },
    methods: {
        showMonth: function() {
            this.$http.get('top_month/', {headers: {"X-CSRFToken": csrftoken}}).then(function(response){
                console.log(response);
                this.infotrack = response.data.month;
                this.infotrack[0] = "/static/mainapp/album_sources/" + this.infotrack[0];
                this.infotrack.push(response.data.track[0]);
                this.infotrack.push(response.data.track[1]);
                //alert(this.infotrack);
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
            this.$http.get('best_performer/', {headers: {"X-CSRFToken": csrftoken}}).then(function(response){
                console.log(response);
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
})

var vm = new Vue ({
	el: '#main',
	data: {
        message: 'сообщение',
        hoverClass:'disk'
    },
    methods: {

    }
});