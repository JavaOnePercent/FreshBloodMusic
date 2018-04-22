Vue.component('profileNastr', {
    template:'#nastr',
    data: function() {
        return{
        }
    },
    methods: { 
    },
});


Vue.component('profile', {
    template:'#profile',
    data: function() {
        return{
        }
    },
    methods: {
        nastrClick() {
            this.$emit('nastr-clicked');
        }
    },
});


new Vue ({
    el: '#VueContainer',
    data:
    {
        nastrShow: false
    },
    methods: {
        show(){
            this.nastrShow = !this.nastrShow;
        }

    }

})
