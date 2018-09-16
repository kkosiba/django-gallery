from django.urls import path

from .views import (
    PictureCreate,
    PictureSearch,
    PicturesByAlbum,
    PicturesByTags,
    Albums,
    PictureDetails,
    PictureDelete,
    PictureUpdate,
    AlbumCreate,
    AlbumDelete,
    AlbumUpdate,
    )

app_name = 'gallery'

urlpatterns = [
	path('', Albums.as_view(), name='albums'),
    path('add/', PictureCreate.as_view(), name='create_picture'),
    path('search/', PictureSearch.as_view(), name='search'),
    path('tags/<str:tag_name>/', PicturesByTags.as_view(), name='tag_name'),

    path('albums/add/', AlbumCreate.as_view(), name='create_album'),
    path('albums/<str:album_name>/',
        PicturesByAlbum.as_view(), name='single_album'),
    path('albums/<str:album_name>/delete/',
        AlbumDelete.as_view(), name='delete_album'),
    path('albums/<str:album_name>/update/',
        AlbumUpdate.as_view(), name='update_album'),

    path('<int:pk>/', PictureDetails.as_view(), name='single_picture'),
    path('<int:pk>/delete/', PictureDelete.as_view(), name='delete_picture'),
    path('<int:pk>/update/', PictureUpdate.as_view(), name='update_picture'),
]