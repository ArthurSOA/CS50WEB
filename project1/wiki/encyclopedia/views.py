from http.client import HTTPResponse
from operator import sub
from turtle import ycor
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from markdown import Markdown
from django.urls import reverse
from django import forms
from random import choice
from . import util

class FormAddEntry(forms.Form):
    title = forms.CharField(label = "Entry Title")
    body = forms.CharField(widget = forms.Textarea)
    edit = forms.BooleanField(initial = False, widget=forms.HiddenInput, required= False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request,entry):
    markdown = Markdown()
    page = util.get_entry(entry)
    if util.get_entry(entry):
        return render(request,"encyclopedia/entry.html",{
            "entry":markdown.convert(page),
            "entryTitle": entry
        })
    else:
        return render(request,"encyclopedia/nonExistingPage.html",{
            "entryTitle":entry
        })


def search(request):

    if request.method == "POST":
        search_parameter = request.POST['q']

        if (util.get_entry(search_parameter)):
            return HttpResponseRedirect(reverse("entry",kwargs={'entry': search_parameter}))

        else:
            substrings =[]
            for entry in util.list_entries():
                if search_parameter.upper() in entry.upper():
                    substrings.append(entry)
            return render(request,"encyclopedia/index.html", {
                "entries": substrings,
                "search": True,
                "value": search_parameter
            })

def random(request):
    list_entries = util.list_entries()
    randomEntry = choice(list_entries)

    return HttpResponseRedirect(reverse("entry", kwargs= {'entry': randomEntry}))

def newEntry(request):
    if request.method =="GET":
        return render(request, "encyclopedia/newPage.html")

