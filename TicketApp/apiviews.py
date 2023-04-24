''' Because this was a learning experience
aside from the eventperformer view the through tables haven't been updated
to use related sets and should not be used as a reference. There are also many
needless uses of try and except instead of a filter() and exists() meaning the code
is needless long and over indented '''

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from TicketApp.models import User, Address, Venue, Event, Area, Offer, Price, Performer, Genre, EventGenre, EventPerformer
from TicketApp.serializers import UserSerializer, AddressSerializer, VenueSerializer, EventSerializer, AreaSerializer, OfferSerializer, PriceSerializer, PerformerSerializer, GenreSerializer, EventGenreSerializer, EventPerformerSerializer
import io

@csrf_exempt
def UserApi(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        email = request.GET.get("email")
        if username and email:
            user = User.objects.filter(Q(username__iexact=username) & Q(email__iexact=email))
            userSerializer = UserSerializer(user, many=True)
            return JsonResponse({"ok" : userSerializer.data}, safe=False)
        elif username:
            user = User.objects.filter(Q(username__iexact=username))
            userSerializer = UserSerializer(user, many=True)
            return JsonResponse({"ok" : userSerializer.data}, safe=False)
        elif email:
            user = User.objects.filter(Q(Q(email__iexact=email)))
            userSerializer = UserSerializer(user, many=True)
            return JsonResponse({"ok" : userSerializer.data}, safe=False)
        else:
            users = User.objects.all()
            usersSerializer = UserSerializer(users, many=True)
            return JsonResponse({"ok" : usersSerializer.data}, safe=False)

    elif request.method == 'POST':
        userbytes = io.BytesIO(request.body)
        userdata = JSONParser().parse(userbytes)
        userSerializer = UserSerializer(data=userdata)
        if userSerializer.is_valid():
            userSerializer.save()
            return JsonResponse({"ok": f'Created User'})
        return JsonResponse({"error": userSerializer.errors}, status=400)

    elif request.method == 'PUT':
        userbytes = io.BytesIO(request.body)
        userdata = JSONParser().parse(userbytes)
        try:
            usermodel = User.objects.get(username=userdata.get("username"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Username not found"}, status=400)
        userSerializer = UserSerializer(usermodel, data=userdata)
        if userSerializer.is_valid():
            userSerializer.save()
            return JsonResponse({"ok": f'Updated {userSerializer.validated_data.get("username")}'})
        else:
            return JsonResponse({"error": userSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if username:
            try:
                usermodel = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Username not found"}, status=400)
            usermodel.delete()
            return JsonResponse({"ok": f'Deleted {username}'})
        return JsonResponse({"error": "Username not provided"}, status=400)

@csrf_exempt
def AddressApi(request, id=""):
    if request.method == 'GET':
        if id:
            address = Address.objects.filter(id=id)
            addressSerializer = AddressSerializer(address, many=True)
            return JsonResponse({"ok" : addressSerializer.data}, safe=False)
        else:
            addresses = Address.objects.all()
            addressesSerializer = AddressSerializer(addresses, many=True)
            return JsonResponse({"ok" : addressesSerializer.data}, safe=False)

    elif request.method == 'POST':
        addressbytes = io.BytesIO(request.body)
        addressdata = JSONParser().parse(addressbytes)
        addressSerializer = AddressSerializer(data=addressdata)
        if addressSerializer.is_valid():
            addressSerializer.save()
            return JsonResponse({"ok": f'Created Address'})
        return JsonResponse({"error": addressSerializer.errors}, status=400)

    elif request.method == 'PUT':
        addressbytes = io.BytesIO(request.body)
        addressdata = JSONParser().parse(addressbytes)
        try:
            addressmodel = Address.objects.get(id=addressdata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Address not found"}, status=400)
        addressSerializer = AddressSerializer(addressmodel, data=addressdata)
        if addressSerializer.is_valid():
            addressSerializer.save()
            return JsonResponse({"ok": f'Updated Address'})
        else:
            return JsonResponse({"error": addressSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                addressmodel = Address.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Address not found"}, status=400)
            addressmodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def OfferApi(request, id=""):
    if request.method == 'GET':
        buyer = request.GET.get("buyer")
        seller = request.GET.get("seller")
        if buyer and seller:
            offers = Offer.objects.filter(Q(buyer__username__iexact=buyer) & Q(seller__username__iexact=seller))
            offersSerializer = OfferSerializer(offers, many=True)
            return JsonResponse({"ok" : offersSerializer.data}, safe=False)
        elif buyer:
            offers = Offer.objects.filter(Q(buyer__username__iexact=buyer))
            offersSerializer = OfferSerializer(offers, many=True)
            return JsonResponse({"ok" : offersSerializer.data}, safe=False)
        elif seller:
            offers = Offer.objects.filter(Q(seller__username__iexact=seller))
            offersSerializer = OfferSerializer(offers, many=True)
            return JsonResponse({"ok" : offersSerializer.data}, safe=False)
        else:
            offers = Offer.objects.all()
            offersSerializer = OfferSerializer(offers, many=True)
            return JsonResponse({"ok" : offersSerializer.data}, safe=False)

    elif request.method == 'POST':
        offerbytes = io.BytesIO(request.body)
        offerdata = JSONParser().parse(offerbytes)
        offerSerializer = OfferSerializer(data=offerdata)
        try:
            if offerSerializer.is_valid():
                offerSerializer.save()
                return JsonResponse({"ok": f'Created Offer'})
        except ObjectDoesNotExist as e:
            return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": offerSerializer.errors}, status=400)

    elif request.method == 'PUT':
        offerbytes = io.BytesIO(request.body)
        offerdata = JSONParser().parse(offerbytes)
        try:
            offermodel = Offer.objects.get(id=offerdata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Offer not found"}, status=400)
        offerSerializer = OfferSerializer(offermodel, data=offerdata)
        try:
            if offerSerializer.is_valid():
                offerSerializer.save()
                return JsonResponse({"ok": f'Updated Offer'})
            else:
                return JsonResponse({"error": offerSerializer.errors}, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"error": e}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                offermodel = Offer.objects.filter(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Offer not found"}, status=400)
            offermodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def VenueApi(request, id=""):
    if request.method == 'GET':
        if id:
            venue = Venue.objects.filter(id=id)
            venueSerializer = VenueSerializer(venue, many=True)
            return JsonResponse({"ok" : venueSerializer.data}, safe=False)
        else:
            venues = Venue.objects.all()
            venuesSerializer = VenueSerializer(venues, many=True)
            return JsonResponse({"ok" : venuesSerializer.data}, safe=False)

    elif request.method == 'POST':
        venuebytes = io.BytesIO(request.body)
        venuedata = JSONParser().parse(venuebytes)
        venueSerializer = VenueSerializer(data=venuedata)
        if venueSerializer.is_valid():
            venueSerializer.save()
            return JsonResponse({"ok": f'Created Venue'})
        return JsonResponse({"error": venueSerializer.errors}, status=400)

    elif request.method == 'PUT':
        venuebytes = io.BytesIO(request.body)
        venuedata = JSONParser().parse(venuebytes)
        try:
            venuemodel = Venue.objects.get(id=venuedata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Venue not found"}, status=400)
        venueSerializer = VenueSerializer(venuemodel, data=venuedata)
        if venueSerializer.is_valid():
            venueSerializer.save()
            return JsonResponse({"ok": f'Updated Venue'})
        else:
            return JsonResponse({"error": venueSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                venuemodel = Venue.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Venue not found"}, status=400)
            venuemodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def AreaApi(request, id=""):
    if request.method == 'GET':
        if id:
            area = Area.objects.filter(id=id)
            areaSerializer = AreaSerializer(area, many=True)
            return JsonResponse({"ok" : areaSerializer.data}, safe=False)
        else:
            areas = Area.objects.all()
            areasSerializer = AreaSerializer(areas, many=True)
            return JsonResponse({"ok" : areasSerializer.data}, safe=False)

    elif request.method == 'POST':
        areabytes = io.BytesIO(request.body)
        areadata = JSONParser().parse(areabytes)
        areaSerializer = AreaSerializer(data=areadata)
        if areaSerializer.is_valid():
            areaSerializer.save()
            return JsonResponse({"ok": f'Created Area'})
        return JsonResponse({"error": areaSerializer.errors}, status=400)

    elif request.method == 'PUT':
        areabytes = io.BytesIO(request.body)
        areadata = JSONParser().parse(areabytes)
        try:
            areamodel = Area.objects.get(id=areadata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Area not found"}, status=400)
        areaSerializer = AreaSerializer(areamodel, data=areadata)
        if areaSerializer.is_valid():
            areaSerializer.save()
            return JsonResponse({"ok": f'Updated Area'})
        else:
            return JsonResponse({"error": areaSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                areamodel = Area.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Area not found"}, status=400)
            areamodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def PriceApi(request, id=""):
    if request.method == 'GET':
        if id:
            price = Price.objects.filter(id=id)
            priceSerializer = PriceSerializer(price, many=True)
            return JsonResponse({"ok" : priceSerializer.data}, safe=False)
        else:
            prices = Price.objects.all()
            pricesSerializer = PriceSerializer(prices, many=True)
            return JsonResponse({"ok" : pricesSerializer.data}, safe=False)

    elif request.method == 'POST':
        pricebytes = io.BytesIO(request.body)
        pricedata = JSONParser().parse(pricebytes)
        priceSerializer = PriceSerializer(data=pricedata)
        if priceSerializer.is_valid():
            priceSerializer.save()
            return JsonResponse({"ok": f'Created Price'})
        return JsonResponse({"error": priceSerializer.errors}, status=400)

    elif request.method == 'PUT':
        pricebytes = io.BytesIO(request.body)
        pricedata = JSONParser().parse(pricebytes)
        try:
            pricemodel = Price.objects.get(id=pricedata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Price not found"}, status=400)
        priceSerializer = PriceSerializer(pricemodel, data=pricedata)
        if priceSerializer.is_valid():
            priceSerializer.save()
            return JsonResponse({"ok": f'Updated Price'})
        else:
            return JsonResponse({"error": priceSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                pricemodel = Price.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Price not found"}, status=400)
            pricemodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def PerformerApi(request, id=""):
    if request.method == 'GET':
        if id:
            performer = Performer.objects.filter(id=id)
            performerSerializer = PerformerSerializer(performer, many=True)
            return JsonResponse({"ok" : performerSerializer.data}, safe=False)
        else:
            performers = Performer.objects.all()
            performersSerializer = PerformerSerializer(performers, many=True)
            return JsonResponse({"ok" : performersSerializer.data}, safe=False)

    elif request.method == 'POST':
        performerbytes = io.BytesIO(request.body)
        performerdata = JSONParser().parse(performerbytes)
        performerSerializer = PerformerSerializer(data=performerdata)
        if performerSerializer.is_valid():
            performerSerializer.save()
            return JsonResponse({"ok": f'Created Performer'})
        return JsonResponse({"error": performerSerializer.errors}, status=400)

    elif request.method == 'PUT':
        performerbytes = io.BytesIO(request.body)
        performerdata = JSONParser().parse(performerbytes)
        try:
            performermodel = Performer.objects.get(id=performerdata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Performer not found"}, status=400)
        performerSerializer = PerformerSerializer(performermodel, data=performerdata)
        if performerSerializer.is_valid():
            performerSerializer.save()
            return JsonResponse({"ok": f'Updated Performer'})
        else:
            return JsonResponse({"error": performerSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                performermodel = Performer.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Performer not found"}, status=400)
            performermodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def GenreApi(request, id=""):
    if request.method == 'GET':
        if id:
            genre = Genre.objects.filter(id=id)
            genreSerializer = GenreSerializer(genre, many=True)
            return JsonResponse({"ok" : genreSerializer.data}, safe=False)
        else:
            genres = Genre.objects.all()
            genresSerializer = GenreSerializer(genres, many=True)
            return JsonResponse({"ok" : genresSerializer.data}, safe=False)

    elif request.method == 'POST':
        genrebytes = io.BytesIO(request.body)
        genredata = JSONParser().parse(genrebytes)
        genreSerializer = GenreSerializer(data=genredata)
        if genreSerializer.is_valid():
            genreSerializer.save()
            return JsonResponse({"ok": f'Created Genre'})
        return JsonResponse({"error": genreSerializer.errors}, status=400)

    elif request.method == 'PUT':
        genrebytes = io.BytesIO(request.body)
        genredata = JSONParser().parse(genrebytes)
        try:
            genremodel = Genre.objects.get(id=genredata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Genre not found"}, status=400)
        genreSerializer = GenreSerializer(genremodel, data=genredata)
        if genreSerializer.is_valid():
            genreSerializer.save()
            return JsonResponse({"ok": f'Updated Genre'})
        else:
            return JsonResponse({"error": genreSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                genremodel = Genre.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Genre not found"}, status=400)
            genremodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def EventPerformerApi(request, id=""):
    if request.method == 'GET':
        performer = request.GET.get("performer")
        event = request.GET.get("event")
        if id:
            eventperformer = EventPerformer.objects.filter(id=id)
            eventperformerSerializer = EventPerformerSerializer(eventperformer, many=True)
            return JsonResponse({"ok" : eventperformerSerializer.data}, safe=False)
        elif event and performer:
                row1 = Event.objects.filter(id=event)
                row2 = Performer.objects.filter(id=performer)
                if not row1.exists():
                    return JsonResponse({"error" : "Event doesnt exist"}, status=400)
                if not row2.exists():
                    return JsonResponse({"error" : "Performer doesnt exist"}, status=400)
                eventperformers = row2[0].eventperformer_set.filter(Q(event=row1[0]))
                eventperformersSerializer = EventPerformerSerializer(eventperformers, many=True)
                return JsonResponse({"ok" : eventperformersSerializer.data}, safe=False)
        elif performer:
            row = Performer.objects.filter(id=performer)
            if not row.exists():
                return JsonResponse({"error": "Performer doesnt exist"}, status=400)
            # Using related set prefered
            eventperformers = row[0].eventperformer_set.all()
            eventperformersSerializer = EventPerformerSerializer(eventperformers, many=True)
            return JsonResponse({"ok" : eventperformersSerializer.data}, safe=False)
        elif event:
            row = Event.objects.filter(id=event)
            if not row.exists():
                return JsonResponse({"error": "Event doesnt exist"}, status=400)
            eventperformers = row[0].eventperformer_set.all()
            eventperformersSerializer = EventPerformerSerializer(eventperformers, many=True)
            return JsonResponse({"ok" : eventperformersSerializer.data}, safe=False)
        else:
            eventperformers = EventPerformer.objects.all()
            eventperformersSerializer = EventPerformerSerializer(eventperformers, many=True)
            return JsonResponse({"ok" : eventperformersSerializer.data}, safe=False)

    elif request.method == 'POST':
        eventperformerbytes = io.BytesIO(request.body)
        eventperformerdata = JSONParser().parse(eventperformerbytes)
        eventperformerSerializer = EventPerformerSerializer(data=eventperformerdata)
        if eventperformerSerializer.is_valid():
            eventperformerSerializer.save()
            return JsonResponse({"ok": f'Created EventPerformer'})
        return JsonResponse({"error": eventperformerSerializer.errors}, status=400)

    elif request.method == 'PUT':
        eventperformerbytes = io.BytesIO(request.body)
        eventperformerdata = JSONParser().parse(eventperformerbytes)
        try:
            eventperformermodel = EventPerformer.objects.get(id=eventperformerdata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "EventPerformer not found"}, status=400)
        eventperformerSerializer = EventPerformerSerializer(eventperformermodel, data=eventperformerdata)
        if eventperformerSerializer.is_valid():
            eventperformerSerializer.save()
            return JsonResponse({"ok": f'Updated EventPerformer'})
        else:
            return JsonResponse({"error": eventperformerSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                eventperformermodel = EventPerformer.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "EventPerformer not found"}, status=400)
            eventperformermodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def EventGenreApi(request, id=""):
    if request.method == 'GET':
        genre = request.GET.get("genre")
        event = request.GET.get("event")
        if id:
            eventgenre = EventGenre.objects.filter(id=id)
            eventgenreSerializer = EventGenreSerializer(eventgenre, many=True)
            return JsonResponse({"ok" : eventgenreSerializer.data}, safe=False)
        elif event and genre:
            try:
                Event.objects.get(id=event)
                Genre.objects.get(name=genre)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Event or Genre doesnt exist"}, status=400)
            eventgenres = EventGenre.objects.filter(Q(event__id=event) & Q(genre__name__iexact=genre))
            eventgenresSerializer = EventGenreSerializer(eventgenres, many=True)
            return JsonResponse({"ok" : eventgenresSerializer.data}, safe=False)
        elif genre:
            try:
                Genre.objects.get(name=genre)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Genre doesnt exist"}, status=400)
            eventgenres = EventGenre.objects.filter(Q(genre__name__iexact=genre))
            eventgenresSerializer = EventGenreSerializer(eventgenres, many=True)
            return JsonResponse({"ok" : eventgenresSerializer.data}, safe=False)
        elif event:
            try:
                Event.objects.get(id=event)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Event doesnt exist"}, status=400)
            eventgenres = EventGenre.objects.filter(Q(event__id=event))
            eventgenresSerializer = EventGenreSerializer(eventgenres, many=True)
            return JsonResponse({"ok" : eventgenresSerializer.data}, safe=False)
        else:
            eventgenres = EventGenre.objects.all()
            eventgenresSerializer = EventGenreSerializer(eventgenres, many=True)
            return JsonResponse({"ok" : eventgenresSerializer.data}, safe=False)

    elif request.method == 'POST':
        eventgenrebytes = io.BytesIO(request.body)
        eventgenredata = JSONParser().parse(eventgenrebytes)
        eventgenreSerializer = EventGenreSerializer(data=eventgenredata)
        if eventgenreSerializer.is_valid():
            eventgenreSerializer.save()
            return JsonResponse({"ok": f'Created EventGenre'})
        return JsonResponse({"error": eventgenreSerializer.errors}, status=400)

    elif request.method == 'PUT':
        eventgenrebytes = io.BytesIO(request.body)
        eventgenredata = JSONParser().parse(eventgenrebytes)
        try:
            eventgenremodel = EventGenre.objects.get(id=eventgenredata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "EventGenre not found"}, status=400)
        eventgenreSerializer = EventGenreSerializer(eventgenremodel, data=eventgenredata)
        if eventgenreSerializer.is_valid():
            eventgenreSerializer.save()
            return JsonResponse({"ok": f'Updated EventGenre'})
        else:
            return JsonResponse({"error": eventgenreSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                eventgenremodel = EventGenre.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "EventGenre not found"}, status=400)
            eventgenremodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)

@csrf_exempt
def EventApi(request, id=""):
    if request.method == 'GET':
        venue = request.GET.get("venue")
        if id:
            event = Event.objects.filter(id=id)
            eventSerializer = EventSerializer(event, many=True)
            return JsonResponse({"ok" : eventSerializer.data}, safe=False)
        elif venue:
            try:
                Venue.objects.get(id=venue)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Venue doesnt exist"}, status=400)
            events = Event.objects.filter(Q(venue__id=venue))
            eventsSerializer = EventSerializer(events, many=True)
            return JsonResponse({"ok" : eventsSerializer.data}, safe=False)
        else:
            events = Event.objects.all()
            eventsSerializer = EventSerializer(events, many=True)
            return JsonResponse({"ok" : eventsSerializer.data}, safe=False)
        
    elif request.method == 'POST':
        eventbytes = io.BytesIO(request.body)
        eventdata = JSONParser().parse(eventbytes)
        eventSerializer = EventSerializer(data=eventdata)
        if eventSerializer.is_valid():
            eventSerializer.save()
            return JsonResponse({"ok": f'Created Event'})
        return JsonResponse({"error": eventSerializer.errors}, status=400)

    elif request.method == 'PUT':
        eventbytes = io.BytesIO(request.body)
        eventdata = JSONParser().parse(eventbytes)
        try:
            eventmodel = Event.objects.get(id=eventdata.get("id"))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=400)
        eventSerializer = EventSerializer(eventmodel, data=eventdata)
        if eventSerializer.is_valid():
            eventSerializer.save()
            return JsonResponse({"ok": f'Updated Event'})
        else:
            return JsonResponse({"error": eventSerializer.errors}, status=400)

    elif request.method == 'DELETE':
        if id:
            try:
                eventmodel = Event.objects.get(id=id)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Event not found"}, status=400)
            eventmodel.delete()
            return JsonResponse({"ok": f'Deleted {id}'})
        return JsonResponse({"error": "id not provided"}, status=400)