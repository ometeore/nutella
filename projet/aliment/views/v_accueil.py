from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RechercheAliment


def index(request):
    form = RechercheAliment()
    return render(request, "layouts/main.html", {"form": form})
