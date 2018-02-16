# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class Position(models.Model):
    position = models.CharField(max_length = 100)
    namespace = models.IntegerField()
    state = models.IntegerField()
    zone = models.IntegerField()
    lga = models.IntegerField()
    display_pic = models.FileField(default='anon.png')
    date = models.DateTimeField(default = datetime.now)

    def __str__(self):
         return self.position


class State(models.Model):
    state = models.CharField(max_length = 50)
    state_code = models.IntegerField(default=1)

    def __str__(self):
         return self.state

class Zone(models.Model):
    state = models.ForeignKey(State)
    zone = models.CharField(max_length = 100)
    zone_code = models.IntegerField()

    def __str__(self):
         return self.zone

    class Meta:
        ordering = ['state']


class Lga(models.Model):
    state = models.ForeignKey(State)
    zone = models.ForeignKey(Zone)
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
    position = models.ForeignKey(Position)
    state = models.ForeignKey(State)
    zone = models.ForeignKey(Zone)
    lga = models.ForeignKey(Lga)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username


class Thread(models.Model):
    account = models.ForeignKey(Account)
    thread = models.TextField()
    namespace = models.IntegerField()
    state = models.IntegerField()
    zone = models.IntegerField()
    lga = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
         return self.thread

class ThreadFavoriter(models.Model):
    thread = models.ForeignKey(Thread)
    account = models.ForeignKey(Account)


class Media(models.Model):
    thread = models.ForeignKey(Thread)
    image = models.FileField()
    audio = models.FileField()
    video = models.FileField()

class Comment(models.Model):
    thread = models.ForeignKey(Thread)
    account = models.ForeignKey(Account)
    comment = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
         return self.comment

class CommentFavoriter(models.Model):
    comment = models.ForeignKey(Comment)
    account = models.ForeignKey(Account)

class Reply(models.Model):
    comment = models.ForeignKey(Comment)
    account = models.ForeignKey(Account)
    reply = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.reply


class ReplyFavoriter(models.Model):
    reply = models.ForeignKey(Reply)
    account = models.ForeignKey(Account)


class Feedback(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    feed = models.TextField()

    def __str__(self):
         return self.feed

class ForgotPassword(models.Model):
    username = models.EmailField()
    reset_password = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.now)
