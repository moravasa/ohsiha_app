from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Avg
import django.http
import requests


# Create your views here.
from .forms import HomeForm
from .models import Kysymys
from .models import Juna, Asetukset


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
    tmp_saa = haeSaatiedot('Tampere')
    hki_saa = haeSaatiedot('Helsinki')
    junat = Juna.objects.all()
    settings = Asetukset.objects.filter(SettingName='junadataUpdated')
    kpi_1_int = int(round(KPI_pros_ajoissa()))
    # Highchart haluaa datat listamuodossa ==> lisätään KPI:t listoihin
    kpi_1 = []
    kpi_1.append(kpi_1_int)
    KPI_keskim_myohastyminen()
    kpi_2_int = KPI_keskim_myohastyminen()
    kpi_2 = []
    kpi_2.append(kpi_2_int)
    args = {'junat': junat, 'settings': settings, 'saa_tre': tmp_saa, 'saa_hki': hki_saa, 'kpi_1': kpi_1, 'kpi_2': kpi_2}
    return render(request, template_name, args)

def haeSaatiedot(kaupunki):
    """ Hakee parametrina annetun kaupungin säätiedot
        OpenWeatherMap API:sta
    """
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + kaupunki + '&units=metric&appid=725e727e28f70ccc71a72a225ccbf4c7'
    vastaus = requests.get(url).json()
    
    saatiedot = {
        'kaupunki': kaupunki,
        'lampotila': "{:.0f}".format(vastaus['main']['temp']),
        'tuuli': vastaus['wind']['speed'],
   #     'tuuli_suunta': vastaus['wind']['deg'],
        'saa_kuvaus': vastaus['weather'][0]['description'],
        'kuvake': vastaus['weather'][0]['icon']
    }

    return saatiedot

def KPI_pros_ajoissa():
    junat_kaikki = Juna.objects.count()
    junat_myohassa = Juna.objects.filter(junaMyohassa='True').count()
    return (100-float(junat_myohassa / junat_kaikki) * 100)

def KPI_keskim_myohastyminen():
    keskiarvo = Juna.objects.filter(junaMyohassa='True').aggregate(Avg('junaMyohassaMin'))
    # ^^ palauttaa dictin
    keskiarvo_int = int(round(keskiarvo['junaMyohassaMin__avg']))
    return keskiarvo_int

