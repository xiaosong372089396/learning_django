# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = (
                        ('1', u'总监'),
                        ('2', u'经理'),
                        ('3', u'研发'),
                    )
    user = models.OneToOneField(User, primary_key=True)
    role = models.CharField(max_length=4, default='3', choices=GENDER_CHOICES)
    note = models.CharField(max_length=128, default='', blank=True)

    def __str__(self):
        return self.role

    def __unicode__(self):
        return self.role


@receiver(post_save, sender=User)
def create_save_user(sender, **kwargs):
    if kwargs['update_fields'] == frozenset([u'last_login']):return True
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

