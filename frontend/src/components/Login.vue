<template>
<div class="background">
    <form method="post">
        <div id="form" class="form">
            <br>
            <input id="username" type="text" name="username" placeholder="Имя пользователя" v-model="username" @input="inputChange" >
            <div v-if=(errorMessUser) id="error" class="error" :data-title="errorMessUser"></div>
            <input id="password" type="password" name="password" placeholder="Пароль" v-model="password" @input="inputChange" >
            <div v-if=(errorMessPass) id="error" class="error" :data-title="errorMessPass"></div>
            <div class="border">
                <input class="button" @click.prevent="sendRegistration" type="submit" name="register" value="Войти">
            </div>
        </div>
    </form>
</div>
</template>

<script>
export default {
    name: 'login',
    data() {
        return {
            errorMessUser:'',
            errorMessPass:'',
            username: '',
            password: ''
        }
    },
    methods: {
        inputChange(e) {
            e.preventDefault();
            if(e.target.value.lenght != 0){
                e.target.style="background-color: rgba(255,255,255,0.92)";
                if(this.errorMessUser=="Кажется, вы ошиблись")
                {
                    this.errorMessUser=''
                    document.getElementById('username').style.backgroundColor="rgba(255,255,255,0.92)"
                    document.getElementById('password').style.backgroundColor="rgba(255,255,255,0.92)"
                }
            }
            if(e.target.name == 'username')
            {
                this.errorMessUser=''
            }
            else 
                this.errorMessPass=''
        },
        sendRegistration() {
            if(this.username && this.password) 
            {
                var data = new FormData();
                data.append('username', this.username);
                data.append('password', this.password);
                var self = this;
                this.$http.post('login', data).then(function(response){
                    self.$store.commit('username', response.data.username)
                    self.$router.push('performers/me')
                },function(error){
                    document.getElementById('username').style.backgroundColor="rgba(255, 179, 179,0.98)"
                    document.getElementById('password').style.backgroundColor="rgba(255, 179, 179,0.98)"
                    this.errorMessUser='Кажется, вы ошиблись'
            });
            }
            if(!this.username)
            {
                document.getElementById('username').style.backgroundColor="rgba(255, 179, 179,0.98)"
                this.errorMessUser = 'Поле не может быть пустым'
            }
            else
            {
                document.getElementById('username').style.backgroundColor="rgba(255,255,255,0.92)"
                this.errorMessUser = ''
            }
            if(!this.password)
            {
                document.getElementById('password').style.backgroundColor="rgba(255, 179, 179,0.98)"
                this.errorMessPass = 'Поле не может быть пустым'
            }
            else
            {
                document.getElementById('password').style.backgroundColor="rgba(255,255,255,0.92)"
                this.errorMessPass = ''
            }
        }
    }
}
</script>

<style scoped>
.background
{
    position: absolute;
    /*background: linear-gradient(0deg, rgba(0, 255, 0, .2), rgba(0, 85, 255,0.2)), url(/RegistrationFon.jpg); */
    /*background: linear-gradient(0deg, rgba(204, 105, 39, 0.3), rgba(0, 85, 255,0.3)), url(/308943842556095.jpg);*/
    background: linear-gradient(0deg, rgba(204, 105, 39, 0.3), rgba(0, 85, 255,0.3)), url(/77491359960545_tumblr_ocp55as7o51qkprgpo1_1280.gif);
    background-position:center; 
    background-size: cover;
    height: 100%;
    width: 100%;
}
label
{
    font-size: 375%;
    width: 23.915%;
    margin-bottom: 15px;
}
.form :not(:nth-child(2))
{
    border-top:0px; 
}
.form .border
{
    border-radius:7px 7px 7px 7px; 
    border-top:2px solid rgb(255,255,255); 
}
.form input[name="username"]
{
    border-radius:7px 7px 0 0; 
}
.form input[name="password"]
{
    border-radius:0 0 7px 7px; 
}
*:focus
{
    outline: none;
    background-color: rgb(230, 242, 255);
}
.form
{
    position: absolute;
    /*background-color: rgba(201, 136, 214,0.1); /*rgba(200, 53, 229,0.7) прозрачность */
    left: 0;
    height: 300px;
    right: 0;
    top:25%;
    bottom: 0;
    width: 600px;
    margin:0 auto;
    text-align: center;
}
form input
{
    left:15%;
    /*left: 20px;*/
    background-color: rgba(255,255,255,0.92);
    position: relative;
    float: left;
    width: 380px;
    height: 40px;
    font-size: 15px;
    padding-left:15px; 
    padding-right:35px;
    border: 1px solid rgba(0,0,0,0.3);
}
p
{
    color: red;
    line-height:30px;
    height: 30px;
    font-size: 25px;
    width: 300px;
    margin: auto;
    display: block;
}
.border
{
    left:15%;
    float: left;
    position: relative;
    box-sizing: border-box;
    border: 2px solid rgb(255,255,255);
    border-radius:7px 7px 7px 7px; 
    margin: 15px auto;
    height: 45px;
    width: 432px;
}
form input[name="register"]
{ 
    left: 0;
    width: 432px;
    height: 40px;
    border-radius:7px 7px 7px 7px; 
    color: #fff;
    line-height:10px;
    font-size: 120%;
    padding: 0px;
    font-weight: 600;
    border: none;
    /*border: 2px solid rgb(255,255,255);
    border-radius:7px 7px 7px 7px; */
    background-color: rgba(0,0,0,0.0);
    cursor: pointer;
}
.border::before{
    transition: left .2s linear;
    opacity: 0;
    content: '';
    position: absolute;
    border-radius:4px 4px 4px 4px; 
    top: 4px; left: 4px; bottom: 4px; right: 4px;
    border: 1px solid rgb(255,255,255);
}
.border:hover::before
{
    transition-duration: .2s;
    opacity: 100;
}
.border:hover
{  
    background-color:rgba(230, 242, 255,0.2);
    /*background-color: rgb(14, 201, 60);*/
}
.error
{   
    float: left;
    right: 78px;
    position: relative;
    float: right;
    width: 43px;
    height: 43px;
}
.error::before
{
    content: '😡';
    display: block;
    position: absolute;
    top: 22%; left: 4px; bottom: 4px; right: 4px;
}
.error::after
{
    opacity: 0;
    content: attr(data-title);
    display: block;
    background-color: rgba(255, 102, 102,0.8);
    color: white;
    line-height: 35px;
    width: 225px;
    height: 35px;
    position: absolute;
    top: 13%; left: 45px; bottom: 4px; right: 4px;
}
.error:hover::after
{
    opacity: 100;
}

</style>