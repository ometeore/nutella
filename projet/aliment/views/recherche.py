from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from aliment.models import Aliment
from utilisateur.models import MyUser
from .forms import RechercheAliment


def index(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RechercheAliment(request.POST)
        print(form)
        if form.is_valid():
            aliment_search_list = Aliment.objects.filter(
                nom__icontains = request.POST["element_search"]
            )
            context = {
                "latest_aliment_list": aliment_search_list,
            }

            if(list(aliment_search_list) == []):
                return render(request, "layouts/main.html", {"form": form})
            else:
                return render(request, "aliment/recherche.html", context)
        else:
            return render(request, "layouts/main.html", {"form": form})


    else:
        return render(request, "aliment/index.html")


def validate_search(request):
    element_search = request.GET.get('element_search', None)
    data = {
        'is_taken': Aliment.objects.filter(nom__icontains=element_search).exists()
    }
    return JsonResponse(data)




def detail(request, aliment_id):
    aliment = get_object_or_404(Aliment, pk=aliment_id)
    return render(request, "aliment/detail.html", {"aliment": aliment})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
