from logging import PlaceHolder
from django import forms

class NewPage (forms.Form):
    entryTitle = forms.CharField (
        label="Entry Title",
        required= True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the title here.', "class" : "textbox", "autocomplete" : "off"}),
        max_length="255",
        help_text= "You can only enter 255 characters max."
        )
    entryContent = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'placeholder': 'Enter Content for the wiki entry.'}),
        required= True,
        min_length= "10",
        max_length= "2097152",
        help_text= "You must enter 10 Characters minimum."
        )

class editPage (forms.Form):
    entryContent = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'placeholder': 'Enter Content for the wiki entry.'}),
        required= True,
        min_length= "10",
        max_length= "2097152",
        help_text= "You must enter 10 Characters minimum."
        )