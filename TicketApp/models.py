# Create your models here.
from django.db import models
from django.db.models.functions import Lower

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    class Meta:
        constraints = [
            models.UniqueConstraint(Lower('email').desc(), Lower('username').desc(), name='unique_lower_username_email')
        ]

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=70)
    street = models.CharField(max_length=90)
    country = models.CharField(max_length=40)
    postalcode = models.CharField(max_length=10)

class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey('User', null=True, related_name="purchased_by", on_delete=models.CASCADE)
    seller = models.ForeignKey('User', null=False, related_name="sold_by", on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    area = models.ForeignKey('Area', on_delete=models.CASCADE)

class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.URLField(null=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    info = models.CharField(max_length=5000)
    class Meta:
        constraints = [
            models.UniqueConstraint('address', name='unique_address')
        ]

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    area_type = models.CharField(max_length=30)
    zone = models.CharField(max_length=20)
    number_seats = models.PositiveSmallIntegerField()
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)

class Price(models.Model):
    class Currency(models.TextChoices):
        Cad = 'CAD',
        Usd = 'USD',
        Gbp = 'GBP',
        Euro = '€'
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey('Area', null=False, on_delete=models.CASCADE)
    currency = models.CharField(max_length=20, choices=Currency.choices)
    value = models.DecimalField(null=False, max_digits=6, decimal_places=2)

class Performer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.URLField(null=True)
    description = models.CharField(max_length=2000)

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('name',), name='unique_name')
        ]

class EventPerformer(models.Model):
    id = models.AutoField(primary_key=True)
    performer = models.ForeignKey('Performer', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    stage_time = models.DateTimeField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['performer', 'event'], name='unique_together_performer_event')
        ]

class EventGenre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['genre', 'event'], name='unique_together_genre_event')
        ]

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    venue = models.ForeignKey('Venue', null=False, on_delete=models.CASCADE)
    lineup = models.ManyToManyField(
        Performer,
        through='EventPerformer',
        through_fields=('event', 'performer'),
    )
    genres = models.ManyToManyField(
        Genre,
        through='EventGenre',
        through_fields=('event', 'genre'),
    )
    date = models.DateTimeField()
    admission_age = models.DecimalField(null=False, max_digits=2, decimal_places=0)
    cancelled = models.BooleanField(null=False)