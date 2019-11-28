from django import forms


class Connexion(forms.Form):
    identifiant = forms.CharField(label="identifiant", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class Creation(forms.Form):
    last_name = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={"class":""}))
    first_name = forms.CharField(label="Prénom", max_length=100)
    Username = forms.CharField(label="Pseudo", max_length=100)
    email = forms.EmailField(label="email")
    confirm_password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput())
    password = forms.CharField(label="Confirmation mot de passe", widget=forms.PasswordInput())
