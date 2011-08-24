# encoding: utf-8

"""Copyright (c) 2010  Maximillian Dornseif. All rights reserved."""

from rewards.models import Campaign, Inflow, Conversion, CONVERSION_STATUS_CHOICES
from rewards.tools import get_ip

__version_info__ = {
    'major' : 0,
    'minor' : 0,
    'micro' : 0,
    'releaselevel' : 'alpha',
    'serial' : 1
}

def get_version(short=False):
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

def regcon(campaign_designator, value, reference='', text='', ip_address='', user_agent='', referer=''):
    campaign = Campaign.objects.get(designator=campaign_designator)
    conversion = Conversion.objects.create(campaign=campaign, value=value, reference=reference,
                                           text=text[:255], ip_address=ip_address, user_agent=user_agent,
                                           referer=referer[:255])


def regcon_by_request(request, value, reference='', text=''):
    """Register a conversion."""
    ip_address = get_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referer = request.META.get('HTTP_REFERER', '')
    campaign_designator = request.session.get('campaign', None)
    if campaign_designator:
        regcon(campaign_designator, int(value), reference, text, ip_address=ip_address,
               user_agent=user_agent, referer=referer)

def updatecon_by_reference(reference, state):
    # TBD
    conversions = Conversion.objects.filter(reference)
    if not len(conversions):
        return None
    if state not in dict(CONVERSION_STATUS_CHOICES):
        raise RuntimeError('invalid state %r' % state)
    conversion = conversions[0]
    conversion.state = state
    conversion.save()
    return conversion