# -*- coding: utf-8 -*-
"""
Models for django-rewards.

Created by Maximillian Dornseif on 2010-01-26.
Copyright (c) 2010  Maximillian Dornseif. All rights reserved.
"""

import base64
import hashlib
import random
import time
from django.conf.urls.defaults import url
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from django.core.cache import cache
from rewards.tools import get_ip


CONVERSION_STATUS_CHOICES = (('created', 'created'), ('processed', 'processed'),
                             ('finished', 'finished'), ('canceled', 'canceled'))

class Campaign(models.Model):
    designator = models.CharField(max_length=28, null=True, blank=True, editable=False,
                                  unique=True, db_index=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    commission = models.DecimalField(max_digits=4,decimal_places=3,default=.100)
    
    class Meta:
        """Additional imformation for the ORM."""
        get_latest_by = 'created_at'
        ordering = ['-created_at']
    
    def __unicode__(self):
        """Return a Unicode/String representation of the Object."""
        return u"Campaign {0}".format(self.designator)

    def _get_inflow_set(self):
        return Inflow.objects.filter(campaign_designator=self.designator)
    inflow_set = property(_get_inflow_set)

    @staticmethod
    def get_cache_key(campaign_designator):
        ct = ContentType.objects.get_for_model(Campaign)
        slug = '{0}:{1}'.format(ct.app_label,ct.model)
        key = '{0}:{1}'.format(slug,campaign_designator)
        return key

    def save(self, *args, **kwargs):
        if not self.designator:
            chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), self.id))
            self.designator = "dc%s" % base64.b32encode(chash.digest()).rstrip('=')

        key = Campaign.get_cache_key(self.designator)
        cache.delete(key)
        return super(Campaign, self).save(*args, **kargs)


class Inflow(models.Model):
    # this has the potential to get an ugly DB bottleneck, so we vo not use something which enforces
    # referential intigrity, like
    # campaign = models.ForeignKey(Campaign, to_field='designator')
    # but instead:
    campaign_designator = models.CharField(max_length=28, db_index=True)
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.campaign_designator, self.referrer, self.created_at)


class Conversion(models.Model):
    campaign = models.ForeignKey(Campaign, to_field='designator')
    value = models.DecimalField(max_digits=13,decimal_places=2)
    amount = models.DecimalField(max_digits=13,decimal_places=2) #This is the commission amount
    reference = models.CharField(max_length=64, blank=True, default='', db_index=True)
    text = models.CharField(max_length=255)
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=CONVERSION_STATUS_CHOICES,
                              default=CONVERSION_STATUS_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


    @staticmethod
    def create_from_inflow(inflow, value, reference, text):
        campaign = Campaign.objects.get(designator=inflow.campaign_designator)
        conversion = Conversion.objects.create(
            campaign=campaign,
            value=value,
            amount=value * campaign.commission,
            reference=reference,
            text=text,
            ip_address=inflow.ip_address,
            referrer=inflow.referrer,
            user_agent=inflow.user_agent
        )
        return conversion


    def clean(self):
        if amount < 0:
            raise ValidationError("Conversion amounts must be more than zero.")

    def __unicode__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.campaign.designator,self.reference, self.status, self.value, self.text)


class Account(models.Model):
    user = models.OneToOneField(User)
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username + "\t" + str(self.balance)

class Activity(models.Model):
    account = models.ForeignKey(Account)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    reference = models.IntegerField()

    def __unicode__(self):
        return self.account.user.username + "\t" + str(self.amount)

    @staticmethod
    def create_from_ref(user, reference, **save_kargs):
        activity = Activity()
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            account = Account.objects.create(user=user, balance=0)
        activity.account = account
        activity.amount = reference.amount
        activity.content_type = ContentType.objects.get_for_model(type(reference))
        activity.reference = reference.pk
        return activity.save(**save_kargs)

    def save(self, *args, **kargs):
        db=None
        if 'using' in kargs:
            db = kargs['using']
        transaction.enter_transaction_management(using=db)
        activity = super(Activity,self).save(*args, **kargs)
        self.account.balance += self.amount
        self.account.save(**kargs)
        transaction.commit(using=db)
        return activity


class Check(models.Model):
    number = models.IntegerField()
    amount = models.DecimalField(max_digits=13,decimal_places=2)
    payee = models.CharField(max_length=30)
    date = models.DateField(auto_created=True)
    creator = models.ForeignKey(User)

    def clean(self):
        if self.amount < 0:
            raise ValidationError('Check amounts must be more than zero.')


class ReversedConversion(models.Model):
    amount = models.DecimalField(max_digits=13,decimal_places=2)
    original_conversion = models.ForeignKey(Conversion)
    date = models.DateField(auto_created=True)

    def clean(self):
        if amount < 0:
            raise  ValidationError('Reversed conversions must be less than zero.')
    
    