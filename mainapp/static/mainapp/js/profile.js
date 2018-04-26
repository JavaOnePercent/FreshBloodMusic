Vue.component('profileNastr', {
    template:'#nastr',
    data: function() {
        return {
            name: '',
            label: null,
            description: ''
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
            this.$http.post('performer', data).then(function(response){

            });
        },
        cencleClick(){
            this.$emit('cencle-clicked');
        } 
    },
});


Vue.component('profile', {
    template:'#profile',
    data: function() {
        return {
            name: '',
            logo: '/static/mainapp/images/camera.svg',
            description: ''
        }
    },
    created() {
        this.$http.get('performer').then(function(response){
            this.name = response.body.name_per;
            this.logo = response.body.image_per;
            this.description = response.body.about_per;
            this.$store.commit('performerName', this.name);
            this.$store.commit('performerLogo', this.logo);
            this.$store.commit('performerDescription', this.description);
        });
    },
    methods: {
        nastrClick() {
            this.$emit('nastr-clicked');
        }
    },
});
