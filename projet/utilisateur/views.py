from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from utilisateur.models import MyUser
from .forms import Connexion, Creation
import logging

LOGGER=logging.getLogger(__name__)

def connexion(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = Connexion(request.POST)
        # check whether it's valid:
        if form.is_valid():
            identifiant = form.cleaned_data["identifiant"]
            mdp = form.cleaned_data["password"]
            user = authenticate(username=identifiant, password=mdp)

            LOGGER.info("le mot de passe" + mdp)
            LOGGER.warn("le mot de passe" + mdp)
            
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return HttpResponseRedirect("/user/")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Connexion()

    return render(request, "user/connexion.html", {"form": form})


def mon_compte(request):
    return render(request, "user/mon_compte.html")

def create(request):
    form = Creation(request.POST)
    if form.is_valid():
        if form.cleaned_data["confirm_password"] == form.cleaned_data["password"]:
            user = MyUser.objects.create_user(form.cleaned_data["Username"])
            user.set_password(form.cleaned_data["password"])
            user.last_name = form.cleaned_data["last_name"]
            user.first_name = form.cleaned_data["first_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            return render(request, "layouts/main.html")
        else:
            render(request, "user/creation.html", {"form": form})
    return render(request, "user/creation.html", {"form": form})


def deconnexion(request):
    logout(request)
    return redirect("/")

def mention_legale(request):
    return render(request, "mention_legales/mention_legales.html")
