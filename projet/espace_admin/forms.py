from django import forms
from django.forms import modelformset_factory, ModelForm 
from aliment.models import Categorie


CATEGORIES = []
categories = Categorie.objects.all()
for cat in categories:
    tuple_temp = (cat.pk ,cat.nom)
    CATEGORIES.append(tuple_temp)



class Add_categorie(forms.Form):
    cat = forms.MultipleChoiceField(
        widget  = forms.CheckboxSelectMultiple,
        choices = CATEGORIES,
    )
    nombre = forms.IntegerField(min_value = 1)
    datatable_categorie_length = forms.IntegerField()

class AddCategorie(forms.ModelForm):
    #C'ets ici que je peux désactiver l'input de name

    class Meta:
        model = Categorie
        exclude = ()

        help_texts = {
            'nom': ('Some useful help text.'),
        }
        error_messages = {
            'nom': {
                'max_length': ("This writer's name is too long."),
            },
        }

CatFormSet = modelformset_factory(Categorie, form=AddCategorie)


##### https://micropyramid.com/blog/understanding-djangos-model-formsets-in-detail-and-their-advanced-usage/

#class UserForm(forms.ModelForm):
#
#    birth_date = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickSeconds": False}))
#    class Meta:
#        model = User
#        exclude = ()
#
#    def __init__(self, *args, **kwargs):
#        self.businessprofile_id = kwargs.pop('businessprofile_id')
#        super(UserForm, self).__init__(*args, **kwargs)
#
#        self.fields['user_group'].queryset = Group.objects.filter(business_profile_id = self.businessprofile_id)
#
#BaseUserFormSet = modelformset_factory(User, form=UserForm, extra=1, can_delete=True)
#
#class UserFormSet(BaseUserFormSet):
#
#    def __init__(self, *args, **kwargs):
#        #  create a user attribute and take it out from kwargs
#        # so it doesn't messes up with the other formset kwargs
#        self.businessprofile_id = kwargs.pop('businessprofile_id')
#        super(UserFormSet, self).__init__(*args, **kwargs)
#        for form in self.forms:
#            form.empty_permitted = False
#
#    def _construct_form(self, *args, **kwargs):
#        # inject user in each form on the formset
#        kwargs['businessprofile_id'] = self.businessprofile_id
#        return super(UserFormSet, self)._construct_form(*args, **kwargs)