from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from aliment.models import Aliment, Categorie
from .forms import Add_categorie, CatFormSet


def index(request):
    categories = Categorie.objects.all()
    return render(
        request,
        "admin/insertion_categorie.html",
        {"cat_list": categories},
    )

### old way sans passer le form par la vue au template (ca marche mais c'est pas charli)
def add_cat(request):
    dictotest ={}
    cat = []
    categories = Add_categorie(request.POST or None)
    if request.method == "POST":
        if categories.is_valid():
            for item in categories.cleaned_data['cat']:
                cat_object = get_object_or_404(Categorie, pk = item)
                cat.append(cat_object)
            dictotest['cat'] = cat
            dictotest['nombre'] = categories.cleaned_data['nombre']
            return render(
                request,
                "admin/success.html",
                dictotest,
            )



### good way to do it
def manage_cat(request):
    nbr_alm_import = 0
    if request.method == "POST":
        formset = CatFormSet(data=request.POST)

        if formset.is_valid():
            for form in formset:
                try:
                    if form.cleaned_data['insert']:
                        cat = Categorie.objects.get(nom=form.cleaned_data['nom'])
                        if cat.insert == False:
                            nbr_alm_import = nbr_alm_import + cat.import_cat()
                            print("\n\n\n NOMBRE D'ALIMENTs IMPORTéS:")
                            print(cat.nom)
                            print(nbr_alm_import)
                            form.save()

                except KeyError as e:
                    print(e)

        else:
            print(formset.errors)
            nbr_alm_import = -1

    else:
        cat= Categorie.objects.filter(insert=False)
        formset=CatFormSet(queryset=cat)
        nbr_alm_import = -1
    return render(request, 'admin/manage_cat.html', {'formset':formset, 'nbr_alm': nbr_alm_import})



def categorie_search(request):
    element_search = request.GET.get('select_categorie', None)
    coresponding_categories = Categorie.objects.filter(nom__icontains=element_search)
    name_list = []
    for el in list(coresponding_categories):
        name_list.append(el.nom)
    data = {
        'name_list': name_list
    }
    return JsonResponse(data)