from rest_framework import serializers
from mainapp.models import Track, LikedTrack, Genre, GenreStyle, Performer


class TrackSerializer(serializers.ModelSerializer):  # сериалайзер трека для метода nextTrack
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'audio_trc', 'image_alb', 'name_per')  # is_liked


class LikedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedTrack
        fields = ('user_id', 'trc_id')


class NoLinkTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per')


class TopTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per', 'rating_trc')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name_gnr')


class GenreStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreStyle
        fields = ('id', 'name_stl')


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = ('name_per', 'image_per')


"""class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('name_alb', 'image_alb', 'tracks')"""

