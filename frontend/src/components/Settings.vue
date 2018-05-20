<template>
  <div class="nastr-conteiner">
        <form method="POST">
            <div class="nastr-row">
                <div class="mainNastr block">
                    <label>Настройки</label>
                    <hr>
                    <div class="N-name str">
                        <label class="line">Ваше имя:</label>
                        <input v-model="name" class="" type="text" name="N-name" maxlength="40"/>
                    </div>
                    <div class="N-Lable str">
                        <label class="line">Аватар:</label>
                        <input @change="setLabel" type="file" name="lable" multiple accept="image/*" />
                    </div> 
                    <div class="N-Description nastr-row">
                        <label class="line">О себе:</label>
                        <textarea v-model="description" class="" type="text" name="N-Description" maxlength="800">
                        </textarea>
                    </div>              
                </div>
        
                <div class="N-vk block nastr-row">
                    <label class="line">Привязка акканута к ВК:</label>
                    ну а тут можно просто ссылку требовать в инпут 
                </div>
        
                <div class="N-style block nastr-row">
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
                            <router-link :to="'/performers/' + myPerformerID"><button @click='saveSettings' class="N-sub" name="sub"> Сохранить </button></router-link>
                            <router-link :to="'/performers/' + myPerformerID"><div type="reset" class="Cancel" @click="cencleClick">Отмена</div></router-link>
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
            id: 0
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
        this.$http.get('performers/' + this.myPerformerID).then(function(response){
            this.id = this.myPerformerID
            this.name = response.data.name_per
            //this.label = response.data.image_per
            this.description = response.data.about_per
        })
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
            data.append('id', this.id);
            this.$http.post('performers', data).then(function(response){
                //this.$store.commit('performerLogo', '');
                this.$store.commit('performerLogo', this.label);
                this.$emit('cencle-clicked');
            });
        },
        cencleClick(){
            this.$emit('cencle-clicked');
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
    top: 55px;
    position: relative;
    padding-left: 15px;
    padding-right: 15px;
    max-width: 1024px;
    margin: 0 auto;
    padding-bottom:69px; 
}
.nastr-row
{
    padding-top: 15px; 
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
    padding: 1%;
    background-color: #fff;
    display: block;
    box-sizing: border-box;
    margin-bottom: 1.5%;
}
.str
{
    width: 100%;
    padding-bottom: 13px;
}
input
{
    padding: 5px;
    width: 50%;
    height: 15px;
}
textarea
{
    padding: 5px;
    width: 50%;
    height: 60px;
    resize: vertical;
    max-height: 250px;
    min-height: 60px;
} 
.line
{
    padding-right: 9px;
    line-height: 28px;
    width: 25%;
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
	background-color: rgb(102, 204, 0);
	border: none;
	width: 30%;
	height: 40px;
	padding-right: 5px;
	position: relative;
	line-height: 35px;
	text-align: center;
}
.Cancel
{
    cursor: pointer;
    text-align: center;
    float: left;
    margin-left:80px; 
    width: 20%;
    height: 40px;
    line-height: 40px;
    background-color: rgb(153, 153, 153);
}
</style>
