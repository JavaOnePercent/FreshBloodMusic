from rest_framework import serializers
from mainapp.models import Track, LikedTrack


class TrackSerializer(serializers.ModelSerializer):  # сериалайзер трека для метода nextTrack
    image_alb = serializers.ReadOnlyField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'link_trc', 'image_alb', 'name_per')  # is_liked


class LikedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedTrack
        fields = ('user_id', 'trc_id')


class NoLinkTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.ReadOnlyField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per')  # is_liked


"""class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('name_alb', 'image_alb', 'tracks')"""

