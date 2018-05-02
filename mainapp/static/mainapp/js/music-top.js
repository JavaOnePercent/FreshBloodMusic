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
            compilation:[],
            compilations:[],
            url: 'track',
            loading: false
          //hoverClass: 'disk'
        }
    },
    mounted(){
        document.addEventListener("scroll", this.onScroll, false);
    },
    methods: {
        onScroll: function(event) {

            var wrapper = event.target.body;
            var list = this.$refs.list;
            var topics = document.getElementById('topics').offsetHeight;
            var header = document.getElementById('header-container').offsetHeight;
            var recommendations = document.getElementById('recommendations').offsetHeight;
            var scrollTop = wrapper.scrollTop;
            var wrapperHeight = wrapper.offsetHeight;
            var listHeight = list.offsetHeight + topics + header + recommendations;

            var diffHeight = listHeight - wrapperHeight;

            //console.log(wrapper);
            //console.log(diffHeight, scrollTop);
            if(diffHeight <= scrollTop && !this.loading) {
                this.showGenre(2);
            }

        },
        showGenre: function(message) {
          this.loading = true;
          this.$http.get(this.url, {params: {genre: message}}).then(function(response){
                this.compilation = response.body.results;
                for(var i = 0; i < this.compilation.length; i++)
                {
                    if(this.compilation[i].image_alb === null )
                    {
                     this.compilation[i].image_alb = "/static/mainapp/images/cat.jpg"
                    }
                }
                this.compilations = this.compilations.concat(this.compilation);
                console.log(this.compilations);
                this.url = response.body.next;
                console.log(this.url);
                this.loading = false;
            }, function(error){
                this.loading = false;
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

var main = Vue.component('main-compilation', {
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