new Vue({
    el: '#VueContainer',
    data:{
        nastrShow: false
    },
    store,
        //bus: bus // Here we bind our event bus to our $root Vue model.
    computed: {
        showLoader () {
            return this.$store.state.showLoader
        },
        showProfile () {
            return this.$store.state.showProfile
        }
    },
    methods:
    {
        showNastr(){
            this.nastrShow = !this.nastrShow;
        }
    }
});