from django.urls import path
from .views import *

app_name = "gallery"

urlpatterns = [
    path("", Albums.as_view(), name="albums"),
    path("search/", PictureSearch.as_view(), name="search"),
    path("tags/<str:tag_name>/", PicturesByTags.as_view(), name="tag_name"),
    # all albums
    path("albums/", Albums.as_view(), name="albums"),
    # add new album
    path("albums/add/", AlbumCreate.as_view(), name="create_album"),
    # pictures by album
    path("albums/<str:album_name>/", PicturesByAlbum.as_view(), name="single_album"),
    # upload pictures to album album_name
    path(
        "albums/<str:album_name>/upload/",
        PictureUpload.as_view(),
        name="upload_pictures",
    ),
    # delete album album_name
    path("albums/<str:album_name>/delete/", AlbumDelete.as_view(), name="delete_album"),
    # update name of the album album_name
    path("albums/<str:album_name>/update/", AlbumUpdate.as_view(), name="update_album"),
    # single picture
    path(
        "albums/<str:album_name>/<int:pk>/",
        PictureDetails.as_view(),
        name="single_picture",
    ),
    # delete single picture
    path(
        "albums/<str:album_name>/<int:pk>/delete/",
        PictureDelete.as_view(),
        name="delete_picture",
    ),
    # update single picture
    path(
        "albums/<str:album_name>/<int:pk>/update/",
        PictureUpdate.as_view(),
        name="update_picture",
    ),
]
