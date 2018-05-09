<template>
    <div class="track-performer-name">
        <p class="track-name">{{ trackName }}</p>
        <p class="performer-name">{{ performerName }}</p>
    </div>
</template>

<script>
export default {
    name: 'track-performer',
    props: [
        'trackName',
        'performerName'
    ]
}
</script>

<style scoped>
.track-name {
	font: 20px Arial,Helvetica,sans-serif;
	color: rgb(0, 0, 0);/* #e8e8e8;*/
	text-align: right;
	width: 60%;
	height: 32px;
    right: 296px;
    margin: auto;
	position: absolute;
	line-height: 32px;
}
.performer-name {
	font: 18px Arial,Helvetica,sans-serif;
	color: rgb(89, 89, 89);
	text-align: right;
	width: 60%;
	height: 32px;
	top: 32px;
    right: 296px;
    margin: auto;
	position: absolute;
	line-height: 32px;
}
</style>