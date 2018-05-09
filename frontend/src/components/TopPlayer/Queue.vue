<template>
    <div class="queue">
        <!--<img @click="openQueue" class="Button queue-button" src="{% static 'mainapp/images/queue.svg' %}" draggable="false"/>-->
        <transition name="queue">
            <div class="queue-list" v-show="showQueue">
                <div @mouseenter="mouseEnterElement(index)" @mouseleave="mouseLeaveElement(index)" :key="index" class="queue-element" v-for="(track, index) in tracksComputed">
                    <img :src="track.img" class="queue-img"/>
                    <span :style="track.style" class="queue-text">{{ track.text }}</span>
                    <!--<img src="{% static 'mainapp/images/playButton.png' %}" class="queue-play">-->
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'queue',
    props: ['tracks'],
    created() {
        this.$bus.$on('queue-opened', event => {
            //this.playNow(event.id);
            this.openQueue();
        });
    },
    data() {
        return {
            showQueue: false,
            tracksComputed: []
        }
    },
    methods: {
        openQueue() {
            this.showQueue = !this.showQueue;
        },
        mouseEnterElement(index) {
            this.tracksComputed[index].text = this.tracks[index].name_per + ' - ' + this.tracks[index].name_trc;
            this.tracksComputed[index].style = 'color: white;';
            this.tracksComputed[index].img = '/static/mainapp/images/playButton.png';
        },
        mouseLeaveElement(index) {
            this.tracksComputed[index].text = this.tracks[index].name_trc;
            this.tracksComputed[index].style = '';
            this.tracksComputed[index].img = this.tracks[index].image_alb;
        },
        iterator(item, i, arr) {
            
            this.$set(this.tracksComputed, i, {img: item.image_alb, text: item.name_trc, style: ''})
            //Vue.set(this.tracksComputed[i], 'img', item.image_alb);
            //Vue.set(this.tracksComputed[i], 'text', item.name_trc);
        }
    },
    watch: {
        tracks(tracks) {
            /*for(var i = 0; i < tracks.length - this.tracksComputed.length; i++)
            {
                this.tracksComputed.push({});
            }*/
            this.tracksComputed = [];
            tracks.forEach(this.iterator);
        }
    }
}
</script>

<style scoped>

</style>


