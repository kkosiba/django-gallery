from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db import transaction

from django.contrib.auth.models import User
from .models import Profile
from .forms import CreatePictureForm
from .forms import UserForm, ProfileForm, SignUpForm

from .models import Category, Picture

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
    paginate_by = 50
    ordering = ('-published_date', )
    

class SignUp(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class About(TemplateView):
    template_name = 'gallery/about.html'


class PictureCreate(LoginRequiredMixin, CreateView):
    model = Picture
    form_class = CreatePictureForm


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
                Q(category__name__icontains=search_query) |
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


class ListCategories(ListView):
    pass


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