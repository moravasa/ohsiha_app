import urllib.request, json
import pytz, parse, pandas as pd
import datetime as dt
import time
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import sys
import os
import django
sys.path.append('/users/sqrl8/documents/ohsiha2019/harkka/ohsiha_django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ohsiha_django.settings'
django.setup()
from ohsiha_app.models import Juna, Asetukset


def vaihdaAikavyohyke(aikaleima):
    """ Vaihtaa aikaleiman UTC-aikavyöhykkeen Suomen aikavyöhykkeelle
        ja palauttaa aikaleiman muodossa pv.kk.vvvv hh:mm
    """
    timezone_org = pytz.timezone("UTC")
    datetime_obj = dt.datetime.strptime(aikaleima, '%Y-%m-%dT%H:%M:%S.000Z')
    datetime_utc = timezone_org.localize(datetime_obj)
    timezone_fi = pytz.timezone("Europe/Helsinki")
    datetime_fi = datetime_utc.astimezone(timezone_fi)

    datetime_fi_formatted = "{:%d.%m.%Y %H:%M}".format(datetime_fi)
    # datetime_django_formatted = "{:%Y-%m-%d %H:%M}".format(datetime_fi)

    return datetime_fi_formatted

def asemanJunatiedot(lahtoAsema, kohdeAsema, aikaikkuna_ennen,
                     aikaikkuna_jalkeen):
    """ Hakee parametrina annettujen lähtö- ja kohdeasemien välillä kulkevien
        junien tiedot. Aikaikkuna-asetuksilla rajataan poimittavien junien
        määrää. Esim. aikaikkuna ennen = kuinka monta minuuttia ennen lähtöä
        juna näytetään. Rajapinnassa aikavälirajoituksen maksimikoko on 24
        tuntia eli 1440 minuuttia.
      
    """
    url = 'https://rata.digitraffic.fi/api/v1/live-trains/station/' + \
          lahtoAsema + '?minutes_before_departure=' + str(aikaikkuna_ennen) + \
          '&minutes_after_departure=' + str(aikaikkuna_jalkeen) + \
          '&minutes_before_arrival=0' + \
          '&minutes_after_arrival=0'

    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode("utf-8"))

        junaTiedot = {}

        for item in data:
            if item['trainType'] in ['IC','S']:
                if onkoOikeaReittiJaSuunta(item['timeTableRows'], lahtoAsema,
                                           kohdeAsema):
                    junaNro = item['trainNumber']
                    junaTyyppi = item['trainType']
                    junaTunnus = junaTyyppi + " " + str(junaNro)

                    junaTiedot[junaTunnus] = {}
                    junaTiedot[junaTunnus]['junaNro'] = junaNro
                    junaTiedot[junaTunnus]['junaTyyppi'] = junaTyyppi
                    junaTiedot[junaTunnus]['junaAsemaKohde'] = kohdeAsema
                    junaTiedot[junaTunnus]['junaAsemaLahto'] = lahtoAsema
                    junaTiedot[junaTunnus]['junaAjossa'] = \
                        item['runningCurrently']
                    lahtoaika, lahtoaika_enn, lahtoaika_tod, myohassa, \
                    myohassa_min = \
                        lahtoAjat(item['timeTableRows'], lahtoAsema)
                    junaTiedot[junaTunnus]['junaLahtoAika'] = lahtoaika
                    junaTiedot[junaTunnus]['junaLahtoAikaArvio'] = lahtoaika_enn
                    junaTiedot[junaTunnus]['junaLahtoAikaTod'] = lahtoaika_tod
                    junaTiedot[junaTunnus]['junaMyohassa'] = myohassa
                    junaTiedot[junaTunnus]['junaMyohassaMin'] = myohassa_min
                    junaTiedot[junaTunnus]['junaPeruttu'] = item['cancelled']

    except Exception as e:
        print("VIRHE: Aikataulutietojen haku epäonnistui!")
        print(e)
        return {}, False

    print("Aikataulutietojen haku OK..")
    return junaTiedot, True

def timeDeltaMinutes(timestamp1, timestamp2):
    """ Palauttaa kahden aikaleiman välisen aikaeron minuutteina
    """

    datetime1 = dt.datetime.strptime(timestamp1, '%Y-%m-%dT%H:%M:%S.000Z')
    datetime2 = dt.datetime.strptime(timestamp2, '%Y-%m-%dT%H:%M:%S.000Z')

    difference = (datetime2 - datetime1).total_seconds()
    difference_in_minutes = difference // 60

    return int(difference_in_minutes)

def lahtoAjat(aikataulu, asema):
    lahtoaika_aikataulu = ""
    lahtoaika_ennuste = ""
    lahtoaika_toteuma = ""
    myohassa = False
    myohassa_min = 0
    MYOHASSA_RAJA_MIN = 2

    for rivi in aikataulu:
        if rivi['stationShortCode'] == asema:
            myohassa_min = 0
            myohassa = False
            lahtoaika_toteuma = ""
            lahtoaika_ennuste = ""
            lahtoaika_aikataulu = vaihdaAikavyohyke(rivi['scheduledTime'])
            
            if 'liveEstimateTime' in rivi.keys():
                lahtoaika_ennuste = vaihdaAikavyohyke(rivi['liveEstimateTime'])
            if 'actualTime' in rivi.keys():
                lahtoaika_toteuma = vaihdaAikavyohyke(rivi['actualTime'])
            if lahtoaika_toteuma != "":
                myohassa_min = timeDeltaMinutes(rivi['scheduledTime'], rivi['actualTime'])
            elif lahtoaika_ennuste != "":
                myohassa_min = timeDeltaMinutes(rivi['scheduledTime'], rivi['liveEstimateTime'])

            if myohassa_min >= MYOHASSA_RAJA_MIN:
                myohassa = True
            else:
                myohassa = False

    return lahtoaika_aikataulu, lahtoaika_ennuste, lahtoaika_toteuma, \
           myohassa, myohassa_min

def onkoOikeaReittiJaSuunta(aikataulu, lahtoasema, kohdeasema):
    lahtoReitilla, lahtoPositio = onkoReitilla(aikataulu, lahtoasema)
    kohdeReitilla, kohdePositio = onkoReitilla(aikataulu, kohdeasema)

    if lahtoReitilla and kohdeReitilla and lahtoPositio < kohdePositio:
        return True
    else:
        return False

def onkoReitilla(aikataulu, asema):
    positio = 0
    asemaReitilla = False

    for rivi in aikataulu:
        if rivi['stationShortCode'] == asema:
            asemaReitilla = True
            break

        positio += 1

    return asemaReitilla, positio


@login_required(login_url='/login/')
def junadataTietokantaan(request):
    """ Hakee junien aikataulutiedot Digitraffic-rajapinnasta ja päivittää
        ne tietokantaan
    """
    print("Tietojen päivitys!")
    # reitti tällä hetkellä kovakoodattuna, voisi parametrisoida
    junaTiedot, luku_ok = asemanJunatiedot('TPE', 'HKI', 300, 1140)
    print("Junatiedot len: " + str(len(junaTiedot)))
    
    if luku_ok and len(junaTiedot) > 0:
        # viedään dictissä olevat junatiedot pandas-dataframeen, jossa
        # niitä on mukavampi käsitellä
        df = pd.DataFrame.from_dict(junaTiedot, orient='index')
        df.index.names = ['junaTunnus']
        df.reindex()
        df = df.sort_values(by=['junaLahtoAika'], ascending=True)

        # tyhjennetään vanhat tiedot tietokantataulusta
        Juna.objects.all().delete()

        # viedään uudet tiedot kantaan
        for row in df.itertuples():
            Juna.objects.create(
                junaTunnus = row.Index,
                junaNro = row.junaNro,
                junaAjossa = row.junaAjossa,
                junaKohdeasema = row.junaAsemaKohde,
                junaLahtoasema = row.junaAsemaLahto,
                junaLahtoaika = row.junaLahtoAika,
                junaLahtoaikaTod = row.junaLahtoAikaTod,
                junaLahtoaikaArvio = row.junaLahtoAikaArvio,
                junaMyohassa = row.junaMyohassa,
                junaMyohassaMin = row.junaMyohassaMin,
                junaPeruttu = row.junaPeruttu
            )
        
        print("debug, inserted data:")
        print(df.loc[:,['junaAsemaLahto', 'junaAsemaKohde', 'junaLahtoAika',
                        'junaLahtoAikaArvio', 'junaLahtoAikaTod',
                        'junaMyohassa', 'junaMyohassaMin']])

        # tallennetaan tietojen päivityshetki tietokantaan
        login_user = request.user.username    
        aika_nyt = dt.datetime.now()
        dt_string = aika_nyt.strftime("%d.%m.%Y %H:%M:%S")

        Asetukset.objects.update(
            SettingName = 'junadataUpdated',
            SettingUser = login_user,
            SettingValue = dt_string,
            Modified = aika_nyt
        )

    return HttpResponseRedirect('/')

