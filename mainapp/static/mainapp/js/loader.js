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
Vue.directive('focus', {        //дерректива для фокуса вызов v-focus
  inserted: function (el) {
      el.focus()
  }
})
Vue.component('loader',{
    template: '#loader',
    store,
    data () {
      return {
      track_name_loader: '',
      photo: '',
      track : [],
      errorMessage : '',
      src:'',
      imgStyle:'camera',
      loaderStyle: 'track-upload',
      currentEdit: null,
      trackName: '',
      janr:'жанр',
      show: false,
      menuIndex:null,
      pointerEvents: "pointerEvents",
      dragging: 0,
      dropbox:null,
      dropAll: null,
      menuItems: [
      	{
        	name: 'Item 1',
          children: [{name: 'Subitem 1'},{name: 'Subitem 2'},{name: 'Subitem 3'}]
        },
        {
        	name: 'Item 2'
        },
        {
        	name: 'Item 2'
        },
        {
        	name: 'Item 2'
        },
        {
        	name: 'Item 2'
        },
        {
        	name: 'Item 2'
        },
      ],
      }
    },
    //если шо то сносить к чертям
    mounted(){
      this.dropbox = document.getElementById("dropbox");
      this.dropAll = document.getElementById("body");   //для того чтобы засечь что элемент на форме
      this.dropAll.addEventListener("dragover", this.dragoverAll, false);
      this.dropAll.addEventListener("dragleave", this.dragleaveAll, false);
      this.dropAll.addEventListener("dragenter", this.dragenterAll, false);
      this.dropbox.addEventListener("dragenter", this.dragenter, false);
      this.dropbox.addEventListener("dragover", this.dragover, false);
      this.dropbox.addEventListener("dragleave", this.dragleave, false);
      this.dropbox.addEventListener("drop", this.drop, false);

      $(document).on('dragover drop', function (e){
        e.stopPropagation();
        e.preventDefault();
        dropAll.style.pointerEvents="all"
        vm.loaderStyle = 'track-upload'
      });
     /*$(document).on('dragover', function (e){
        //e.stopPropagation();
        e.preventDefault();
        //e.dataTransfer.effectAllowed = "none"
        e.originalEvent.dataTransfer.dropEffect = 'none' //иконка
        //vm.loaderStyle = 'track-upload-drop'
        //if(vm.loaderStyle != 'track-upload')
        //{
         // dropAll.style.pointerEvents="none"
        //}
      });
      $(document).on('dragleave', function (e){
        //e.stopPropagation();
        e.preventDefault();
        //dropAll.style.pointerEvents="none"
        e.originalEvent.dataTransfer.dropEffect = 'none'
          vm.loaderStyle = 'track-upload'
          //dropAll.style.pointerEvents="all"
        //if(vm.loaderStyle == 'track-upload')
        //{
          //vm.loaderStyle = 'track-upload-drop'
          //dropAll.style.pointerEvents="all"
        //}
      });*/
     
    },

    //сносить досюда
    methods: {
      dragenter(e){
        e.stopPropagation();
        e.preventDefault();
        this.loaderStyle ='track-upload-drop2'
        e.dataTransfer.dropEffect = 'copy'
        //console.log(vm.loaderStyle)
        //document.getElementById('dropbox').classList.add("track-upload-drop")
        //document.getElementById('dropbox').classList.remove("track-upload")   //фу-фу-фу
      },
        dragover(e)
        {
          e.stopPropagation();
          e.preventDefault();
          //dropAll.style.pointerEvents="all"
          e.dataTransfer.dropEffect = 'copy'
          this.loaderStyle ='track-upload-drop2'
        },
        dragleaveAll(e){
          e.stopPropagation();
          e.preventDefault();
          this.dragging--;
          //e.dataTransfer.dropEffect = 'copy'
        if (this.dragging === 0 & this.loaderStyle != 'track-upload-drop2') 
          {
            this.loaderStyle = 'track-upload'
          this.dropAll.style.pointerEvents="all"
          }
        },
        dragoverAll(e){
          e.stopPropagation();
          e.preventDefault();
          e.dataTransfer.dropEffect = 'none' 
          //dropAll.style.pointerEvents="none"
          //e.dataTransfer.dropEffect = 'none'
          //vm.loaderStyle ='track-upload-drop'
        },
         dragenterAll(e){
          e.stopPropagation();
          e.preventDefault();
          this.dragging++;
          this.dropAll.style.pointerEvents="none"
          e.dataTransfer.dropEffect = 'none'
          this.loaderStyle ='track-upload-drop'
          //document.getElementById('dropbox').classList.add("track-upload-drop")
          //document.getElementById('dropbox').classList.remove("track-upload")
        },
      dragleave(e){
        e.stopPropagation();
        e.preventDefault();
        //e.dataTransfer.dropEffect = 'none'
        if( this.loaderStyle === 'track-upload-drop2'){
          this.loaderStyle='track-upload'   //чтобы убрать мелкое подлагивание поставить "track-upload-drop"
        this.dropAll.style.pointerEvents="all"
        }
        //document.getElementById('dropbox').classList.add("track-upload")
        //document.getElementById('dropbox').classList.remove("track-upload-drop")
      },
      drop(e) {
        e.stopPropagation();
        e.preventDefault();
        //document.getElementById('dropbox').classList.add("track-upload")
        //document.getElementById('dropbox').classList.remove("track-upload-drop")
        this.dropAll.style.pointerEvents="all"
        this.loaderStyle='track-upload'
        var dt = e.dataTransfer;
        var files = dt.files;
        document.getElementById("add").files =  files; 
      },
      close(){
        this.$store.commit("showModel",false)
      },
      sync_photo: function (e) {
        e.preventDefault();
        var preview = document.querySelector('img[alt="обложка"]');  //я знаю это колхоз, но я чот сломался
        var file    = document.querySelector('input[name="photo"]').files[0];
        var reader  = new FileReader();
    
        this.errorMessage = ''
        this.photo = e.target.files[0];
        reader.onloadend = function () {
        preview.src = reader.result;
        }
  
        if (file) {
          if(e.target.files[0].name.split('.').pop() =="jpg" ) //проверяем формат файла (переписать)
          {   
          reader.readAsDataURL(file);
          this.imgStyle='Loaderimg';
        } else {
          preview.src = "/static/mainapp/images/camera.png";
          this.imgStyle='camera';
        }
        }
        else 
        {
          preview.src = "/static/mainapp/images/camera.png";
          this.imgStyle='camera';
          this.errorMessage = 'формат картинки только jpg'  //хотя скорее всего эта ошибка не нужна
        }
        //let reader = new FileReader();
        //this.src = reader.readAsDataURL(e.target.files[0]);
        //console.log(e.target.result)
        },
      sync_track: function(e)  {
        e.preventDefault();
        for(var i=0;i<e.target.files.length;i++) //пробегаем по файлам
        {
          if(this.track.length < 20 )  //проверяем количество файлов в массиве 
          {
            if(e.target.files[i].name.split('.').pop() =="mp3" ) //проверяем формат файла
            {
              this.errorMessage = ''
              console.log(e.target.files[i].type)
              file= {"name":e.target.files[i].name.replace(/\.[^.]+$/, "") ,"file": e.target.files[i]};
              //e.target.reset();
              //e.target.files[i] = null;
              console.log(e.target.files[i].name)
              this.track.push(file);
              console.log(this.track.length)
            } else 
            {
              this.errorMessage = 'формат музыки только mp3'  //хотя скорее всего эта ошибка не нужна
            }
          } else
          {
            this.errorMessage = "был превышен лимит";
            break
          }
        }
      this.$refs.add.value  =  ""; 
      },
      track_Name: function(e){
        e.preventDefault();
        if(this.track[this.currentEdit].name.length<1)
        {
          console.log(this.trackName);
          this.errorMessage = "название трека не может быть пустым";
          this.track[this.currentEdit].name = this.trackName;
        }
        console.log(this.track[this.currentEdit].name.length)
      },
        
      send:function () 
        {
          var track_name_loader=this.track_name_loader
          var track=this.track
          var photo=this.photo
          data = new FormData()
          data.append('photo ', this.photo)
          data.append('track ', this.track)
          data.append('name ', this.track_name_loader)

          console.log('track_name_loader, track, photo=', track_name_loader, track, photo);
          if (track_name_loader && track) {
            this.errorMessage = '';
            this.$http.post('/add_album/', data, {headers: {'X-CSRFToken': csrftoken}}).then(function(response){ //csrf token уже подключён перехватчиком, который находится в music-top
              console.log('Success! Response: ', response.body);
          }, function(error){
          })
          }
          else {
            this.errorMessage = 'Ты в пиве';
            console.log('errorMessage=', this.errorMessage)
          }
        },
          imit:function(){
            this.$refs.fileInput.click()
          },
          deleteTrack:function(id){
            this.track.splice(id, 1);
          },
          upgradeName:function(index)
          {
            this.currentEdit=index
            this.trackName = this.track[this.currentEdit].name
          },
          setSelectedItem:function(item) {
            this.selectedDropdown = item;
          },
          menuIndexfunc:function(id)
          {
            if(this.menuIndex == null)
            {
              this.menuIndex=id
            }
            else
            this.menuIndex=null
          },
          chooseJanr:function(name)
          {
            this.show = !this.show
            this.janr = name;
          }
  }
});