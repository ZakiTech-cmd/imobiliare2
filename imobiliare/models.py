from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Announce(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, verbose_name='Titlu')
    description = models.TextField(verbose_name='Descriere')
    price = models.FloatField(verbose_name='Pret')
    floor = models.IntegerField(null=True, verbose_name='Etaj')
    county = models.CharField(max_length=100, verbose_name='Judet')
    location = models.CharField(max_length=100, verbose_name='Localitate')
    image = models.ImageField(null=True, blank=True, verbose_name='Imagine')
    publish_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        ordering = ['-last_update', '-publish_date']

    #  functii care sunt declarate in interiorul clasei se numesc metode,
    #  Getter de titlu

    def __str__(self):
        return self.title


class PostImage(models.Model):
    announce = models.ForeignKey(Announce, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', verbose_name='Imagine')

    def __str__(self):
        return self.announce.title
