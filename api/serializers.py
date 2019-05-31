from rest_framework import serializers
from api.models import *


class TrackSerializer(serializers.ModelSerializer):  # сериалайзер трека для метода nextTrack
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_alb = serializers.ReadOnlyField(source='alb_id.name_alb')  # название альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя
    per_id = serializers.ReadOnlyField(source='alb_id.per_id.id')  # ид исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'audio_trc', 'image_alb', 'name_per', 'per_id', 'name_alb')  # is_liked


class NoLinkTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя
    id_per = serializers.ReadOnlyField(source='alb_id.per_id.id')  # id исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per', 'id_per', 'rating_trc', 'duration', 'alb_id')


class TopTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека без ссылки на аудио
    image_alb = serializers.FileField(source='alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='alb_id.per_id.name_per')  # имя исполнителя
    name_gnr = serializers.ReadOnlyField(source='alb_id.stl_id.gnr_id.name_gnr') # название жанра
    name_stl = serializers.ReadOnlyField(source='alb_id.stl_id.name_stl') # жанра стиля
    id_per = serializers.ReadOnlyField(source='alb_id.per_id.id')  # id исполнителя

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'image_alb', 'name_per', 'audio_trc', 'rating_trc', 'name_gnr', 'name_stl', 'id_per')


class SmallTrackSerializer(serializers.ModelSerializer):  # сериалайзер трека только с именем
    # likes = serializers.IntegerField()

    class Meta:
        model = Track
        fields = ('id', 'name_trc', 'rating_trc', 'audio_trc', 'numplays_trc', 'duration')


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
        fields = ('name_per', 'image_per', 'id')


class AlbumSerializer(serializers.ModelSerializer):
    style = serializers.ReadOnlyField(source='stl_id.name_stl')
    genre = serializers.ReadOnlyField(source='stl_id.gnr_id.name_gnr')
    name_per = serializers.ReadOnlyField(source='per_id.name_per')
    image_per = serializers.FileField(source='per_id.image_per')

    class Meta:
        model = Album
        fields = ('name_alb', 'genre', 'style', 'image_alb', 'date_alb', 'id', 'about_alb', 'numplays_alb',
                  'rating_alb', 'name_per', 'image_per', 'per_id')


class PlaylistSerializer(serializers.ModelSerializer):
    name_per = serializers.ReadOnlyField(source='per_id.name_per')

    class Meta:
        model = Playlist
        fields = ('id', 'title', 'image', 'per_id', 'name_per')


class PlaylistTrcSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='playlist.title')
    id = serializers.ReadOnlyField(source='playlist.id')

    class Meta:
        model = PlaylistTrack
        fields = ('id', 'title')


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = NoLinkTrackSerializer(source='trc_id', read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ('id', 'track')


class PlaylistTracksSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(source='pl_tracks', many=True, read_only=True)
    name_per = serializers.ReadOnlyField(source='per_id.name_per')

    class Meta:
        model = Playlist
        fields = ('id', 'title', 'image', 'per_id', 'tracks', 'name_per')


'''class FullAlbumSerializer(serializers.ModelSerializer):
    style = serializers.ReadOnlyField(source='stl_id.name_stl')
    genre = serializers.ReadOnlyField(source='stl_id.gnr_id.name_gnr')
    tracks = SmallTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('name_alb', 'genre', 'style', 'image_alb', 'date_alb', 'id', 'about_alb', 'numplays_alb',
                  'rating_alb', 'tracks')'''


class AlbumTracksSerializer(serializers.ModelSerializer):
    tracks = SmallTrackSerializer(many=True, read_only=True)
    style = serializers.ReadOnlyField(source='stl_id.name_stl')
    genre = serializers.ReadOnlyField(source='stl_id.gnr_id.name_gnr')
    name_per = serializers.ReadOnlyField(source='per_id.name_per')

    class Meta:
        model = Album
        fields = ('name_alb', 'image_alb', 'date_alb', 'id', 'about_alb', 'numplays_alb',
                  'rating_alb', 'per_id', 'name_per', 'style', 'genre', 'tracks')


class FullPerformerSerializer(serializers.ModelSerializer):
    # albums = FullAlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Performer
        fields = ('id', 'name_per', 'image_per', 'about_per', 'rating_per', 'date_per')  # , 'albums')


class LikedTrackSerializer(serializers.ModelSerializer):
    image_alb = serializers.FileField(source='trc_id.alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='trc_id.alb_id.per_id.name_per')  # имя исполнителя
    name_trc = serializers.ReadOnlyField(source='trc_id.name_trc')  # имя трека
    duration = serializers.ReadOnlyField(source='trc_id.duration')

    class Meta:
        model = LikedTrack
        fields = ('name_trc', 'name_per', 'image_alb', 'trc_id', 'duration')


class TrackHistorySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='trc_id', read_only='True')
    image_alb = serializers.FileField(source='trc_id.alb_id.image_alb')  # картинка альбома
    name_per = serializers.ReadOnlyField(source='trc_id.alb_id.per_id.name_per')  # имя исполнителя
    name_trc = serializers.ReadOnlyField(source='trc_id.name_trc')  # имя трека
    audio_trc = serializers.FileField(source='trc_id.audio_trc')  # имя трека

    class Meta:
        model = TrackHistory
        fields = ('name_trc', 'name_per', 'image_alb', 'id', 'audio_trc')


class LikedPlaylistSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='playlist_id.id')
    image = serializers.FileField(source='playlist_id.image')
    title = serializers.ReadOnlyField(source='playlist_id.title')
    per_id = serializers.ReadOnlyField(source='playlist_id.per_id.id')
    name_per = serializers.ReadOnlyField(source='playlist_id.per_id.name_per')

    class Meta:
        model = LikedPlaylist
        fields = ('id', 'image', 'title', 'per_id', 'name_per')  # , 'date')


class LikedAlbumSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='album_id.id')
    image = serializers.FileField(source='album_id.image_alb')
    title = serializers.ReadOnlyField(source='album_id.name_alb')
    per_id = serializers.ReadOnlyField(source='album_id.per_id.id')
    name_per = serializers.ReadOnlyField(source='album_id.per_id.name_per')

    class Meta:
        model = LikedPlaylist
        fields = ('id', 'image', 'title', 'per_id', 'name_per')  # , 'date')
