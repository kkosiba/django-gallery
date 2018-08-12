from django.urls import path

# for restricting access to post related actions
from django.contrib.auth.decorators import login_required

from .views import (
    Index,
    PictureCreate,
    PictureSearch,
    ListPicturesByAuthor,
    ListCategories,
    PictureDetails,
    PictureDelete,
    PictureUpdate,
    )

app_name = 'gallery'

urlpatterns = [
	path('', Index.as_view(), name='index'),
    path('add/', PictureCreate.as_view(), name='create_picture'),
    path('search/', PictureSearch.as_view(), name='search'),
    path('author/<str:author>/',
         ListPicturesByAuthor.as_view(), name='author'),
    path('categories/', ListCategories.as_view(), name='categories'),
    path('<int:pk>/', PictureDetails.as_view(), name='single_picture'),
    path('<int:pk>/delete/', PictureDelete.as_view(), name='delete_picture'),
    path('<int:pk>/update/', PictureUpdate.as_view(), name='update_picture'),
]