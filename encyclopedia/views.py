import markdown2
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label = '', widget = forms.TextInput(attrs = {"placeholder": "Search Encyclopedia"}))

class NewPageForm(forms.Form):
    new_title = forms.CharField(label = "", widget = forms.TextInput(attrs = {"placeholder": "Title"}))
    new_text = forms.CharField(label = "", widget = forms.Textarea(attrs={"placeholder": "Description"}))
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm(),
            "error": "Your requested page wasn't found!"
        })
    else:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/title.html", {
        "entries": entry,
        "page_title": title,
        "form": SearchForm()
        })

def search(request):
    entries = util.list_entries()
    find_entries = list()

    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["q"]
        
        for entry in entries:
            if query.upper() == entry.upper():
                return HttpResponseRedirect(f'/wiki/{query}')

            if query.upper() in entry.upper():
                find_entries.append(entry)
        
        if find_entries:
            return render(request, "encyclopedia/search.html", {
                "search_results": find_entries,
                "form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "no_result": f"No results for {query}",
                "form": SearchForm()
            })

def new_page(request):
    if request.method == "POST":
        form_new = NewPageForm(request.POST)

        if form_new.is_valid():
            entries = util.list_entries()
            title = form_new.cleaned_data["new_title"]

            for entry in entries:
                if entry.upper() == title.upper():
                    return render(request, "encyclopedia/error.html", {
                        "form": SearchForm(),
                        "error": "Your title already exists!"
                    }) 
            else:
                content = form_new.cleaned_data["new_text"]
                save = util.save_entry(title, content)
                return HttpResponseRedirect(f'/wiki/{title}')
            
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": SearchForm(),
            "form_new": NewPageForm()
        })

def edit_page(request, page_title):
    content = util.get_entry(page_title)

    if request.method == "GET":
        return render(request, "encyclopedia/edit_page.html", {
            "title": page_title,
            "content": content,
            "form": SearchForm(),
        })

    else:
        edited = request.POST["edited"]
        util.save_entry(page_title, edited)
        return HttpResponseRedirect(f'/wiki/{page_title}')

def random_page(request):
    entries = util.list_entries()
    page_title = random.choice(entries)
    return HttpResponseRedirect(f'/wiki/{page_title}')