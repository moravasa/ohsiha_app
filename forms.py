from django import forms
from ohsiha_app.models import Kysymys

class HomeForm(forms.ModelForm):
    class Meta:
        model = Kysymys
        fields = ('syote',)
        labels = {'syote':'Nimimerkki'}

