<template>
  <div class="nastr-conteiner">
        <form method="POST">
            <div class="nastr-row">
                <div class="mainNastr block">
                    <label style="fontSize:135%">Настройки</label>
                    <hr>
                    <div class="N-name str">
                        <label class="line">Ваше имя:</label>
                        <input v-model="name" class="" type="text" name="N-name" maxlength="40"/>
                    </div>
                    <div class="N-Lable str nastr-row" style="padding:15px 0">
                        <label class="line">Аватар:</label>
                        <img style="display:none" id="lable" class="lable" :src="src" alt="обложка">
                        <label class="imit" @click="imit">Выберите фото</label>
                        <input style="display:none" ref="fileInput" @change="setLabel" type="file" name="lable" multiple accept="image/*" />
                    </div> 
                    <div class="N-Description str">
                        <label class="line">О себе:</label>
                        <textarea v-model="description" class="" type="text" name="N-Description" maxlength="800">
                        </textarea>
                    </div>              
                </div>
        
                <div style="display:none" class="N-vk block nastr-row">
                    <label class="line">Привязка акканута к ВК:</label>
                    ну а тут можно просто ссылку требовать в инпут 
                </div>
        
                <div style="display:none" class="N-style block nastr-row">
                    <label>Вид страницы</label>
                    <hr>
                    <div class="str">
                        <label class="line">Фон профиля:</label>
                        <input type="file" name="background" multiple accept="image/*" />
                    </div>
                    <div class="str">
                        <label class="line">Цвет фона:</label>
                        <input type="color"/>
                    </div>
                    <div class="str">
                        <label class="line">Любимый альбом:</label>
                        поиск по всем альбомам
                    </div>
                </div>
        
                <div class="N-subbmit block nastr-row">
                    
                        <div class="str" > 
                            <div @click='saveSettings' class="N-sub" name="sub"> Сохранить </div>
                            <router-link :to="'/performers/' + myPerformerID"><div type="reset" class="Cancel">Отмена</div></router-link>
                        </div>
                    
                </div>             
            </div>
        </form>
    </div>
</template>

<script>
export default {
  name: 'settings',
  data: function() {
        return {
            name: '',
            label: null,
            description: '',
            id: 0, 
            src: ''
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
    watch: {
        myPerformerID(id) {
            if(id !== 0)
                this.getData()
        }
    },
    created() {
        this.getData()
    },
    methods: {
        getData() {
            this.$http.get('../api/performers/' + this.myPerformerID).then(function(response){
                    this.id = this.myPerformerID
                    this.name = response.data.name_per
                    //this.label = response.data.image_per
                    this.src = response.data.image_per + '?' + Math.random()
                    this.description = response.data.about_per
                    document.getElementById('lable').style = ""
                })
        },
         setLabel(e) {
            e.preventDefault();
            var preview = document.querySelector('img[alt="обложка"]');  
            var file    = document.querySelector('input[name="lable"]').files[0];
            var reader  = new FileReader();

            this.label = e.target.files[0];

            reader.onloadend = function () {
                preview.src = reader.result;
                document.getElementById('lable').style.display="block"
            }
            
            if (file) {
            if(e.target.files[0].type =="image/jpeg" || e.target.files[0].type =="image/png" ) //проверяем формат файла (переписать)
            {   
                reader.readAsDataURL(file);
                this.imgStyle='Loaderimg';
            } 
            else 
            {
                document.getElementById('lable').style.display="none"
                preview.src = "";
                this.$refs.fileInput.value  =  ""; 
            }
            }
            else 
            {
                document.getElementById('lable').style.display="none"
                preview.src = "";
                this.$refs.fileInput.value  =  ""; 
            }

        },
        imit:function(){
            this.$refs.fileInput.click()
        },
        saveSettings() {
            var data = new FormData();
            data.append('name', this.name);
            data.append('label', this.label);
            data.append('description', this.description);
            var self = this
            this.$http.put('../api/performers/' + this.id, data, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(function(response){
                this.$store.commit('performerLogo', '');
                self.$router.push('performers/' + self.myPerformerID)
            });
        }
    },
    computed: {
        myPerformerID() {
            return this.$store.state.myPerformerID
        }
    }
}
</script>

<style scoped>


.nastr-conteiner
{
    background-color: rgba(70, 57, 78, 0.281);
    /* background: linear-gradient(0deg, rgba(255, 255, 153, .2), rgba(36, 87, 189, 0.2)); */
    font-size: 110%;
    /* top: 55px; */
    position: absolute;
    min-height: 100%;
    width: 100%;
    margin: 0 auto;
    /* padding-bottom:69px;  */
}
.nastr-row
{
    padding-bottom:69px; 
    padding-left: 15px;
    padding-right: 15px;
    margin: 0 auto;
    max-width: 1143px; 
    min-width: 915px; 
    padding-top: 70px; 
    margin: 0 auto;
}
.nastr-row:after
{
    content: "";
    display: table;
    clear: both;
}
*:focus {outline: none;}

.block
{
    box-shadow: 0 5px 12px rgba(0,0,0,0.15), 0 3px 3px rgba(0,0,0,0.12);
    padding: 1%;
    background-color: #fff;
    display: block;
    box-sizing: border-box;
    margin-bottom: 1.5%;
}
.str
{
    height: auto;
    width: 100%;
    padding-bottom: 13px;
}
.lable
{
    margin-right:10px; 
    float: left;
    position: relative;
    object-fit: cover;
    border-style: solid;
    border-color:black;
    width: 250px;
    height: auto;
}
input
{
    padding: 5px;
    width: 500px;
    height: 15px;
}
input[type=file]
{
    /* float: left;
    clear: both; */
    position: relative;
    width: 200px;
}
.imit
{
    cursor: pointer;
    background-color: rgba(0, 153, 153,0.5);
    line-height: 28px;
    display: inline-block;
    height: 28px;
    /* border: solid;
    border-color:black;
    border-width: 0.1px; */
    position: relative;
    padding: 0 5px
}
.imit:hover
{
    background-color: rgba(27, 223, 223, 0.5);
}
textarea
{
    font-family: Arial,Helvetica,sans-serif;
    padding: 5px;
    width: 500px;
    height: 60px;
    resize: vertical;
    max-height: 250px;
    min-height: 60px;
} 
.line
{
    padding-right: 9px;
    line-height: 28px;
    position: relative;
    width: 300px;
    float: left;
    text-align: right;
}
.N-sub
{
    float: left;
    left: 50px;
    color: #fff;
	font-size: 100%; 
	cursor: pointer;
	/* background-color: rgba(0, 153, 38,0.7); */
    background-color: rgb(255, 181, 43);
	border: none;
	width: 30%;
	height: 40px;
	padding-right: 5px;
	position: relative;
	line-height: 40px;
	text-align: center;
}
.N-sub:hover
{
    /* background-color:  rgba(16, 180, 57, 0.7); */
    background-color: rgb(226, 160, 38);
}
.Cancel
{
    color: white;
    cursor: pointer;
    text-align: center;
    float: left;
    margin-left:80px; 
    width: 20%;
    height: 40px;
    line-height: 40px;
    /* color: black; */
    /* background-color: rgb(153, 153, 153); */
    background-color: rgb(169, 154, 190);
}
.Cancel:hover
{
    /* background-color: rgb(177, 177, 177); */
    background-color: rgb(141, 111, 185);
}
</style>
