from django.contrib.auth.views import (
    login, logout,
    )
from django.urls import path

# for restricting access to post related actions
from django.contrib.auth.decorators import login_required

from .views import (
    Index,
    SignUp,
    About,
    PictureCreate,
    PictureSearch,
    ListPicturesByAuthor,
    ListCategories,
    PictureDetails,
    PictureDelete,
    PictureUpdate
    )

app_name = 'gallery'

urlpatterns = [
	path('', Index.as_view(), name='index'),

	# user management
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),

    path('about/', About.as_view(), name='about'),

    path('add/',
    	 login_required(PictureCreate.as_view()), name='create_picture'),
    
    path('search/', PictureSearch.as_view(), name='search'),
    
    path('author/<str:author>/',
         ListPicturesByAuthor.as_view(), name='author'),

    path('category/', ListCategories.as_view(), name='all_categories'),

    path('<pk:pk>/', PictureDetails.as_view(), name='single_picture'),
    path('<pk:pk>/delete/',
         login_required(PictureDelete.as_view()), name='delete_picture'),
    path('<pk:pk>/update/',
         login_required(PictureUpdate.as_view()), name='update_picture'),
]