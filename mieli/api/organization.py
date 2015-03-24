from identity.models import Organization
from django.contrib.sites.models import Site
from django.db import transaction
from mieli import registry
import random
import string
import copy

def setup_query(kwargs):
    query = copy.copy(kwargs)
    for key in kwargs.iterkeys():
        if key == 'domain' or key == 'name':
            value = query.pop(key)
            query['site__%s' % key] = value
    return query

def get(**kwargs):
    query = setup_query(kwargs)
    try:
        organization = Organization.objects.get(**query)
    except Organization.DoesNotExist:
        organization = None
    return organization

def get_by_username(username):
    if not '@' in username:
        raise Exception("invalid username '%s', expected username@organization" % username)
    domain = username.split('@')[1]
    query = { 'domain': domain }
    result = get(**query)
    if result == None:
        query = { 'alias': domain }
        result = get(**query)
    return result

@transaction.atomic
def create(domain, name, **kwargs):
    if get(domain=domain):
        raise Exception('domain %s is already in use' % domain)
    site = Site(domain=domain, name=name)
    site.full_clean()
    site.save()
    url = kwargs.pop('url') # hack
    u = kwargs.pop('user') # hack
    token = kwargs.pop('token') # hack
    organization = Organization(site=site, **kwargs)
    organization.full_clean()
    organization.save()
    kwargs['url'] = url
    kwargs['token'] = token
    kwargs['user'] = u
    registry.signal('organization_create', organization=organization, **kwargs)
    return organization

@transaction.atomic
def delete(**kwargs):
    organization = get(**kwargs)
    if organization == None:
        raise Exception('unknown organization')
    registry.signal('organization_delete', organization=organization, **kwargs)
    organization.site.delete()
