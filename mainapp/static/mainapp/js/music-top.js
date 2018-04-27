Vue.component('header-container',
{
    template: '#header-container',
    data() {
        return {  
            menuShow:false,
        }
    },
    methods: {
        showMenu() {
            this.$store.commit("showLoader", true)
        },
        openProfile() {
            this.$store.commit("showProfile")
        }
    }
});

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
                this.compilations = JSON.parse(response.bodyText);
                for(var i = 0; i < this.compilations.length; i++)
                {
                    if(this.compilations[i].image_alb === null )
                    {
                     this.compilations[i].image_alb = "/static/mainapp/images/cat.jpg"
                    }
                }
            })
        },
        trackClick: function(index) {
            //this.$emit('trackclicked');
            bus.$emit('trackclicked', {
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
                this.infotracks = response.data;
                /*this.infotracks.forEach(function(item, i, arr) {
                    item[2] = "/media/albums/" + item[2];
                });*/
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
                this.compositors = response.data;
                /*this.compositors.forEach(function(item, i, arr) {
                    item[1] = "/static/mainapp/performer_sources/" + item[1];
                });*/
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