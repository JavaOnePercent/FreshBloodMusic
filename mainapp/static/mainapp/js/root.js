const router = new VueRouter({
    routes: [
        { path: '/performers/:id', name: 'performer', component: profile },
        { path: '/settings', component: settings },
        { path: '/', component: main },
    ],
    linkActiveClass: 'router-link-noob',
    linkExactActiveClass: 'router-link-noob'
});

new Vue({
    el: '#VueContainer',
    data:{
        nastrShow: false
    },
    store,
    router,
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