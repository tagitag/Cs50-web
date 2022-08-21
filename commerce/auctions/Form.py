from logging import PlaceHolder
from django import forms

CATAGORIES = ["Old", "New", "Hip", "Fresh",
              "Arcaine", "Dwarven", "No Category"]


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    # description = forms.CharField(widget=forms.Textarea(attrs={'name': 'dis'}))
    startBid = forms.IntegerField(
        max_value=999999)
    imageUrl = forms.URLField()
    #catagory = forms.Select(catagories=CATAGORIES)


class ListPageForm(forms.Form):
    bid = forms.IntegerField(max_value=999999)
