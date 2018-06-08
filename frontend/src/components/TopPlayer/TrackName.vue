<template>
    <div :class="isFull ? 'full-track-performer-name' : 'track-performer-name'">
        <p :class="isFull ? 'full-track-name' : 'track-name'">{{ trackName }}</p>
        <p :class="isFull ? 'full-performer-name' : 'performer-name'" @click="toPerformerPage">{{ performerName }}</p>
    </div>
</template>

<script>
export default {
    name: 'track-performer',
    props: [
        'trackName',
        'performerName',
        'isFull',
        'performerID'
    ],
    methods: {
        toPerformerPage() {
            this.$router.push({ name: 'performer', params: { id: this.performerID }})
        },
    }
}
</script>

<style scoped>

.full-track-performer-name {
    text-align:center;
    height: 62px;
	top: 350px;
    right: 0;
    left: 0;
    margin: auto;
	position: absolute;
}

.track-performer-name {
    text-align: right;
    height: 64px;
	top: 0px;
    right: 296px;
    /*max-width: 300px;*/
    margin: auto;
	position: absolute;
    
}

.full-track-name {
	font: 28px Arial,Helvetica,sans-serif;
	color: rgb(0, 0, 0);
    height: 32px;
    line-height: 32px;
    top: 0;
    margin: auto;
}

.track-name {
	font: 20px Arial,Helvetica,sans-serif;
	color: rgb(0, 0, 0);
    height: 32px;
    line-height: 32px;
    top: 0;
    margin: auto;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.full-performer-name {
	font: 20px Arial,Helvetica,sans-serif;
	color: rgb(89, 89, 89);
    height: 32px;
    line-height: 32px;
    top: 32px;
    margin: auto;
}

.performer-name {
	font: 18px Arial,Helvetica,sans-serif;
	color: rgb(89, 89, 89);
    height: 32px;
    line-height: 32px;
    top: 32px;
    right: 0;
    margin: auto;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
    width: auto;
    position: absolute;
}

.performer-name:hover {
    
    /*background: -webkit-linear-gradient(left, #ffd319 20%, #ff901f 40%, #ff2975 55%, #f222ff 80%, #8c1eff 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;*/
    /*color: rgb(255, 66, 66);*/
}

</style>