# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from geo.models import Admin1Codes, Admin2Codes, Geoname, Location
from django import forms
import re

def load_administrative_divisions(country):
    return Admin1Codes.objects.filter(countrycode=country)

def load_administrative_2_divisions(country, admin1_code):
    return Admin2Codes.objects.filter(countrycode=country, admin1_code=admin1_code)

def load_places(country, admin1_code):
    return Geoname.objects.filter(country=country, admin1=admin1_code, fcode__startswith='PPL')

def __admin2_sanitizer(admin2):
    admin2.name = admin2.name.split(' ')[-1]
    return admin2

def build_administrative_2_divisions(admin1_code):
    admin2_divisions = map(__admin2_sanitizer, load_administrative_2_divisions(admin1_code.countrycode, admin1_code.admin1_code))
    return [('', '')] + sorted(map(lambda x: (x.geonameid, x.name[0].upper() + x.name[1:]), admin2_divisions), key=lambda x: x[1])

def build_places(admin1_code):
    places = load_places(admin1_code.countrycode, admin1_code.admin1_code)
    return [('', '')] + sorted(map(lambda x: (x.geonameid, x.name[0].upper() + x.name[1:]), places), key=lambda x: x[1])

def set_extra_fields(**kwargs):
    form = kwargs['form']
    form.initial['administrative_division'] = ''
    form.initial['place'] = ''
    fields = form.fields
    catalonia = filter(lambda x: x.name == 'Catalonia', load_administrative_divisions('ES'))[0]
    fields['administrative_division'] = forms.ChoiceField(label=_('Prov&iacute;ncia'), choices=build_administrative_2_divisions(catalonia))
    fields['place'] = forms.ChoiceField(label=_('Municipi'), choices=build_places(catalonia))
    return kwargs

def clean_extra_fields(form, **kwargs):
    if not 'administrative_division' in form.cleaned_data and form.cleaned_data['administrative_division'] != '':
        form.add_error('administrative_division', _('Indica una prov&iacute;ncia'))
        return
    if not 'place' in form.cleaned_data and form.cleaned_data['place'] != '':
        form.add_error('place', _('Indica un municipi'))
        return

def on_user_creation(user, **kwargs):
    if 'location' in kwargs:
        if kwargs['location'] == None:
            if 'place' in kwargs:
                if kwargs['place'] == '':
                    raise Exception('Place missing')
            else:
                return
            kwargs['location'] = kwargs['place']
        place = Geoname.objects.get(geonameid=kwargs['location'])
        kwargs['administrative_division'] = place.admin2
        kwargs['admin1'] = place.admin1
        location = Location(user=user, admin1=kwargs['admin1'], admin2=kwargs['administrative_division'], place=kwargs['location'])
        location.full_clean()
        location.save()
        
