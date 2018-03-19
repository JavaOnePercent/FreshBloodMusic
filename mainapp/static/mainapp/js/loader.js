//import loader from 'views
/*export default {
    data() {
      return {
        track_name_loader: '',
        track: '',
        photo: ''
      }
    },
    methods: {
      send () {
        console.log('track_name_loader, track, photo=', track_name_loader, track, photo)
        var track_name_loader, track, photo = this
        if (track_name_loader && track) {
          errorMessage = ''
         // loader.send({  track_name_loader, track, photo })
        } else {
          errorMessage = 'Ты в пиве'
        }
      }
    }
}*/


//var VueResource = require('vue-resource')

//Vue.use(VueResource)


//import loader from 'views
new Vue({
    el: '#loader-conteiner',
    data () {
      return {
      track_name_loader: '',
      photo: '',
      track: '',
      errorMessage : ''}
    },
    methods: {
      sync_photo (e) {
        e.preventDefault();
        this.photo = e.target.files[0];
        },
      sync_track (e) {
        e.preventDefault();
        this.track = e.target.files[0];
        },
      send () 
        {
          var track_name_loader=this.track_name_loader
          var track=this.track
          var photo=this.photo
          data = new FormData()
          data.append('photo ', this.photo)
          data.append('track ', this.track)
          data.append('name ', this.track_name_loader)

            console.log('track_name_loader, track, photo=', track_name_loader, track, photo)
            if (track_name_loader && track) {
              this.errorMessage = ''
              var csrftoken = this.getCookie('csrftoken');
              var config = {
                headers: {"X-CSRFToken": csrftoken}, 
                //responseType: 'json'
              }
              this.$http.post('/add_album/', data, config).then(
                response => {
                  console.log('Success! Response: ', response.body);
                }
              )}
            else {
              this.errorMessage = 'Ты в пиве'
              console.log('errorMessage=', this.errorMessage)
            }
          },
          
    getCookie: function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
  }
});