from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404

from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator

from django.db import transaction

from django.contrib.auth.models import User
from .models import Profile, Album, Picture
from .forms import CreatePictureForm, AlbumCreateForm
from .forms import UserForm, ProfileForm, SignUpForm

from django.urls import reverse_lazy

# class based views
from django.views.generic.edit import (
    CreateView, DeleteView,
    UpdateView, FormView)

from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# complex lookups (for searching)
from django.db.models import Q

from django.contrib import messages
# Create your views here.

class Index(ListView):
    model = Picture
    template_name = 'gallery/index.html'
    context_object_name = 'pictures'
    paginate_by = 10
    ordering = ('-published_date', )
    

class SignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)


class About(TemplateView):
    template_name = 'gallery/about.html'


class PictureCreate(LoginRequiredMixin, CreateView):
    model = Picture
    form_class = CreatePictureForm

    # to process request.user and all files in the form
    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.author = self.request.user
        files = self.request.FILES.getlist('picture')
        if files:
            for file in files:
                obj = self.model.objects.create(
                    title=form.cleaned_data['title'],
                    picture=file,
                    author=form.instance.author,
                    description=form.cleaned_data['description'])
        return super().form_valid(form)


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumCreateForm

    # to process request user in the form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumDelete(DeleteView):
    pass


class AlbumUpdate(UpdateView):
    pass


class PictureSearch(ListView):
    model = Picture
    context_object_name = 'pictures'
    template_name = 'gallery/search_pictures.html'
    paginate_by = 50
    ordering = ('-published_date',)

    def get_queryset(self):
        search_query = self.request.GET.get('q', None)
        results = []
        if search_query:
            results = Picture.objects.filter(
                Q(album__name__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)).distinct()
        return results


class ListPicturesByAuthor(ListView):
    model = Picture
    context_object_name = 'pictures'
    template_name = 'gallery/pictures_by_author.html'
    paginate_by = 50
    ordering = ('-published_date',)

    def get_queryset(self):
        author = self.kwargs.get('author', None)
        results = []
        if author:
            results = Picture.objects.filter(author__username=author)
        return results


class ListAlbums(ListView):
    model = Album
    template_name = 'gallery/list_albums.html'
    context_object_name = 'albums'
    paginate_by = 10


class ListPicturesByAlbum(ListView):
    model = Picture
    context_object_name = 'pictures'
    template_name = 'gallery/pictures_by_album.html'
    paginate_by = 50
    ordering = ('-published_date',)

    def get_queryset(self):
        album = self.kwargs.get('album_name', None)
        results = []
        if album:
            results = Picture.objects.filter(album__name=album)
        return results


class ListPicturesByTags(ListView):
    model = Picture
    context_object_name = 'pictures'
    template_name = 'gallery/pictures_by_tags.html'
    paginate_by = 50
    ordering = ('-published_date',)

    def get_queryset(self):
        tag = self.kwargs.get('tag_name', None)
        results = []
        if tag:
            results = Picture.objects.filter(
                tags__name=tag)
        return results

class PictureDetails(DetailView):
    model = Picture
    template_name = 'gallery/single_picture.html'


class PictureDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    success_url = reverse_lazy('gallery:index')

    def test_func(self):
        """
        Only let the user delete object if they own the object being deleted
        """
        return self.get_object().author.first_name == self.request.user.first_name


class PictureUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picture
    form_class = CreatePictureForm

    def test_func(self):
        """
        Only let the user update object if they own the object being updated

        """
        return self.get_object().author.first_name == self.request.user.first_name


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })