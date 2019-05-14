<template>
    <div class="DelateConfirmation-Conteiner">
        <div class="DelateConfirmation">
            <h3> Вы уверено, что хотите удалить {{getAlbumName}} </h3>
            <div style="width:100%; display:flex; justify-content: center">
                <div class="btn cancel" @click="$emit('close')"> Отмена </div>
                <div class="btn accept" @click="accept(); $emit('close')"> Удалить </div>
            </div>
        </div>
        <div id='bg' class='bg' @click="$emit('close')"></div>
    </div>
</template>

<script>
export default {
    name: 'DelateConfirmation',
    props: ['albumType', 'albumName', 'albumId'],
    data() {
        return {
            methods: {
            }
        }
    },
    computed: {
        getAlbumName() {
            var str =''
            switch (this.albumType) {
                case 'album':
                    str = 'альбом '
                    break;
                case 'playlist':
                    str = 'плейлист '
                    break;
                }
            return str + '\"' + this.albumName + '\"'
        },
    },
    methods: {
        accept() {
            this.$emit('changeStatus', 'dead')
             switch (this.albumType) {
                case 'album':
                    this.deleteAlbum()
                    break;
                case 'playlist':
                    this.deletePlaylist()
                    break;
                }
        },
        deleteAlbum() {
            this.$http.delete('../api/albums/' + this.albumId, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(
                response => {
            })
        },
        deletePlaylist() {
            this.$http.delete('../api/playlists/' + this.albumId, {headers: {'X-CSRFToken': this.$root.csrftoken}}).then(
                response => {
            })
        }
    }
}
</script>

<style scoped>
.DelateConfirmation
{
    z-index: 9999;
    position: fixed;
    top: 50%;
    left: 50%;
    min-width: 250px;
    min-height: 100px;
    padding: 25px;
    transform: translate(-50%, -50%);
    background: #fff;
}
.bg
{
    bottom: 0px;
    z-index: 9998;
    position: fixed;
    overflow-y: hidden;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.3);
}
.btn
{
    display: inline-block;
    width: 150px;
    font-size: 19px;
    cursor: pointer;
    height: 30px;
    line-height: 30px;
    padding: 10px 0;
    text-align: center;
}
.btn:nth-child(1)
{
    margin-right: 15px;
}
.cancel
{
    background-color: rgb(169, 154, 190);
}
.cancel:hover
{
    background-color: rgb(141, 111, 185);
}
.accept
{
    background-color: rgb(255, 181, 43);
}
.accept:hover
{
    background-color: rgb(226, 160, 38);
}

</style>