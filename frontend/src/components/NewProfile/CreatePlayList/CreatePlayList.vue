<template>
    <div class="CreatePlayList">
        <div class="PlayList-img-conteiner" >
            <label>Обложка</label>
            <img :class="imgStyle"  @click="imit" src="/static/mainapp/images/camera.svg" alt="обложка">
            <input style="display: none" id="photo" ref="fileInput" class="add" @change="sync_photo" type="file" name="photo" accept="image/*,image/jpeg" > <!--если шо тот ref -->
        </div>
        <div class="playlistName-conteiner">
            <label for="playlistName">Плейлист<span style="font-size:12px">( обязательное поле )</span></label>
            <input :class="{'error':error!=''}" class="playlistName" type="text" name="playlistName" placeholder="" v-model='playlistName' @change="error=''" maxlength="23">
            <span>{{error}}</span>
            <div @click="send" class="playAll"> 
                <span> Создать плейлист </span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CreatePlayList',
    data() {
        return {
            imgStyle:'camera',
            playlistName:'',
            lable: '',
            error: ''
        }
    },
    methods: {
        imit:function(){
            this.$refs.fileInput.click()
        },
        sync_photo: function (e) {
            e.preventDefault();
            var preview = document.querySelector('img[alt="обложка"]');
            var file    = document.querySelector('input[name="photo"]').files[0];
            var reader  = new FileReader();
        
            this.errorMessage = ''
            this.lable = e.target.files[0];
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
            }
            }
            else 
            {
                preview.src = "/static/mainapp/images/camera.svg";
                this.imgStyle='camera';
            }
        },
        send:function () 
        {
            if (this.playlistName.length === 0)
            {
                this.error='поле "плейлист" не может быть пустым'
                return
            }

            var playlistName = this.playlistName
            var lable = this.lable
            var data = new FormData()
            data.append('image', this.lable)
            data.append('title', this.playlistName)
            this.$http.post('api/playlists', data, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(response => {
                console.log('победа')
                this.$emit('playlist_created', true)
            })
        },
    }
}
</script>

<style scoped>
@media (max-width: 988px)
{
    .CreatePlayList
    {
        margin-left: 15px;
        top: 15px;
        padding: 10px;
        position: relative;
        display: flex;
        flex-direction: column;
        background-color: white;
    }
}
@media (min-width: 988px)
{
    .CreatePlayList
    {
        margin-left: 15px;
        padding: 10px;
        top: 15px;
        position: relative;
        display: flex;
        background-color: white;
    }
}
.PlayList-img-conteiner
{
	display: flex;
	flex-direction: column;
    position: relative;
    margin-right: 22px;
    margin-bottom: 22px;
}
.PlayList-img-conteiner label, .playlistName-conteiner label
{
    font-size: 25px;
}
.camera
{
	padding: 0;
	object-fit: scale-down;
	display: block;
    border-style: solid;
    border-color:black;
    width: 200px;
    height: 200px;
}
.Loaderimg
{
	cursor: pointer;
	padding: 0;
	object-fit: cover;
	display: block;
    border-style: solid;
    border-color:black;
    width: 200px;
    height: 200px;
}
.camera:hover, .Loaderimg:hover
{
	cursor: pointer;
	filter: opacity(50%);
}
.playlistName-conteiner
{
    width: 445px;
    width: 80%;
	display: flex;
	flex-direction: column;
    position: relative;
}
input
{
    font-size: 20px;
    outline: none;
    height: 30px;
    border-style: solid;
    border-color: rgb(153, 153, 153);
    background-color: rgba(255, 255, 255,0.4);
    padding: 3px 5px; 
}
.playAll
{
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    margin-top:5px;
    margin-bottom: 5px; 
    padding: 5px;
    height: 30px;
    cursor: pointer;
    line-height: 30px;
    font-size: 18px;
    text-align: center;
    background-color: rgb(255, 181, 43);
    /* transform: skew(-10deg); */
    width: 233.656px;
}
.playAll:hover
{
    background-color: rgb(226, 160, 38);
    cursor: pointer;
}
.error
{
    border: 2px solid rgb(226, 160, 38);
}

</style>