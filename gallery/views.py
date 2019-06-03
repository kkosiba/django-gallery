from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q  # complex lookups (for searching)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
from .models import Album, Picture
from .forms import UploadPictureForm, UpdatePictureForm, AlbumForm

# Create your views here.

## Albums
class Albums(ListView):
    model = Album
    template_name = "gallery/index.html"
    context_object_name = "albums"
    paginate_by = 12


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm

    # To conveniently swap 'Update' and 'Create' in album form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = False
        return context


class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy("gallery:albums")

    """
    To overcome error:
    'Generic detail view AlbumDelete must be called with either an object pk
     or a slug in the URLconf.'
    """

    def get_object(self):
        return get_object_or_404(Album, name=self.kwargs.get("album_name"))


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm

    def get_object(self):
        return get_object_or_404(Album, name=self.kwargs.get("album_name"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


## Pictures
class PictureUpload(LoginRequiredMixin, View):
    form_class = UploadPictureForm
    template_name = "gallery/upload_pictures_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # override post method to upload multiple images
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            for file in form.files.getlist("picture"):
                Picture(
                    album=form.cleaned_data["album"],
                    picture=file,
                    description="Empty description",
                ).save()
            return redirect(
                "gallery:single_album", album_name=self.kwargs.get("album_name")
            )

        return render(request, self.template_name, {"form": form})


class PictureUpdate(LoginRequiredMixin, FormView):
    form_class = UpdatePictureForm
    template_name = "gallery/update_picture_form.html"
    success_url = reverse_lazy("gallery:albums")

    # def get_form(self, form_class):
    #     """
    #     Show the form populated with details from database, let user change them.
    #     """
    #     if form_class is None:
    #         form_class = self.get_form_class()
    #     picture = get_object_or_404(Picture, pk=self.kwargs['pk'])
    #     if picture:
    #         return form_class(instance=picture, **self.get_form_kwargs())
    #     else:
    #         return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        file = request.FILES.get("picture")

        if form.is_valid():
            pic = get_object_or_404(Picture, pk=self.kwargs["pk"])
            pic.album = form.cleaned_data["album"]
            pic.picture = file
            pic.description = form.cleaned_data["description"]
            pic.tags = form.cleaned_data["tags"]
            pic.save()
            return redirect(
                "gallery:single_album", album_name=self.kwargs.get("album_name")
            )

        return render(request, self.template_name, {"form": form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs["album_name"]
        pk = self.kwargs["pk"]
        context["pk"] = pk
        context["picture"] = get_object_or_404(Picture, pk=pk)
        return context


class PictureSearch(ListView):
    model = Picture
    context_object_name = "pictures"
    template_name = "gallery/search_pictures.html"
    paginate_by = 50
    ordering = ("-published_date",)

    def get_queryset(self):
        search_query = self.request.GET.get("q", None)
        results = []
        if search_query:
            results = Picture.objects.filter(
                Q(album__name__icontains=search_query)
                | Q(description__icontains=search_query)
            ).distinct()
        return results


class PicturesByAlbum(ListView):
    context_object_name = "pictures"
    template_name = "gallery/pictures_by_album.html"
    paginate_by = 50
    ordering = ("-published_date",)

    def get_queryset(self):
        album = get_object_or_404(Album, name=self.kwargs["album_name"])
        results = []
        if album:
            results = Picture.objects.filter(album__name=album)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs.get("album_name", None)
        # to be implemented
        context["created"] = 0
        return context


class PicturesByTags(ListView):
    model = Picture
    context_object_name = "pictures"
    template_name = "gallery/pictures_by_tags.html"
    paginate_by = 50
    ordering = ("-published_date",)

    def get_queryset(self):
        tag = self.kwargs.get("tag_name", None)
        results = []
        if tag:
            results = Picture.objects.filter(tags__name=tag)
        return results


class PictureDetails(DetailView):
    model = Picture
    template_name = "gallery/single_picture.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs.get("album_name", None)
        context["pk"] = self.kwargs.get("pk", None)
        return context


class PictureDelete(LoginRequiredMixin, DeleteView):
    model = Picture
    success_url = reverse_lazy("gallery:albums")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs.get("album_name", None)
        context["pk"] = self.kwargs.get("pk", None)
        return context

