Vue.component('app-music-top',{
    template:'#music-top'
});

Vue.component('app-compilation',{
    template:'#compilation',
    data: function () {
        return {
            hoverClass:'disk'
          }
      }
});

var vm = new Vue ({
	el: '#main',
	data: {
        massege: 'Ты Хуй',
        hoverClass:'disk'
    },
    methods: {

    }
});