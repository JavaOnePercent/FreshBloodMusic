<template>
    <div class="menu" @click="toggleDrop">
        <img class="Button menu-pic" src="/static/mainapp/images/menu.png" draggable="false"/>
        <transition name="menu-more">
            <ul class="menu-dropdown" v-show="showMenu" @mouseleave="closeDrop">
                <li class="Button"><router-link :to="{ name: 'performer', params: { id: this.performerID }}"><p class="menuElements">На страницу исполнителя</p></router-link></li>
                <li class="Button"><p class="menuElements">Добавить в избранное</p></li>
                <li class="Button"><p class="menuElements">Пожаловаться</p></li>
            </ul>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'menu-more',
    props: [ 'performerID' ],
    data() {
        return {
            showMenu: false,
        }
    },
    methods: {
        toggleDrop() {
            this.showMenu = !this.showMenu;
        },
        closeDrop() {
            this.showMenu = false;
        }
    }
}
</script>

<style scoped>
li {
    display: inline-block;
    width: 100%;
}

li:hover {
    background: #252525;
}

li:hover .menuElements {
    color: white;
}

.menuElements {
    font: 15px Arial,Helvetica,sans-serif;
	color: black;/*#e8e8e8;*/
	text-align: center;
    padding: 0 10px 0 10px;
}

.menu-more-enter-active, .menu-more-leave-active {
    transition: opacity .2s;
}
.menu-more-enter, .menu-more-leave-to {
    opacity: 0;
}

.menu {
    z-index: 5;
    width: 30px;
    height: 30px;
    /*right: 191px;*/
    right: 150px;
    top: 0;
    bottom: 0;
    line-height:0;
    margin: auto;
	position: absolute;
}

.menu-pic {
    width: 100%;
    height: 100%;
    padding: initial;
}

.menu-pic:hover {
    position: absolute;
    left: -3%;
    top: -3%;
	width: 106%;
	height: 106%;
}

.menu-dropdown {
    position: absolute;
    margin: auto;
    bottom: 58px;
    width: 160px;
    right: 0;
    z-index: 100;
    list-style: none;
    padding: 0;
    background: rgba(245, 245, 245, 0.95);/*#323232;*/
    box-shadow:  0 -2px 4px rgba(0, 0, 0, .1), /*тут бы поиграть с тенями*/
    -23px 0 20px -23px rgba(0, 0, 0, .3),
    23px 0 20px -23px rgba(0, 0, 0, .3),
    0 0 40px rgba(0, 0, 0, .1) inset;
}
</style>