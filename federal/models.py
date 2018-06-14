# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
import pytz



class Position(models.Model):
    position = models.CharField(max_length = 100)
    namespace = models.IntegerField()
    state = models.IntegerField()
    zone = models.IntegerField()
    lga = models.IntegerField()
    display_pic = models.FileField(default='anon.png')
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
         return self.position


class State(models.Model):
    state = models.CharField(max_length = 50)
    state_code = models.IntegerField(default=1)

    def __str__(self):
         return self.state

class Zone(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    zone = models.CharField(max_length = 100)
    zone_code = models.IntegerField()

    def __str__(self):
         return self.zone

    class Meta:
        ordering = ['state']


class Lga(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    lga = models.CharField(max_length = 100)
    lga_code = models.IntegerField()


    def __str__(self):
         return self.lga

    class Meta:
        ordering = ['lga']

class Account(models.Model):
    username = models.EmailField()
    password = models.CharField(max_length = 50)
    firstname = models.CharField(max_length = 30 , default='anonymous')
    lastname = models.CharField(max_length = 30 , default='anonymous')
    display_pic = models.FileField(default='anon.png')
    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    lga = models.ForeignKey(Lga,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Thread(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    thread = models.TextField()
    namespace = models.IntegerField()
    state = models.IntegerField()
    zone = models.IntegerField()
    lga = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
         return self.thread

class ThreadFavoriter(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)


class Media(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    image = models.FileField()
    audio = models.FileField()
    video = models.FileField()

class Comment(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return self.comment

class CommentFavoriter(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    reply = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.reply


class ReplyFavoriter(models.Model):
    reply = models.ForeignKey(Reply,on_delete=models.CASCADE)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)


class Feedback(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    feed = models.TextField()
    date = models.DateTimeField(default= timezone.now)

    def __str__(self):
         return self.feed

class ForgotPassword(models.Model):
    username = models.EmailField()
    reset_password = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
