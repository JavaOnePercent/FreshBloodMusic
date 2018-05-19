from rest_framework import serializers
from mainapp.models import Track, LikedTrack, Genre, GenreStyle, Performer, Album


class TrackSerializer(serializers.ModelSerializer):  # сериалайзер трека для метода nextTrack
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя
    per_id = serializers.ReadOnlyField(source='alb_id.per_id.id')  # ид исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'audio_trc', 'image_alb', 'name_per', 'per_id')  # is_liked


class NoLinkTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per')


class TopTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя
    name_gnr = serializers.ReadOnlyField(source='alb_id.stl_id.gnr_id.name_gnr') # название жанра
    name_stl = serializers.ReadOnlyField(source='alb_id.stl_id.name_stl') # жанра стиля
    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per', 'rating_trc', 'name_gnr', 'name_stl')


class SmallTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека только с именем
    class Meta:
        model = Track
        fields = ('id', 'name_trc')


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


class AlbumSerializer(serializers.ModelSerializer):
    tracks = SmallTrackSerializer(many=True, read_only=True)
    style = serializers.ReadOnlyField(source='stl_id.name_stl')
    genre = serializers.ReadOnlyField(source='stl_id.gnr_id.name_gnr')

    class Meta:
        model = Album
        fields = ('name_alb', 'genre', 'style', 'image_alb', 'date_alb', 'tracks')


class FullPerformerSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Performer
        fields = ('id', 'name_per', 'image_per', 'about_per', 'albums')


class LikedTrackSerializer(serializers.ModelSerializer):
    image_alb = serializers.FileField(source='trc_id.alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='trc_id.alb_id.per_id.name_per')  # имя исполнителя
    name_trc = serializers.ReadOnlyField(source='trc_id.name_trc')  # имя трека

    class Meta:
        model = LikedTrack
        fields = ('name_trc', 'name_per', 'image_alb', 'trc_id')

