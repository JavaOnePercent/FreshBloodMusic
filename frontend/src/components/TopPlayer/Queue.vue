<template>
    <div>
        <div :class="isFull ? 'full-queue' : 'queue'">
            <!--<img @click="openQueue" class="Button queue-button" src="{% static 'mainapp/images/queue.svg' %}" draggable="false"/>-->
            <transition name="queue">
                <draggable v-model="queueTracks" :options="{group:'people'}" @start="drag=true" @end="drag=false" v-show="showQueue">
                    <div :key="index" :class="isFull ? 'full-queue-element' : 'queue-element'" v-for="(track, index) in queueTracks">
                        <img :src="track.image_alb" :class="isFull ? 'full-queue-img' : 'queue-img'"/>
                        <span :style="track.style" :class="isFull ? 'full-queue-text' : 'queue-text'">{{ track.name_trc }}</span>
                    </div>
                </draggable>
                <!--<div :class="isFull ? 'full-queue-list' : 'queue-list'" v-show="showQueue">
                    <div @mouseenter="mouseEnterElement(index)" @mouseleave="mouseLeaveElement(index)" :key="index" :class="isFull ? 'full-queue-element' : 'queue-element'" v-for="(track, index) in tracksComputed">
                        <img :src="track.img" :class="isFull ? 'full-queue-img' : 'queue-img'"/>
                        <span :style="track.style" :class="isFull ? 'full-queue-text' : 'queue-text'">{{ track.text }}</span>
                    </div>
                </div>-->
            </transition>
        </div>
        <div :class="isFull ? 'full-history' : 'history'">
            <transition name="history">
                <div :class="isFull ? 'full-queue-list' : 'queue-list'" v-show="showHistory">
                    <div :key="index" :class="isFull ? 'full-queue-element' : 'queue-element'" v-for="(track, index) in historyTracks">
                        <img :src="track.image_alb" :class="isFull ? 'full-queue-img' : 'queue-img'"/>
                        <span :style="track.style" :class="isFull ? 'full-queue-text' : 'queue-text'">{{ track.name_trc }}</span>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
    name: 'queue',
    components: {
        draggable
    },
    props: ['isFull'],
    created() {
        this.$bus.$on('queue-opened', event => {
            //this.playNow(event.id);
            this.openQueue();
        });
        this.$bus.$on('history-opened', event => {
            //this.playNow(event.id);
            this.openHistory();
        });
    },
    data() {
        return {
            showQueue: false,
            showHistory: false
        }
    },
    computed: {
        queueTracks: {
            get() {
                return this.$store.state.queueTracks
            },
            set(value) {
                this.$store.commit('updateQueueTracks', value)
            }
        },
        historyTracks() {
            return this.$store.state.historyTracks
        }
    },
    watch: {
        isFull(iF) {
            if(!iF)
                this.hideLists()
        }
    },
    methods: {
        hideLists() {
            this.showQueue = false
            this.showHistory = false
        },
        openQueue() {
            this.showQueue = !this.showQueue;
            this.showHistory = false
        },
        openHistory() {
            this.showHistory = !this.showHistory;
            this.showQueue = false
        },
    },
}
</script>

<style scoped>

.full-history {
    position: absolute;
    margin: auto;
    width: 250px;
    height: 50px;
    left: -350px;
    top: 150px;
}

.full-queue {
    position: absolute;
    margin: auto;
    width: 250px;
    height: 50px;
    right: -350px;
    top: 150px;
}

.full-queue-button {
    width: 50px;
    height: 50px;
    left: 0;
    right: 0;
    position: absolute;
    margin: auto;
}

.full-queue-button:hover {
    left: -1px;
    top: -1px;
    width: 52px;
    height: 52px;
}

.full-queue-list {
    position: absolute;
    margin: auto;
    width: 250px;
    z-index: 1000;
    /*background: rgba(245, 245, 245, 0.95);
    box-shadow: 0 6px 12px rgba(0,0,0,0.08), 0 10px 10px rgba(0,0,0,0.05);*/
    display: flex;
    flex-direction: column;
}

.full-queue-element {
    height: 40px;
    /*flex-basis: 40px;*/
    background: rgba(105, 105, 105, 0.3);
    box-shadow: 0 6px 12px rgba(0,0,0,0.04);
    margin: 0px 0 10px 0;
}

.full-queue-element:hover {
    background: rgba(0, 0, 0, 0.8);
    cursor: pointer;
}

.full-queue-element .full-queue-text:hover {
    color: white;
}

.full-queue-img {
    position: absolute;
    height: 40px;
    width: 40px;
    
}

.full-queue-text {
    color: black;
    position: absolute;
    left: 55px;
    width: 195px;
    height: 40px;
    line-height: 40px;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.full-queue-play {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    height: 30px;
    width: 30px;
}
</style>


