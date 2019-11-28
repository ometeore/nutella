from django import forms


class RechercheAliment(forms.Form):
    element_search = forms.CharField(label="", max_length=100)
