from rest_framework import serializers
from TicketApp.models import *
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist
# from rest_framework.validators.functions import Lower
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from django.http import HttpResponse, JsonResponse
# import io

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=20, validators=[
                                     UniqueValidator(queryset=User.objects.all(), lookup='iexact')])
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact')])

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):

    city = serializers.CharField(max_length=70)
    street = serializers.CharField(max_length=90)
    country = serializers.CharField(max_length=40)
    postalcode = serializers.CharField(max_length=10)

    class Meta:
        model = Address
        fields = ("id", "city", "street", "country", "postalcode")

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.country = validated_data.get('country', instance.country)
        instance.postalcode = validated_data.get(
            'postalcode', instance.postalcode)
        instance.save()
        return instance


class VenueSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=100)
    address = serializers.SlugRelatedField(
        slug_field='id', queryset=Address.objects.all())
    info = serializers.CharField(max_length=5000)
    image = serializers.URLField(allow_null=True)

    class Meta:
        model = Venue
        fields = ("id", "name", "address", "info", "image")

    def create(self, validated_data):
        return Venue.objects.create(**validated_data)

    def update(self, instance, validated_data):

        address = validated_data.get("address")
        setattr(instance, "address", address)

        instance.name = validated_data.get('name', instance.name)
        instance.info = validated_data.get('info', instance.info)
        instance.image = validated_data.get(
            'image', instance.image)

        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=120)
    venue = serializers.SlugRelatedField(
        slug_field='id', queryset=Venue.objects.all())
    date = serializers.DateTimeField()
    admission_age = serializers.DecimalField(max_digits=2, decimal_places=0)
    cancelled = serializers.BooleanField()

    class Meta:
        model = Event
        fields = ("id", "name", "venue", "date", "admission_age", "cancelled")

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):

        venue = validated_data.get("venue")
        setattr(instance, "venue", venue)

        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.admission_age = validated_data.get(
            'admission_age', instance.admission_age)
        instance.cancelled = validated_data.get(
            'cancelled', instance.cancelled)

        instance.save()
        return instance


class AreaSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=40)
    area_type = serializers.CharField(max_length=30)
    zone = serializers.CharField(max_length=20)
    number_seats = serializers.IntegerField()
    venue = serializers.SlugRelatedField(
        slug_field='id', queryset=Venue.objects.all())

    class Meta:
        model = Area
        fields = ("id", "name", "area_type", "zone", "number_seats", "venue")

    def create(self, validated_data):
        return Area.objects.create(**validated_data)

    def update(self, instance, validated_data):

        venue = validated_data.get("venue")
        setattr(instance, "venue", venue)

        instance.name = validated_data.get('name', instance.name)
        instance.area_type = validated_data.get(
            'area_type', instance.area_type)
        instance.zone = validated_data.get('zone', instance.zone)
        instance.number_seats = validated_data.get(
            'number_seats', instance.number_seats)

        instance.save()
        return instance


class OfferSerializer(serializers.ModelSerializer):
    buyer = serializers.SlugRelatedField(
        slug_field='username', allow_null=True, required=False, queryset=User.objects.all())
    seller = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())
    event = serializers.SlugRelatedField(
        slug_field='id', queryset=Event.objects.all())
    area = serializers.SlugRelatedField(
        slug_field='id', queryset=Area.objects.all())

    class Meta:
        model = Offer
        fields = ("id", "buyer", "seller", "event", "area")

    def create(self, validated_data):
        return Offer.objects.create(
            **validated_data)

    def update(self, instance, validated_data):
        buyer = validated_data.get('buyer')
        setattr(instance, "buyer", buyer)

        seller = validated_data.get("seller")
        setattr(instance, "seller", seller)

        event = validated_data.get("event")
        setattr(instance, "event", event)

        area = validated_data.get("area")
        setattr(instance, "area", area)

        instance.save()
        return instance


class PriceSerializer(serializers.ModelSerializer):

    area = serializers.SlugRelatedField(
        slug_field='id', queryset=Area.objects.all())
    currency = serializers.ChoiceField(choices=Price.Currency.choices)
    value = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Price
        fields = ("id", "area", "currency", "value")

    def create(self, validated_data):
        return Price.objects.create(**validated_data)

    def update(self, instance, validated_data):

        area = validated_data.get("area")
        setattr(instance, "area", area)

        instance.currency = validated_data.get('currency', instance.currency)
        instance.value = validated_data.get('value', instance.value)

        instance.save()
        return instance


class PerformerSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    image = serializers.URLField(allow_null=True)

    class Meta:
        model = Performer
        fields = ("id", "name", "description", "image")

    def create(self, validated_data):
        return Performer.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get(
            'image', instance.image)

        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=40)

    class Meta:
        model = Genre
        fields = ("id", "name")

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)

        instance.save()
        return instance


class EventPerformerSerializer(serializers.ModelSerializer):
    performer = serializers.SlugRelatedField(
        slug_field='id', queryset=Performer.objects.all())
    event = serializers.SlugRelatedField(
        slug_field='id', queryset=Event.objects.all())
    stage_time = serializers.DateTimeField()

    class Meta:
        model = EventPerformer
        fields = ("id", "performer", "event", "stage_time")

    def create(self, validated_data):
        return EventPerformer.objects.create(**validated_data)

    def update(self, instance, validated_data):

        performer = validated_data.get("performer")
        setattr(instance, "performer", performer)

        event = validated_data.get("event")
        setattr(instance, "event", event)

        instance.stage_time = validated_data.get(
            'stage_time', instance.stage_time)

        instance.save()
        return instance


class EventGenreSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='name', queryset=Genre.objects.all())
    event = serializers.SlugRelatedField(
        slug_field='id', queryset=Event.objects.all())

    class Meta:
        model = EventGenre
        fields = ("id", "genre", "event")

    def create(self, validated_data):
        return EventGenre.objects.create(**validated_data)

    def update(self, instance, validated_data):

        genre = validated_data.get("genre")
        setattr(instance, "genre", genre)

        event = validated_data.get("event")
        setattr(instance, "event", event)

        instance.save()
        return instance
