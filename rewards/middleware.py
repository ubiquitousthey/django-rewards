#!/usr/bin/env python
# encoding: utf-8
"""
middleware.py

created by Maximillian Dornseif on 2009-02-07.
Copyright (c) 2009, 2010 HUDORA. All rights reserved.
"""
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core import urlresolvers
from django.http import HttpResponseRedirect, Http404
from rewards.models import Campaign, Inflow
from rewards.tools import get_ip

AFFILIATE_COOKIE = 'affiliate_cookie'
AFFILIATE_PARM = 'aff'
AFFILIATE_SESSION_VAR = 'campaign'
class RewardsMiddleware(object):
    
    def process_request(self, request):
        new_inflow = False
        campaign_from_path = False
        campaign_designator = None
        if not hasattr(request, 'session'):
            raise RuntimeError('No session information! Do you use SessionMiddleware'
                               ' and have it loaded before RewardsMiddleware?')

        # don't process AJAX requests
        if request.is_ajax():
            return

        #check for campaign on end #TODO:Figure out how to put this in the urls.py file so that it can be included at end
        resolution = ''
        try:
            resolution = urlresolvers.resolve(request.path)
        except Http404:
            path_end = request.path.split('/')[-1]
            if path_end:
                campaign_designator = path_end
                redirect_path = request.path[:-len(path_end)]
                new_inflow = True
                campaign_from_path = True

        if resolution:
            return

        # only process GET requests with an 'aff' parameter
        if (request.method == 'GET') and (AFFILIATE_PARM in request.GET):
            campaign_designator = request.GET[AFFILIATE_PARM]
            redirect_path = request.path
            new_inflow = True

        if AFFILIATE_COOKIE in request.COOKIES:
            campaign_designator = request.COOKIES[AFFILIATE_COOKIE]
            redirect_path = request.path
            new_inflow = False

        if not campaign_designator:
            return

        try:
            key = Campaign.get_cache_key(campaign_designator)
            campaign = cache.get(key)
            if not campaign:
                campaign = Campaign.objects.get(designator=campaign_designator)
                cache.set(key,campaign)
        except Campaign.DoesNotExist:
            return

        request.session[AFFILIATE_SESSION_VAR] = campaign_designator

        if new_inflow:
            # register inflow
            ip_address = get_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
            referrer = request.META.get('HTTP_REFERER', '')[:255]
            Inflow.objects.create(campaign_designator=campaign.designator, ip_address=ip_address,
                                  user_agent=user_agent, referrer=referrer)

        return HttpResponseRedirect(redirect_path)

    def process_response(self,request, response):
        if request.is_ajax():
            return response

        try:
            if not AFFILIATE_COOKIE in request.COOKIES:
                response.set_cookie('affiliate_code',request.session['campaign'],max_age=60*24*60*60)
        except:
            pass
        
        return response