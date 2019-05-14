<template>
    <div id="loader-conteiner" class="loader-conteiner">
        <header class="Loaderheader">
            <span>Загрузка музыкального издания</span>
            <img class="esc" src="/static/mainapp/images/whiteClose.png" @click="close">
        </header>
        <form method="POST">
            <div class="track-img-loader-conteiner" >
                <label>Обложка</label>
                <img :class="imgStyle"  @click="imit" src="/static/mainapp/images/camera.svg" alt="обложка">
            </div>
            <div class="track-name-loader-conteiner">
                <label for="track-name-loader">Название*</label>
                <input class="track-name-loader" type="text" name="track-name-loader" placeholder="" v-model='track_name_loader' maxlength="22">
            </div>
    
            <div class="track-janr-loader-conteiner">
                <label for="track-janr-loader">Жанр*</label>
                <div class="Loaderjanr" @click="genresButtonClick">{{ janr }}</div>
                <ul class="janr-drop" v-if="show">
                    <li v-for="(item,index) in menuItems" :key="index" @click='genreClick(index)'>{{ item.name }}
                        <ul class="janr-drop-menu" v-if="menuIndex===index">
                            <li :key="index" v-for="(child,index) in item.children" @click="chooseJanr(child.name, child.id)"> {{ child.name }}
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
    
            <!-- <div class="description-conteiner">
                <label for="track-name-loader">Описание</label>
                <textarea type="text" name="description" maxlength="800" v-model="description"> </textarea>
            </div> -->
    
    
            <input style="display: none" id="photo" ref="fileInput" class="add" @change="sync_photo" type="file" name="photo" accept="image/*,image/jpeg" > <!--если шо тот ref -->
            <div class="loader-tracks" :key="index" v-for="(tracks, index) in track" >
                <img v-if="tracks.loading===false" class="Loaderplay" src="/static/mainapp/images/playButton.svg" alt="play" @click="playNow(tracks)">
                <input v-focus v-on:keyup.enter="currentEdit=null" v-if="currentEdit===index" id="input" class="track" type="text" v-model='tracks.name' @change="track_Name" @blur="currentEdit=null" maxlength="30" > <!-- а тут менять длину по базе-->
                <div v-else class="track" style="cursor: pointer"  @click="upgradeName(index)" >{{tracks.name}}</div>
                <div class="Loaderplay" v-show="tracks.loading"><span class="cssload-loader"><span class="cssload-loader-inner"></span></span></div>
                <img v-if="currentEdit===index" class="edit" src="/static/mainapp/images/forward.png" @mousedown="currentEdit=null">
                <img v-else class="edit" src="/static/mainapp/images/edit.png" @mousedown="upgradeName(index)">
                <img class="del" src="/static/mainapp/images/xiomi.png" @click="deleteTrack(index)">
                <hr class="HRloader">
            </div>
      
            <div style="pointer-events: all" id = "dropbox" class="add" :class="loaderStyle">
                <label>
                    <input style="display:none" id='add' ref="add" @change="sync_track" type="file" name="track" multiple accept="audio/mpeg" >
                    Добавить композиции
                </label>
            </div>
            <div style='font-size: 20px;' id="error" class="error"><label  >{{errorMessage}} </label></div>
            <!--<div class="loading" v-if="loader"><span class="cssload-loader"><span class="cssload-loader-inner"></span></span></div>-->
            <button v-if='this.track.length > 0 & track_name_loader != "" & janr != "Выбрать жанр" & !loader'  class="loader" name="loader" @click.prevent='send()'>Загрузить </button>
            <span class="description-conteiner" style="font-size: 16px;"> Обратите внимание, что длина названия одного трека не должна превышать 50 символов </span>

        </form>
    </div>
</template>

<script>
// directive('focus', {        //дерректива для фокуса вызов v-focus
//   inserted: function (el) {
//       el.focus()
//   }
// })
export default {
    name: 'loader',
    directives: {
    focus: {
        // определение директивы
        inserted: function (el) {
        el.focus()
        }
    }
    },
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
            janr:'Выбрать жанр',
            genreID: '',
            show: false,
            menuIndex:null,
            pointerEvents: "pointerEvents",
            dragging: 0,
            dropbox:null,
            dropAll: null,
            menuItems: [],
            loader:false,
            description: ''
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

        /*$(document).on('dragover drop', function (e){
            e.stopPropagation();
            e.preventDefault();
            dropAll.style.pointerEvents="all"
            vm.loaderStyle = 'track-upload'
        });*/
    },
    beforeDestroy () {
        this.dropAll.removeEventListener("dragover", this.dragoverAll, false);
        this.dropAll.removeEventListener("dragleave", this.dragleaveAll, false);
        this.dropAll.removeEventListener("dragenter", this.dragenterAll, false);
        this.dropbox.removeEventListener("dragenter", this.dragenter, false);
        this.dropbox.removeEventListener("dragover", this.dragover, false);
        this.dropbox.removeEventListener("dragleave", this.dragleave, false);
        this.dropbox.removeEventListener("drop", this.drop, false);
    },
    //сносить досюда
    methods: {
        playNow(tr) {
            if(tr.trc_id)
                this.$bus.$emit('play-track', {
                    id: tr.trc_id
                });
        },
        genresButtonClick() {
            this.show=!this.show;
            if(this.menuItems.length === 0)
            {
                this.$http.get('/api/genre').then(response => {response.body.forEach(this.genresIterator)})
            }
        },
        
        genresIterator(item, i, arr) {
            this.$set(this.menuItems, i, {name: item.name_gnr, id: item.id, children: []});
        },
        
        genreClick(index) {
            this.menuIndexfunc(index);
            if(this.menuItems[index].children.length === 0)
                this.$http.get('/api/genre', {params: {id: this.menuItems[index].id}}).then(response => {response.body.forEach(this.stylesIterator)});
        },
      
        stylesIterator(item, i, arr) { 
            this.$set(this.menuItems[this.menuIndex].children, i, {name: item.name_stl, id: item.id});
        },
        
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
            this.dragoverdrop(e)
        },

        dragoverdrop (e){
            e.stopPropagation();
            e.preventDefault();
            dropAll.style.pointerEvents="all"
            vm.loaderStyle = 'track-upload'
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
            this.dragoverdrop(e)
        },

        close(){
            this.$store.commit("showLoader",false)
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
            if(e.target.files[0].type =="image/jpeg" || e.target.files[0].type =="image/png" ) //проверяем формат файла (переписать)
            {   
                reader.readAsDataURL(file);
                this.imgStyle='Loaderimg';
            } 
            else 
            {
                preview.src = "/static/mainapp/images/camera.svg";
                this.imgStyle='camera';
                this.errorMessage = 'формат картинки только jpg'  //хотя скорее всего эта ошибка не нужна
            }
            }
            else 
            {
            preview.src = "/static/mainapp/images/camera.svg";
            this.imgStyle='camera';
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
                        //console.log(e.target.files[i].type)

                        var file= {"name":e.target.files[i].name.replace(/\.[^.]+$/, "").substr(0, 50),"file": e.target.files[i]};
                        //e.target.reset();
                        //e.target.files[i] = null;
                        //console.log(e.target.files[i].name)
                        //file=e.target.files[i];
                        this.track.push(file);
                        //console.log(this.track.length)
                    } 
                    else 
                    {
                        this.errorMessage = 'формат музыки только mp3'  //хотя скорее всего эта ошибка не нужна
                    }
                } 
                else
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
            //console.log(this.trackName);
                this.errorMessage = "название трека не может быть пустым";
                this.track[this.currentEdit].name = this.trackName;
            }
            //console.log(this.track[this.currentEdit].name.length)
        },
        
        send:function () 
        {
            var track_name_loader=this.track_name_loader
            var track=this.track
            var photo=this.photo
            var data = new FormData()
            data.append('photo', this.photo)
            /*for(var track of this.track)
            {
                data.append('track', track.file)
                data.append('track_name', track.name)
            }*/
            data.append('name', this.track_name_loader)
            data.append('gen_id', this.genreID)
            data.append('description', this.description)

            //console.log('track_name_loader, track, photo=', track_name_loader, track, photo);
            if (track_name_loader && track) {
                this.errorMessage = '';
                this.loader=true;

                var self = this
                this.$http.post('api/albums', data, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(response => {
                    this.loader = false
                    //console.log('Альбом создан: ', response.body)
                    for(var tr of track)
                    {
                        var data = new FormData()
                        data.append('track', tr.file)
                        data.append('track_name', tr.name)
                        data.append('album', response.body.alb_id)
                        data.append('index', track.indexOf(tr))
                        self.$set(self.track[self.track.indexOf(tr)], 'loading', true)
                        this.$http.post('api/tracks', data, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(response => { 
                            //console.log(response.body.index) 
                            self.track[response.body.index].loading = false 
                            self.$set(self.track[response.body.index], 'trc_id', response.body.id)
                        })
                    }
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
            if(this.menuIndex === null || id != this.menuIndex)
              this.menuIndex = id;
            else
              this.menuIndex = null;
        },

        chooseJanr:function(name, id)
        {
            this.show = !this.show
            this.janr = name;
            this.genreID = id;
        }
    }
}
</script>

<style scoped>

.pointerEvents
{
	pointer-events: none
}
*:focus {outline: none;}

input
{
	font-size: 90%;
	padding-left:5px; 
	height: 30px;
	width: 500px;
	border-style: solid;
	border-color:rgb(153, 153, 153);
	background-color: rgba(179, 179, 179,0.3);
}
textarea
{
	z-index: 80;
	font-family: Arial,Helvetica,sans-serif;
	background-color: rgba(179, 179, 179,0.3);
	border-style: solid;
	border-width:2px; 
	border-color:rgb(153, 153, 153);
	font-size: 100%;
	resize: vertical;
	height: 30px;
	width: 755px;
	max-height: 250px;
	min-height: 30px;
}

.loader-conteiner
{
	font-size: 160%;
	display:block;
	position: relative;
	background-color: rgba(255, 255, 255, 0.8);
	height: auto;
	max-width: 800px;
	padding-bottom: 185px;
	margin: 100px auto ;
	margin-bottom: 0;
}

/*шапка*/
.Loaderheader
{
	line-height: 40px;
	padding: 8.5px 13.5px;
	position: relative;
	height: 40px;
	font-size: 25px;
	color: rgb(250, 250, 250);
	/* background-color: rgb(70, 70, 70); */
    background-color: rgb(141, 111, 185);
	margin-bottom: 17px;
}
.esc
{
	cursor: pointer;
	display: block;
	padding-top: 7.5px; 
	float: right;
	width: 25px;
	height: 25px;
}

/*обложка*/
.track-img-loader-conteiner
{
	margin: 0 20px 20px 20px;
	display: flex;
	flex-direction: column;
	position: absolute;
}
.camera
{
	padding: 0;
	object-fit: scale-down;
	display: block;
    border-style: solid;
    border-color:black;
    width: 220px;
    height: 220px;
}
.Loaderimg
{
	cursor: pointer;
	padding: 0;
	object-fit: cover;
	display: block;
    border-style: solid;
    border-color:black;
    width: 220px;
    height: 220px;
}
.camera:hover, .Loaderimg:hover
{
	cursor: pointer;
	filter: opacity(50%);
}
/*жанр*/
.Loaderjanr
{
	cursor: pointer;
	text-align:center;
	height: 30px;
	width: 200px;
	padding: 0 25px;
	border-color:rgb(153, 153, 153);
	background-color: rgba(179, 179, 179,0.3);
	border-style: solid;
	border-width:2px; 
}
.Loaderjanr:active
{
	background-color: rgba(179, 179, 179,0.8);
}
.track-janr-loader-conteiner li
{
	list-style-type: none;
}
.janr-drop
{
	height: 90px;
	z-index: 90;
	width: 224px;
	position: absolute;
	top: 62.5px;
	padding: 0;
	margin: 0;
}
.janr-drop li
{
	background-color: rgb(179, 179, 179);
	border-color:rgb(153, 153, 153);
	border-style: solid;
	border-width:2px; 
	transition: .4s;
	cursor: pointer;
	border-top:none;
	text-align: center;
	width: 250px;
	height: 30px;
}
.janr-drop li:hover{
background-color: rgb(129, 129, 129);
}

.janr-drop-menu
{
	overflow-y: auto;
 	overflow-x: hidden !important;
	min-height: 30px;
	max-height: 94px;
	top: -1.3px;
	position: absolute;
	left: 254px;
	padding: 0;
	margin: 0;
	border-bottom: 2px solid rgb(153, 153, 153);
	border-top: 2px solid rgb(153, 153, 153);
}
.janr-drop-menu li
{
	border-left: none;
	border-bottom: 2px solid rgb(153, 153, 153);
	border-top: none;
	cursor: pointer;
	text-align: center;
	width: 250px;
	height: 30px;
}
.janr-drop-menu li:last-child
{
	border-bottom: none;
}

.track-name-loader-conteiner, .track-janr-loader-conteiner, .add, .loader
{
	width: 520px;
	margin: 0 22px;
	padding-bottom:45px; 
	display: flex;
	flex-direction: column;
	position: relative;
}
.description-conteiner, .add, .loader, .loader-tracks
{
	margin: 0 22px;
	position: relative;
	top: 165px;

}
.track-name-loader-conteiner, .track-janr-loader-conteiner
{
	left: 250px;
}
.track-janr-loader-conteiner
{
	position: absolute
}
.loader-tracks
{
	display: block;
	line-height: 40px;
	width: 760px;
	height: 40px;
	position: relative;
	margin: 0px 20px 20px;
}
.Loaderplay
{
    cursor: pointer;
	position: absolute;
	display: block;
	width: 40px;
	height: 40px;
}
.track
{
	display: block;
	left: 65px;
	position: absolute;
	height: 35px;
	width: 625px;
    font-size: 17px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    white-space: nowrap;
}
.edit
{
	cursor: pointer;
	overflow: visible;
	left: 669px;
	top:7.5px;
	position: absolute;
	display: block;
	width: 25px;
	height: 25px;
}

.del
{
	cursor: pointer;
	left: 720px;
	position: absolute;
	float: right;
	display: block;
	width: 40px;
	height: 40px;
}
.HRloader
{
	position: relative;
	top:47px;
	overflow: visible;
	border: 0;
	height: 1px;
	background-color: #000;
	background-image: -webkit-linear-gradient(left, rgba(255, 255, 255, 0.8), #000, rgba(255, 255, 255, 0.8));
}
.error
{
	z-index: 80;
	display: block;
	margin-bottom: -25px;
	overflow: hidden;
	padding: 0;
	width: 450px;
	height: 30px;
	left:370px;
	bottom: -130px; 
	position: relative;
	color: red;
}
.loader
{
	color: #fff;
	font-size: 100%;
	margin-top: 15px; 
	cursor: pointer;
	/* background-color: rgba(0, 153, 38,0.5); */
    background-color: rgb(255, 181, 43);
	border: none;
	width: 50%;
	height: 40px;
	padding-left: 140px;
	position: relative;
	line-height: 40px;
	text-align: center;
}
.loader:hover{
	/* background-color:  rgba(0, 230, 57,0.5) */
    background-color: rgb(226, 160, 38);
}
/*кнопка загрузки*/
.track-upload
{
	transition-duration: .4s;
	position: relative; /* Даем возможность делать позиционирование, внутри данного элемента */
	overflow: hidden; /* Все что выходит за пределы - скрываем */
	width: 40%; /* Задаем ширину кнопки выбора файла */
	height: 25px; /* Задаем высоту кнопки выбора файла */
	/* background: rgb(89, 89, 89); */
    background-color: rgb(169, 154, 190);
	padding: 8px 4px;
	color: #fff;
	line-height: 36px;
	text-align: center;
}
.track-upload:hover 
{
	/* background: rgb(128, 128, 128); */
    background-color: rgb(141, 111, 185);
}
.track-upload label, .track-upload-drop label, .track-upload-drop2 label
{
	/* Растягиваем label на всю возможную площадь блока .file-upload */
	content: "Добавить музыку";
	border: none;
	display: block;
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	cursor: pointer;
}
/*кнопка загрузки дроп*/
.track-upload-drop
{
	z-index: 90;
	transition-duration: .4s;
	border-style:  dashed;
	border-color:  rgb(153, 153, 153);
	position: relative; /* Даем возможность делать позиционирование, внутри данного элемента */
	width: 93.2%; /* Задаем ширину кнопки выбора файла */
	height: 80px; /* Задаем высоту кнопки выбора файла */
	line-height: 96px;
	overflow: hidden;
	background:rgb(242, 255, 255);
	padding: 8px 4px;
	color: rgb(0, 0, 0);
	text-align: center;
}
/*кнопка загрузки дроп2*/
.track-upload-drop2
{
	z-index: 90;
	border-style:  dashed;
	border-color:  rgb(0, 92, 230);
	position: relative; /* Даем возможность делать позиционирование, внутри данного элемента */
	width: 93.2%; /* Задаем ширину кнопки выбора файла */
	height: 80px; /* Задаем высоту кнопки выбора файла */
	line-height: 96px;
	overflow: hidden;
	background: rgb(242, 255, 255);
	padding: 8px 4px;
	color: rgb(0, 0, 0);
	text-align: center;
}
.loading
{
    margin: 0 22px;
    width: 6%;
    position: relative;
    left: 500px;
}

.cssload-loader {
	display: block;
	margin:0 auto;
	width: 25px;
	height: 25px;
	position: relative;
	border: 5px solid rgb(0,0,0);
	animation: cssload-loader 2.3s infinite ease;
		-o-animation: cssload-loader 2.3s infinite ease;
		-ms-animation: cssload-loader 2.3s infinite ease;
		-webkit-animation: cssload-loader 2.3s infinite ease;
		-moz-animation: cssload-loader 2.3s infinite ease;
}

.cssload-loader-inner {
	vertical-align: top;
	display: inline-block;
	width: 100%;
	background-color: rgb(70, 70, 70);
	animation: cssload-loader-inner 2.3s infinite ease-in;
		-o-animation: cssload-loader-inner 2.3s infinite ease-in;
		-ms-animation: cssload-loader-inner 2.3s infinite ease-in;
		-webkit-animation: cssload-loader-inner 2.3s infinite ease-in;
		-moz-animation: cssload-loader-inner 2.3s infinite ease-in;
}

@keyframes cssload-loader {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-o-keyframes cssload-loader {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-ms-keyframes cssload-loader {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-webkit-keyframes cssload-loader {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@-moz-keyframes cssload-loader {
	0% {
		transform: rotate(0deg);
	}
	
	25% {
		transform: rotate(180deg);
	}
	
	50% {
		transform: rotate(180deg);
	}
	
	75% {
		transform: rotate(360deg);
	}
	
	100% {
		transform: rotate(360deg);
	}
}

@keyframes cssload-loader-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-o-keyframes cssload-loader-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-ms-keyframes cssload-loader-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-webkit-keyframes cssload-loader-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

@-moz-keyframes cssload-loader-inner {
	0% {
		height: 0%;
	}
	
	25% {
		height: 0%;
	}
	
	50% {
		height: 100%;
	}
	
	75% {
		height: 100%;
	}
	
	100% {
		height: 0%;
	}
}

</style>