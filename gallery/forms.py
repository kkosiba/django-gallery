from django import forms
from .models import Album, Picture


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "required": True,
                    "placeholder": "Album's name...",
                }
            )
        }


class UploadPictureForm(forms.Form):
    album = forms.ModelChoiceField(
        queryset=Album.objects, empty_label="Select album", label="Album"
    )
    picture = forms.ImageField(
        label="Pictures",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )


class UpdatePictureForm(forms.Form):
    album = forms.ModelChoiceField(
        queryset=Album.objects, empty_label="Select album", label="Album"
    )
    picture = forms.ImageField(label="Picture")
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={}))
    tags = forms.CharField(label="Tags")
