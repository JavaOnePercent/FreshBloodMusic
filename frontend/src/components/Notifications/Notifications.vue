<template>
        <transition-group class="Notifications-Conteiner"  name="style" tag="div">
            <div class="toasts" :key="toast.id" v-for="(toast, index) in toasts">
                <div class="toast">
                    {{toast.text}}
                </div>
                <img src="/static/mainapp/images/cross.svg" class="toast__close" @click="close(index)">
            </div>
        </transition-group>
</template>

<script>
export default {
    name: 'Notifications',
    data() {
        return {
            toasts: [],
            config: {
                autohide: true,
                delay: 5000
            },
            id: 0,
            timer: null
        }
    },
    created() {
        this.$bus.$on('likeNot', data => {this.create(data)})
    },
    methods: {
        Hide() {
            if (this.config.autohide) {
                var self = this
               this.timer = setTimeout(function () {
                    self.toasts.shift()
                    this.id--
                }, this.config.delay)
            }
        },
        close(index) {
            this.toasts.splice(index, 1)
            clearTimeout(this.timer)
            this.id--
        },
        create(text) {
            var obj = {text: text, show: true, id: this.id}
                this.toasts.push(obj)
                this.id++
            this.Hide()
        }
    }
}
</script>

<style scoped >
.Notifications-Conteiner{
    position: absolute;
    top: 55px;
    right: 15px;
    width: 540px;
    z-index: 1000
}
.toast {
    overflow: hidden;
    font-size: 0.875rem;
    background-color: rgb(255, 255, 255);
    background-clip: padding-box;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 0.25rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    position: relative;
    padding: 0.75rem 2rem 0.75rem 0.75rem;
    overflow-wrap: break-word;
    word-break: break-word;
    cursor: default;
}
.toast__close {
    position: absolute;
    top: 13px;
    bottom: 0;
    right: 7.5px;
    width: 16px;
    height: 16px;
    cursor: pointer;
}
.toasts
{
    position: relative;
}
.toast:not(:last-child) {
    margin-bottom: 0.75rem;
}
.style-enter-active, .style-leave-active {
    transition: all 0.3s;
}
.style-enter, .style-leave-active {
    transform: translateX(100%);
    position: relative;
}
.style-move {
  transition: transform 0.3s;
}

</style>