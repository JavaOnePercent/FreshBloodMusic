<template>
    <div class="header-conteiner">
        <div class="header" >
            <div class="row">
                <router-link to="/">
                    <div class="name">
                        BoysBand
                    </div>
                </router-link>
                <div class="management">
                    <div v-if="username != ''">
                        <div class="drop-menu row" @mouseenter="menuShow=!menuShow" @mouseleave="menuShow=!menuShow" >
                            <div class="user">
                                <span>{{ username }}</span>
                                <img src="/static/mainapp/images/user.svg" alt="user">
                            </div>
                            <ul class="menu-drop" v-if="menuShow">
                                <li><router-link :to="'/performers/' + performerID">Профиль</router-link></li> <!-- <a @click="openProfile">Профиль</a> -->
                                <li><a @click="logout">Выйти</a></li>
                            </ul>

                        </div>
                        <div style="width:55px; height:55px; display:inline-block; position: relative;" class="uploud-cont" @click='showMenu'>
                            <img title="загрузить музыку" class="uploadButton" src="/static/mainapp/images/download.svg" alt="loader">
                        </div>  
                    </div>
                    <div v-else>
                        <router-link to="/login">Войти</router-link>
                        <router-link to="/register">Регистрация</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'header-container',
  data() {
        return {  
            menuShow:false
        }
    },
    methods: {
        showMenu() {
            this.$store.commit("showLoader", true)
        },
        openProfile() {
            this.$store.commit("showProfile")
        },
        logout() {
            var self = this
            this.menuShow=false
            this.$http.get('../api/logout').then(function(response){
                self.$store.commit("username", '')
            });
        }
    },
    computed: {
        username() {
            return this.$store.state.username
        },
        performerID() {
            return this.$store.state.myPerformerID
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.row
{
    margin: 0 auto;
}
.row:after
{
    content: "";
    display: table;
    clear: both;
}
/*шапка*/
.header-conteiner
{
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select:none;
    width: 100%;
    background-color: rgba(255, 254, 255, 0.98);
    z-index: 120;
    position: fixed;
    height: 55px;
    box-sizing: border-box;
    box-shadow: 0 1px 6px rgba(0,0,0,0.08), 0 1px 2.5px rgba(0,0,0,0.07);
}
.header
{
    padding-left: 15px;
    padding-right: 15px;
    left:0;
    right:0;
    box-sizing: border-box;
    margin: 0 auto;
    max-width: 1280px;
    min-width: 915px;  
}
.name
{
    color: #000;
    line-height: 55px;
    box-sizing: border-box;
    float: left;
    outline: none;
    font-size: 295%;
    width: 30%;
}
.management
{
    text-align: center;
    display: table-cell;
    vertical-align:middle;
    line-height: 55px;
    text-align: right;
    box-sizing: border-box;
    float: right;
    font-size:155%;
    width: 68%
}
.uploud-cont
{
    border-radius: 25px;
    cursor: pointer;
}
.uploud-cont:after {
  display: block;
  position: absolute;
  margin: 0;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  content: '.';
  color: transparent;
  width: 1px;
  height: 1px;
  border-radius: 50%;
  background: transparent;
}
.uploud-cont:hover:after {
  -webkit-animation: circle .3s ease-in forwards;
}
@-webkit-keyframes circle {
  0% {
    width: 1px;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    margin: auto;
    height: 1px;
    z-index: -1;
    background: #eee;
    border-radius: 100%;
  }
  100% {
    background: rgba(170, 170, 170, 0.2);
    height: 45px;
    width: 45px;
    z-index: -1;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    border-radius: 35px;
  }
} 
@supports not ( -webkit-animation: circle .3s ease-in forwards) {
    .uploud-cont:hover{
        background-color: rgba(204, 204, 204,0.3);
    }
}

.uploadButton
{
    width: 25px;
    height: auto;
    margin: auto;
    position: absolute;
    top: 0; left: 0; bottom: 0; right: 0;
}
.drop-menu:hover
{
    background-color: rgba(204, 204, 204,0.3);
}
.drop-menu
{
    position: relative;
    display: block;
    padding: 0 15px;
    cursor: pointer;
    margin-left: 35px;
    text-align: right;
    float: right;
    min-width: 155px;
    max-width: 80%;
    line-height: 55px;
    height: 55px;
}
.drop-menu img
{
    width: 25px;
    height: auto;
    position: relative;
    margin-left: 5px; 
    top: 0; left: 0; bottom: 0; right: 0;
}
.user 
{
    display: flex;
    justify-content: flex-end;
    position: relative;
    height: 55px;
    font-size: 20px;
}
.drop-menu ul
{
    width: auto; /* 140 px*/
    margin: 0px;
    position: relative;
    display: block;
    background-color: rgb(236, 236, 236);
    padding: 7px;
    box-shadow: 0 3.5px 7px rgba(0,0,0,0.25), 0 2.5px 2.5px rgba(0,0,0,0.22);
}
.drop-menu ul:hover ~ .drop-menu
{
    background-color: rgba(204, 204, 204,0.3); 
}
li a
{
    display: block;
    height: 100%;
}
.drop-menu a:hover
{
    text-decoration: none;
}
.drop-menu li
{
    display: block;
    padding: 0;
    margin: 0;
    line-height: 35px;
}

.drop-menu li:hover
{
    background-color: rgba(179, 179, 179,0.8);
}
.drop-menu li:first-child
{
    border-bottom: 2px solid rgb(153, 153, 153)
}
.management a
{
    color: #000;
    font-size:85%;
    text-decoration: none;
}
.management a:hover
{
    text-decoration: underline;
}
.management a:nth-of-type(n+2)
{
    border-left: 1px solid #000; 
    padding-left:5px; 
}
.management a:nth-of-type(n+1)
{
    padding-right:5px; 
}
</style>
