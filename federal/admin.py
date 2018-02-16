# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Account , Position , State , Lga , Thread , Zone , Reply , Feedback

# Register your models here.

admin.site.register(Account)
admin.site.register(Position)
admin.site.register(State)
admin.site.register(Zone)
admin.site.register(Lga)
admin.site.register(Thread)
admin.site.register(Reply)
admin.site.register(Feedback)
