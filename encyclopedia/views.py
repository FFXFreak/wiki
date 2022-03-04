import random

from pdb import post_mortem
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
from . import forms

def index(request):
    """
    Sends a list of wiki entries to index page
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, req_entry):
    """
    finds an entry from the address bar input and converts 
    .md file to HTML using "markdown". If there is no wiki
    page that has been entered the user will get an error message
    """
    markdowner = Markdown()
    if not util.get_entry(req_entry):
        return render(request, "encyclopedia/error.html", {
        'errorTitle' : 'Your request could not be found!',
        'errorContent' : 'Please check the spelling of your request and try again.'
    })

    return render(request, "encyclopedia/entry.html", {
        "req_entry": markdowner.convert(util.get_entry(req_entry)),
        "entry": req_entry
    })

def search(request):
    """
    This function takes any input from the search bar and checks to see if there
    is a wiki entry. If there is it directs the user to the entries function, if 
    it is a partial match it will show the results that it could have been. Otherwise
    we get an error message
    """
    search = request.GET.get('q')
    # here we get a value from get_entry function and check to see if it exists
    check = util.get_entry(search)
    if check:
        return HttpResponseRedirect(reverse("wiki:entry", args=[search]))
    # if it doesnt exist we will now check for a partial match with the search entry function
    results = util.search_entry(search)
    if results:
        return render(request, "encyclopedia/search.html",{
            "results" : results,
            "search" : search
        })
    # if we still don't get a match we send out an error message
    else:
        return render(request, "encyclopedia/error.html", {
        'errorTitle' : 'Your search request could not be found!',
        'errorContent' : 'Please check the spelling of your request and try again.'
    })
        

def newPage(request):
    """
    This function allows the user to create a new wiki page
    """
    if request.method == "POST":
        # when the form is submitted we run the necessary validations on the form
        form = forms.NewPage(request.POST)
        if form.is_valid():
            # here we check if there is already a page with the same name if not we create
            if not util.search_entry(form.cleaned_data["entryTitle"]):
                util.save_entry(form.cleaned_data["entryTitle"], form.cleaned_data["entryContent"])
                return HttpResponseRedirect(reverse("wiki:index"))
        # if there is a page with the same name we send an error message
        return render(request, "encyclopedia/error.html", {
        'errorTitle' : 'There was an error while creating your entry',
        'errorContent' : 'There may already be an entry that matches the title you have provided. Please check and then try again.'
    })
    # this creates a new form for the user to add a wiki page
    return render(request, "encyclopedia/newpage.html",{
            "form" : forms.NewPage()
        })

def editPage(request, req_entry):
    """
    Here we allow the user to edit any wiki page that already exists
    """
    if request.method == "POST":
        # here we do validation checks on the form
        form = forms.editPage(request.POST)
        if form.is_valid():
            # we also check that the page already exists and then we update
            if util.search_entry(req_entry):
                util.save_entry(req_entry, form.cleaned_data["entryContent"])
                return HttpResponseRedirect(reverse("wiki:entry", args=[req_entry]))
        # otherwise we give the user an error message
        return render(request, "encyclopedia/error.html", {
        'errorTitle' : 'There was an error while creating your entry',
        'errorContent' : 'This wiki page no longer exists.'
    })
    # this creates the relevent form and pre-populates with current data
    return render(request, "encyclopedia/editpage.html",{
            "entry" : req_entry,
            "form" : forms.editPage({"entryContent" : util.get_entry(req_entry)})
        })

def randomPage(request):
    """
    This function chooses a random wiki item and displays it
    """
    randomNum = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:entry", args=[randomNum]))