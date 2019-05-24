import re
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView

from .models import *
from django.http import HttpResponse, Http404
from .uploader import save_album, save_performer, save_track, save_playlist
from .serializers import *
from .model_methods import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ParseError
from datetime import date
from django.db.models import CharField, Value


@ensure_csrf_cookie
def get_token(request):
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE', 'GET'])  # обработчик лайков
def likes(request):
    if request.method == 'PUT':  # добавление лайка
        result = LikedTrackMethods.add_like(request.query_params['track_id'], auth.get_user(request).id)
        counter = LikedTrackMethods.add_increment(request.query_params['track_id'])
        if result and counter:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # удаление лайка
        result = LikedTrackMethods.remove_like(request.query_params['track_id'], auth.get_user(request).id)
        counter = LikedTrackMethods.add_decrement(request.query_params['track_id'])
        if result and counter:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":  # получение лайков для исполнителя
        performer = request.query_params['performer']
        likes = LikedTrackMethods.get(performer)
        serializer = LikedTrackSerializer(likes, many=True)
        data = serializer.data
        for datum in data:
            is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request), datum['trc_id'])
            datum.__setitem__('is_liked', is_liked)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_performer(request):
    user_id = auth.get_user(request).id
    try:
        performer = Performer.objects.get(user_id=user_id)
    except Performer.DoesNotExist:
        raise ParseError('User must be logged in to access this method')
    return performer


class PostLimitOffsetPagination(PageNumberPagination):
    page_size = 12


class SearchView(generics.ListAPIView):
    pagination_class = PostLimitOffsetPagination

    def handle_exception(self, exc):
        if type(exc) == ParseError:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exc

    def get_queryset(self):
        pass

    def list(self, request, *args, **kwargs):
        try:
            track = request.query_params['track']
            track = Track.objects.get(pk=track)
        except MultiValueDictKeyError:
            track = None
        except Track.DoesNotExist:
            raise ParseError('Track id is invalid')
        if track is not None:
            tracks = Track.objects.all()
            queryset = TrackRecommendation.calculate_recommendations([(track.id, 1)], tracks, tracks.count(),
                                                                     only_similar=True)
            ser = TrackSerializer(queryset, many=True)
            queryset = ser.data
        else:
            request = self.request

            try:
                query = request.query_params['query']
            except MultiValueDictKeyError:
                raise ParseError('query parameter must be specified')
            tracks = Track.objects.filter(name_trc__icontains=query).values('id',
                                                                            rating=F('rating_trc'),
                                                                            name=F('name_trc'),
                                                                            image=F('alb_id__image_alb'),
                                                                            type=Value('track', CharField()))
            albums = Album.objects.filter(name_alb__icontains=query).values('id',
                                                                            rating=F('rating_alb'),
                                                                            name=F('name_alb'),
                                                                            image=F('image_alb'),
                                                                            type=Value('album', CharField()))
            performers = Performer.objects.filter(name_per__icontains=query).values('id',
                                                                                    rating=F('rating_per'),
                                                                                    name=F('name_per'),
                                                                                    image=F('image_per'),
                                                                                    type=Value('performer',
                                                                                               CharField()))
            result = tracks.union(albums, performers)
            result = result.order_by('-rating')
            length = len(tracks)
            try:
                suggest = request.query_params['suggest']
                if suggest != 'false':
                    result = result[:10]
                    length = 10
            except MultiValueDictKeyError:
                pass

            recommended_tracks = TrackRecommendation.filter_query_by_recommendation(user_id=auth.get_user(request),
                                                                                    tracks=tracks, length=length)
            result = list(result)
            i = 0
            for index, res in enumerate(result):
                if res['type'] == 'track':
                    result[index] = recommended_tracks[i]
                    i += 1

            queryset = result

        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(queryset)


class TrackOverview(generics.ListCreateAPIView):
    serializer_class = NoLinkTrackSerializer
    pagination_class = PostLimitOffsetPagination

    def create(self, request, *args, **kwargs):
        album = request.POST["album"]
        audio = request.FILES["track"]
        name = request.POST["track_name"]
        track = save_track(album, name, audio, get_performer(request))
        return Response({"index": request.POST["index"], 'id': track.id}, status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        if type(exc) == ParseError:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exc

    def get_queryset(self):
        try:
            filter = self.request.query_params['filter']
        except MultiValueDictKeyError:
            raise ParseError('Filter param must be set')

        if filter != 'popular':
            TrackOverview.serializer_class = NoLinkTrackSerializer
            TrackOverview.pagination_class = PostLimitOffsetPagination

            request = self.request

            try:
                sort = self.request.query_params['sort']
            except MultiValueDictKeyError:
                sort = 'popularity'

            recommendation_kwargs = {}

            if filter == 'favorite':
                user = auth.get_user(request)
                if type(user) == User:
                    likedtracks = LikedTrack.objects.filter(user_id=user.id).values_list('trc_id').order_by('id')
                    if likedtracks.count() > 0:
                        ordering = 'FIELD(id, %s)' % ','.join(str(id) for id in likedtracks[0])
                        tracks = Track.objects.filter(id__in=likedtracks).extra(
                            select={'ordering': ordering}, order_by=('ordering',))
                    else:
                        tracks = likedtracks
                else:
                    raise ParseError('User must be logged in to access favorite tracks')
            else:
                if filter == 'genre':
                    try:
                        genre = self.request.query_params['genre']
                    except MultiValueDictKeyError:
                        raise ParseError('Filter by genre must have genre param')
                    recommendation_kwargs['genre_id'] = genre

                elif filter == 'style':
                    try:
                        style = self.request.query_params['style']
                    except MultiValueDictKeyError:
                        raise ParseError('Filter by style must have style param')
                    recommendation_kwargs['style_id'] = style

                elif filter == 'all':
                    pass
                else:
                    raise ParseError('Filter value is incorrect')

                if sort == 'time':
                    tracks = TrackRecommendation.get_recommendation(auth.get_user(request), limit=60,
                                                                    **recommendation_kwargs)
                elif sort == 'popularity':
                    tracks = TrackRecommendation.get_recommendation(auth.get_user(request), limit=12, interval=1,
                                                                    **recommendation_kwargs)
                    id_tracks1 = TrackRecommendation.get_recommendation(auth.get_user(request), limit=12, interval=7,
                                                                        **recommendation_kwargs, added_tracks=tracks)
                    tracks.extend(id_tracks1)
                    id_tracks2 = TrackRecommendation.get_recommendation(auth.get_user(request), limit=12, interval=30,
                                                                        **recommendation_kwargs, added_tracks=tracks)

                    tracks.extend(id_tracks2)
                    id_tracks3 = TrackRecommendation.get_recommendation(auth.get_user(request), limit=60-len(tracks),
                                                                        **recommendation_kwargs, added_tracks=tracks)
                    tracks.extend(id_tracks3)
                else:
                    raise ParseError('Incorrect value of the sort parameter')
            return tracks

        else:
            try:
                limit = self.request.query_params['limit']
                interval = self.request.query_params['interval']
            except MultiValueDictKeyError:
                raise ParseError('Filter by popularity requires limit and interval params')
            TrackOverview.serializer_class = TopTrackSerializer
            TrackOverview.pagination_class = None
            tracks = Track.objects.order_by('-rating_trc').filter(
                date_trc__gte=date.today() - timedelta(days=int(interval)))[:int(limit)]
            return tracks


class TrackDetail(APIView):
    def get_next(self, user):
        try:
            recommendations = TrackRecommendation.get_recommendation(user, limit=1)
            if len(recommendations) != 0:
                track = Track.objects.get(id=recommendations[0].id)
            else:
                track = Track.objects.get(id=1)
            # TrackHistoryMethods.create(track.id, user)
            return track
        except Track.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if re.fullmatch(r'[0-9]+', pk):
            track = self.get_object(pk)
        elif pk == 'next':
            track = self.get_next(auth.get_user(request))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            trc_plays = TrackPlaysAmount.objects.get(trc_id=track, date=date.today())
        except TrackPlaysAmount.DoesNotExist:
            trc_plays = TrackPlaysAmount.objects.create(trc_id=track)
        trc_plays.amount += 1
        trc_plays.save()
        user_id = auth.get_user(request)
        serializer = TrackSerializer(track)
        is_liked = LikedTrackMethods.check_if_liked(user_id, track.id)
        data = dict(serializer.data)
        data["is_liked"] = is_liked
        if is_liked:
            liked_track = LikedTrack.objects.get(user_id=user_id, trc_id=track.id)
            liked_track.plays_amount += 1
            liked_track.save()
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete = TrackMethods.delete(pk, auth.get_user(request).id)
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AlbumsList(APIView):

    def get(self, request, format=None):
        try:
            sort = request.query_params['sort']
        except MultiValueDictKeyError:
            sort = 'new'
        try:
            performer = request.query_params['performer']
            albums = Album.objects.filter(per_id=performer)
        except MultiValueDictKeyError:
            albums = Album.objects.all()

        if sort == 'new':
            albums = albums.order_by('-date_alb')
        elif sort == 'popular':
            albums = Album.objects.all().order_by('-rating_alb')
        else:
            return Response('Incorrect sort key value', status=status.HTTP_400_BAD_REQUEST)
        ser = AlbumSerializer(albums, many=True)
        for datum in ser.data:
            is_liked = LikedAlbumMethods.check_if_liked(auth.get_user(request), datum['id'])
            datum.__setitem__('is_liked', is_liked)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, request):
        album_name = request.POST["name"]
        gen_id = request.POST["gen_id"]
        description = request.POST["description"]
        try:
            photo = request.FILES["photo"]
        except MultiValueDictKeyError:
            photo = None
        album = save_album(performer=get_performer(request), name=album_name, genre=gen_id, logo=photo,
                           description=description)
        return Response({"alb_id": album.id}, status=status.HTTP_201_CREATED)


class AlbumDetail(APIView):

    def get(self, request, pk):
        try:
            albums = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return Response('Wrong album id', status=status.HTTP_400_BAD_REQUEST)
        ser = AlbumTracksSerializer(albums)

        data = ser.data
        is_liked = LikedAlbumMethods.check_if_liked(auth.get_user(request), pk)
        data.__setitem__('is_liked', is_liked)
        for datum in data['tracks']:
            is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request), datum['id'])
            datum.__setitem__('is_liked', is_liked)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete = AlbumMethods.delete(pk, auth.get_user(request).id)
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AlbumLikes(APIView):

    def get(self, request):
        try:
            performer = request.query_params['performer']
            try:
                user_id = Performer.objects.get(pk=performer).user_id
            except Performer.DoesNotExist:
                raise ParseError('Incorrect performer id')
        except MultiValueDictKeyError:
            user_id = auth.get_user(request)
            if type(user_id) != User:
                raise ParseError('User must be logged in')
        albums = LikedAlbum.objects.filter(user_id=user_id)
        ser = LikedAlbumSerializer(albums, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def get_album(self, request):
        try:
            album = request.query_params['album']
            return Album.objects.get(pk=album)
        except Album.DoesNotExist:
            raise ParseError('Wrong album id')
        except MultiValueDictKeyError:
            raise ParseError('Album id must be specified')

    def handle_exception(self, exc):
        if type(exc) == ParseError:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exc

    def post(self, request):
        album = self.get_album(request)
        user = auth.get_user(request)
        if type(user) == User:
            LikedAlbum.objects.create(album_id=album, user_id=user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ParseError('User must be logged in')

    def delete(self, request):
        album = self.get_album(request)
        user = auth.get_user(request)
        if type(user) == User:
            try:
                LikedAlbum.objects.get(album_id=album, user_id=user).delete()
            except LikedAlbum.DoesNotExist:
                return ParseError('Like instance was not found')
            return Response(status=status.HTTP_200_OK)
        else:
            return ParseError('User must be logged in')


class PlaylistsList(APIView):

    def get(self, request, format=None):
        try:
            track = request.query_params['track']
        except MultiValueDictKeyError:
            track = None
        try:
            performer = request.query_params['performer']
            if track is None:
                playlists = Playlist.objects.filter(per_id=performer)
                ser = PlaylistSerializer(playlists, many=True)
                data = ser.data
                for datum in data:
                    is_liked = LikedPlaylistMethods.check_if_liked(auth.get_user(request), datum['id'])
                    datum.__setitem__('is_liked', is_liked)
            else:
                playlists = PlaylistTrack.objects.filter(trc_id=track, playlist__per_id=performer)
                ser = PlaylistTrcSerializer(playlists, many=True)

            return Response(ser.data, status=status.HTTP_200_OK)

        except MultiValueDictKeyError:
            return Response('Performer param must be set', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        title = request.POST["title"]
        try:
            image = request.FILES["image"]
        except MultiValueDictKeyError:
            image = None
        save_playlist(get_performer(request), title, image)
        return Response(status=status.HTTP_201_CREATED)


class PlaylistDetail(APIView):

    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response('Wrong album id', status=status.HTTP_400_BAD_REQUEST)
        ser = PlaylistTracksSerializer(playlist)
        data = ser.data
        is_liked = LikedPlaylistMethods.check_if_liked(auth.get_user(request), pk)
        data.__setitem__('is_liked', is_liked)
        for datum in data['tracks']:
            is_liked = LikedTrackMethods.check_if_liked(auth.get_user(request), datum['track']['id'])
            datum['track'].__setitem__('is_liked', is_liked)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        delete = PlaylistMethods.delete(pk, get_performer(request))
        if delete:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PlaylistTrackView(APIView):

    '''def get(self, request):
        try:
            track = request.query_params['track']
        except MultiValueDictKeyError:
            return Response('Track param must be set', status=status.HTTP_400_BAD_REQUEST)
        try:
            performer = request.query_params['performer']
        except MultiValueDictKeyError:
            return Response('Performer param must be set', status=status.HTTP_400_BAD_REQUEST)

        playlists = PlaylistTrack.objects.filter(trc_id=track, playlist__per_id=performer)
        ser = PlaylistTrcSerializer(playlists, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)'''

    def post(self, request):
        try:
            playlist = request.query_params['playlist']
            playlist = Playlist.objects.get(pk=playlist, per_id=get_performer(request))
        except Album.DoesNotExist:
            return Response('Wrong playlist id or doesnt belong to the user', status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            return Response('Playlist id must be specified', status=status.HTTP_400_BAD_REQUEST)
        try:
            track = request.query_params['track']
            trc = Track.objects.get(pk=track)
        except MultiValueDictKeyError:
            return Response('Track id must be specified', status=status.HTTP_400_BAD_REQUEST)
        except Track.DoesNotExist:
            return Response('Invalid track id', status=status.HTTP_400_BAD_REQUEST)
        try:
            PlaylistTrack.objects.get(trc_id=trc, playlist=playlist)
            return Response('Track already in playlist', status=status.HTTP_400_BAD_REQUEST)
        except PlaylistTrack.DoesNotExist:
            PlaylistTrack.objects.create(playlist=playlist, trc_id=trc)
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        try:
            playlist = request.query_params['playlist']
            playlist = Playlist.objects.get(pk=playlist, per_id=get_performer(request))
        except Playlist.DoesNotExist:
            return Response('Wrong playlist id or doesnt belong to the user', status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            return Response('Playlist id must be specified', status=status.HTTP_400_BAD_REQUEST)
        try:
            track = request.query_params['track']
            trc = Track.objects.get(pk=track)
        except MultiValueDictKeyError:
            return Response('Track id must be specified', status=status.HTTP_400_BAD_REQUEST)
        except Track.DoesNotExist:
            return Response('Invalid track id', status=status.HTTP_400_BAD_REQUEST)
        try:
            pt = PlaylistTrack.objects.get(trc_id=trc, playlist=playlist)
            pt.delete()
            return Response(status=status.HTTP_200_OK)
        except PlaylistTrack.DoesNotExist:
            return Response('Track is not in this playlist', status=status.HTTP_400_BAD_REQUEST)


class PlaylistLikes(APIView):

    def get(self, request):
        try:
            performer = request.query_params['performer']
            try:
                user_id = Performer.objects.get(pk=performer).user_id
            except Performer.DoesNotExist:
                raise ParseError('Incorrect performer id')
        except MultiValueDictKeyError:
            user_id = auth.get_user(request)
            if type(user_id) != User:
                raise ParseError('User must be logged in')
        playlists = LikedPlaylist.objects.filter(user_id=user_id)
        ser = LikedPlaylistSerializer(playlists, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def get_playlist(self, request):
        try:
            playlist = request.query_params['playlist']
            return Playlist.objects.get(pk=playlist)
        except Playlist.DoesNotExist:
            raise ParseError('Wrong playlist id')
        except MultiValueDictKeyError:
            raise ParseError('Playlist id must be specified')

    def handle_exception(self, exc):
        if type(exc) == ParseError:
            return Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exc

    def post(self, request):
        playlist = self.get_playlist(request)
        user = auth.get_user(request)
        if type(user) == User:
            LikedPlaylist.objects.create(playlist_id=playlist, user_id=user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ParseError('User must be logged in')

    def delete(self, request):
        playlist = self.get_playlist(request)
        user = auth.get_user(request)
        if type(user) == User:
            try:
                LikedPlaylist.objects.get(playlist_id=playlist, user_id=user).delete()
            except LikedPlaylist.DoesNotExist:
                return ParseError('Like instance was not found')
            return Response(status=status.HTTP_200_OK)
        else:
            return ParseError('User must be logged in')


@api_view(['GET'])
def genre(request):
    if request.method == "GET":
        try:
            gen_id = request.query_params['id']
        except MultiValueDictKeyError:
            gen_id = None
        if gen_id is None or gen_id == '':
            genres = GenreMethods.get()
            serializer = GenreSerializer(genres, many=True)
        else:
            styles = GenreStyleMethods.get(gen_id)
            serializer = GenreStyleSerializer(styles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PerformersList(APIView):

    def get(self, request, format=None):
        try:
            limit = request.query_params['limit']
        except MultiValueDictKeyError:
            limit = 5
        performer = Performer.objects.order_by('-rating_per')[:int(limit)]
        serializer = PerformerSerializer(performer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PerformerDetail(APIView):
    def get_object(self, pk):
        try:
            return Performer.objects.get(pk=pk)
        except Performer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if re.fullmatch(r'[0-9]+', pk):
            performer = self.get_object(pk)
            serializer = FullPerformerSerializer(performer)
            '''for album in serializer.data["albums"]:
                for track in album["tracks"]:
                    track["likes"] = LikedTrackMethods.likesAmount(track["id"])'''
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):  # изменение исполнителя
        name = request.POST["name"]
        try:
            label = request.FILES["label"]
        except MultiValueDictKeyError:
            label = None
        description = request.POST["description"]
        performer = get_performer(request)
        if performer.id == int(pk):
            save_performer(name, label, description, performer)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response('Specified performer doesnt belong to the user', status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET'])
def history(request):
    if request.method == 'PUT':
        result = TrackHistoryMethods.create(request.query_params['track_id'], auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        user = auth.get_user(request)
        if type(user) == User:
            tracks = TrackHistoryMethods.get(user.id)
            serializer = TrackHistorySerializer(tracks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('User must be logged in to access this method', status=status.HTTP_400_BAD_REQUEST)


'''@api_view(['PUT'])
def report(request):
    if request.method == 'PUT':
        track = request.query_params['track']
        result = TrackReportMethods.create(track, auth.get_user(request).id)
        if result:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)'''


@api_view(['POST', 'GET'])
def login(request):
    if request.method == 'GET':
        performer = get_performer(request)
        return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            performer = get_performer(request)
            return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username, '1@1.ru', password).save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        performer = PerformerMethods.create(auth.get_user(request).id, username, '')
        return Response({'username': auth.get_user(request).username, 'per_id': performer.id}, status=status.HTTP_200_OK)
