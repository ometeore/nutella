from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from aliment.models import Question, Aliment


def index(request):
    latest_aliment_list = Aliment.objects.order_by("id")[:5]
    context = {
        "latest_aliment_list": latest_aliment_list,
    }
    return render(request, "aliment/index.html", context)
