<template>
    <div :class="isFull ? 'full-menu' : 'menu'" @click="toggleDrop">
        <img :class="isFull ? 'full-menu-pic' : 'menu-pic'" src="/static/mainapp/images/menu.svg" draggable="false"/>
        <transition name="menu-more">
            <ul class="menu-dropdown" v-show="showMenu" @mouseleave="closeDrop">
                <li @click="toPerformerPage"><p class="menuElements">На страницу исполнителя</p></li>
                <li @click="$emit('likepressed')"><p class="menuElements">{{ likeText }}</p></li>
                <li @click="report"><p class="menuElements">Пожаловаться</p></li>
            </ul>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'menu-more',
    props: [ 'performerID', 'isFull', 'isLiked' ],
    data() {
        return {
            showMenu: false,
            likeText: "Добавить в избранное"
        }
    },
    watch: {
        isLiked(iL) {
            if(iL) this.likeText = "Удалить из избранного"
            else this.likeText = "Добавить в избранное"
        }
    },
    computed: {
        trackID() {
            return this.$store.state.currentTrack.id;
        }
    },
    methods: {
        toPerformerPage() {
            this.$router.push({ name: 'performer', params: { id: this.performerID }})
            this.$emit('show-performer')
        },
        toggleDrop() {
            this.showMenu = !this.showMenu;
        },
        closeDrop() {
            this.showMenu = false;
        },
        report() {
            this.$http.put('../api/report', {}, {params: {track: this.trackID}}).then(function(response){
                this.showMenu = false;
                alert('Вы отправили жалобу!\nСпасибо, что помогаете сделать наш сервис лучше:)');
            }, function(error){
                alert('Вы уже отправляли жалобу:(');
            })
        },
    }
}
</script>

<style scoped>
li {
    display: inline-block;
    width: 100%;
    cursor: pointer;
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
    user-select: none;
    
}

.menu-more-enter-active, .menu-more-leave-active {
    transition: opacity .2s;
}
.menu-more-enter, .menu-more-leave-to {
    opacity: 0;
}

.full-menu {
    z-index: 5;
    width: 40px;
    height: 40px;
    left: -75px;
    top: 457px;
    margin: auto;
	position: absolute;
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

.full-menu-pic {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    margin: auto;
    width: 40px;
    height: 40px;
    padding: initial;
    cursor: pointer;
}

.full-menu-pic:hover {
    left: -1px;
	width: 42px;
	height: 42px;
}

.menu-pic {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    margin: auto;
    width: 30px;
    height: 30px;
    padding: initial;
    cursor: pointer;
}

.menu-pic:hover {
    left: -1px;
	width: 32px;
	height: 32px;
}

.menu-dropdown {
    position: absolute;
    margin: auto;
    bottom: 58px;
    width: 160px;
    left: -65px;
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