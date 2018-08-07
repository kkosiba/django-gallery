from django.shortcuts import render
from django.utils import timezone

from .models import Category, Picture

# class based views
from django.views.generic.edit import (
    CreateView, DeleteView,
    UpdateView, FormView)

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

# complex lookups (for searching)
from django.db.models import Q

# Create your views here.

class Index(ListView):
    pass


class SignUp(TemplateView):
    pass


class About(TemplateView):
    pass


class PictureCreate(CreateView):
    pass


class PictureSearch(ListView):
    pass


class ListPicturesByAuthor(ListView):
    pass


class ListCategories(ListView):
    pass


class PictureDetails(DetailView):
    pass


class PictureDelete(DeleteView):
    pass


class PictureUpdate(UpdateView):
    pass
