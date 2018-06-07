var settings = Vue.component('profileNastr', {
    template:'#nastr',
    data: function() {
        return {
            name: '',
            label: null,
            description: '',
            id: 0
        }
    },
    /*computed: {
        name() {
            return this.$store.state.performerName
        },
        logo() {
            return this.$store.state.performerLogo
        },
        description() {
            return this.$store.state.performerDescription
        }
    },*/
    created() {
        this.name = this.$store.state.performerName;
        this.label = this.$store.state.performerLogo;
        this.description = this.$store.state.performerDescription;
        this.id = this.$store.state.performerID;
    },
    methods: {
        setLabel(e) {
            this.label = e.target.files[0];
        },
        saveSettings() {
            var data = new FormData();
            data.append('name', this.name);
            data.append('label', this.label);
            data.append('description', this.description);
            data.append('id', this.id);
            this.$http.post('performers', data).then(function(response){
                this.$store.commit('performerLogo', '');
                this.$store.commit('performerLogo', this.label);
                this.$emit('cencle-clicked');
            });
        },
        cencleClick(){
            this.$emit('cencle-clicked');
        } 
    },
});


var profile = Vue.component('profile', {
    template:'#profile',
    data() {
        return {
            albums: [],
            likes: []
        }
    },
    watch: {
        // в случае изменения маршрута запрашиваем данные вновь
        '$route': 'receiveData'
      },
    created() {
        this.receiveData();
    },
    computed: {
        name() {
            return this.$store.state.performerName;
        },
        logo() {
            return this.$store.state.performerLogo;
        },
        description() {
            return this.$store.state.performerDescription;
        }
    },
    methods: {
        receiveData() {
            var id = this.$route.params.id;
            this.$http.get('performers/' + id).then(function(response){
                //console.log(response.body)
                for(var i = 0; i < response.body.albums.length; i++)
                {
                    var tracks = [];
                    for(var j = 0; j < response.body.albums[i].tracks.length; j++)
                    {
                        tracks.push({name: response.body.albums[i].tracks[j].name_trc, id: response.body.albums[i].tracks[j].id});
                    }
                    this.$set(this.albums, i, { name: response.body.albums[i].name_alb,
                                                logo: response.body.albums[i].image_alb,
                                                genre: response.body.albums[i].genre + ' / ' + response.body.albums[i].style,
                                                date: response.body.albums[i].date_alb,
                                                tracks: tracks});
                }
                this.$store.commit('performerID', response.body.id);
                this.$store.commit('performerName', response.body.name_per);
                this.$store.commit('performerLogo', response.body.image_per);
                this.$store.commit('performerDescription', response.body.about_per);
            });
            this.$http.get('likes').then(function(response){
                //console.log(response.body)
                for(var i = 0; i < response.body.length; i++)
                {
                    this.$set(this.likes, i, {name: response.body[i].name_trc, performer: response.body[i].name_per, logo:response.body[i].image_alb})
                }
            });
        },
        backgroundImage(url) {
            return 'background-image: url('+ url +')';
        },
        nastrClick() {
            this.$emit('nastr-clicked');
        }
    },
});
