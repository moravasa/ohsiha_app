from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import HomeForm
from .models import Kysymys
from .models import Juna, Asetukset
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import django.http


def HomePageView(request):
    return render(request, 'index.html', {})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class TestPageView(TemplateView):
    template_name = 'kantatesti.html'
    
    def get(self, request):
        form = HomeForm()
        vierailijat = Kysymys.objects.all().order_by('-pvm')
        
        args = {'form': form, 'vierailijat': vierailijat}
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            form.save()
            text = form.cleaned_data['syote']
            form = HomeForm()
            return redirect(self.request.path_info)

        args = {'form': form, 'text':text}
        return render(request, self.template_name, args)

@login_required(login_url='/login/')
def PalveluView(request):
    template_name = 'palvelu.html'
    junat = Juna.objects.all()
    settings = Asetukset.objects.filter(SettingName='junadataUpdated')
    args = {'junat': junat, 'settings': settings}
    return render(request, template_name, args)


