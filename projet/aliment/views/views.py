from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from aliment.models import Aliment, Categorie


@login_required(login_url="/user/")
def index(request):

    return render(request, "aliment/index.html")


def detail(request, aliment_id):
    aliment = get_object_or_404(Aliment, pk=aliment_id)

    cat = aliment.categorie.values_list("pk", flat=True)
    aliments_same_categorie = Aliment.objects.filter(categorie__pk__in=cat).order_by('note_nutritionelle')[:6]

    return render(
        request,
        "aliment/detail.html",
        {"aliment": aliment, "substitute": aliments_same_categorie},
    )


def substitute(request, aliment_id):
    alm = get_object_or_404(Aliment, pk=aliment_id)
    request.user.aliment.add(alm)
    return render(request, "aliment/index.html")

def delete_aliment_of_user(request, aliment_id):
    alm = get_object_or_404(Aliment, pk=aliment_id)
    request.user.aliment.remove(alm)
    return render(request, "aliment/index.html")