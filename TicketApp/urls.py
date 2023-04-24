from django.urls import path, re_path
from TicketApp import views, apiviews

'''
List of api routes

                    User Routes:
Get, Delete
-----------------------------
Show all users = api/users/
Show one user by username = api/users?username={username}
Show one user by email = api/users?email={email}
Delete one user = api/users/<username>

Post, Put Routes
-----------------------------
id required in body for Put
Add/Update user with request body = api/users/


                    Address Routes:
Get, Delete
-----------------------------
Show all addresses = api/addresses/
Show/Delete one address = api/addresses/<id>

Post, Put Routes
-----------------------------
id required in body for Put
Add/Update address with request body = api/addresses/


                    Offer Routes:
Get, Delete
-----------------------------
Show all offers = api/offers/
Show all of a buyers and/or sellers offers = api/offers?buyer={username}&seller={username}
Show/Delete offer = api/offers/<id>

Post, Put Routes
-----------------------------
id required in body for Put
buyer username may be blank or omitted entirely
buyer (if provided) and seller usernames must exist or else error returned, ids for event and area must exist
Add/Update offer with request body = api/offers/


                    Venue Routes:
Get, Delete
-----------------------------
Show all venues = api/venues/
Show/Delete venue = api/venues/<id>

Post, Put Routes
-----------------------------
id required in body for Put
id for address must exist
Add/Update venue with request body = api/venues/


                    Area Routes:
Get, Delete
-----------------------------
Show all areas = api/areas/
Show/Delete area = api/areas/<id>

Post, Put Routes
-----------------------------
id required in body for Put
id for venue must exist
Add/Update area with request body = api/areas/


                    Price Routes:
Get, Delete
-----------------------------
Show all prices = api/prices/
Show/Delete price = api/prices/<id>

Post, Put Routes
-----------------------------
id required in body for Put
id for area must exist
Add/Update price with request body = api/prices/


                    Performer Routes:
Get, Delete
-----------------------------
Show all performers = api/performers/
Show/Delete performer = api/performers/<id>

Post, Put Routes
-----------------------------
id required in body for Put
Add/Update performer with request body = api/performers/


                    Genre Routes:
Get, Delete
-----------------------------
Show all genres = api/genres/
Show/Delete genre = api/genres/<id>

Post, Put Routes
-----------------------------
id required in body for Put
Add/Update genre with request body = api/genres/


                    EventPerformer Routes:
Get, Delete
-----------------------------
Show all eventperformers = api/eventperformers/
Show all events with performer = api/eventperformers?performer={id}
Show all of an events performers = api/eventperformers?event={id}
Check if event has a performer = api/eventperformers?event={id}&performer={id} | Will return json { ok : [] } in case false
Show/Delete eventperformer = api/eventperformers/<id>

Post, Put Routes
-----------------------------
id required in body for Put
event and performer ids must exist
date is in the format YYYY-MM-DDThh:mm e.g 2023-01-01T23:59
Add/Update eventperformer with request body = api/eventperformers/


                    EventGenre Routes:
Get, Delete
-----------------------------
Show all eventgenres = api/eventgenres/
Show all events with genre = api/eventgenres?genre={name}
Show all of an events genres = api/eventgenres?event={id}
Check if event has a genre = api/eventgenres?event={id}&genre={name} | Will return json { ok : [] } in case false
Show/Delete eventgenre = api/eventgenres/<id>

Post, Put Routes
-----------------------------
id required in body for Put
event id and genre name must exist
Add/Update eventgenre with request body = api/eventgenres/


                    Event Routes:
Get, Delete
-----------------------------
Show all events = api/events/
Show all of a venues events = api/events?venue={id}
Show/Delete event = api/events/<id>

Post, Put Routes
-----------------------------
id required in body for Put
venue id must exist
date is in the format YYYY-MM-DDThh:mm e.g 2023-01-01T23:59
Add/Update event with request body = api/events/

'''

urlpatterns = [
    
    re_path(r'^users/?$', apiviews.UserApi, name="all-users"),
    re_path(r'^users/(?P<username>\w+)', apiviews.UserApi, name="one-user"),

    re_path(r'^addresses/?$', apiviews.AddressApi, name="all-addresses"),
    re_path(r'^addresses/(?P<id>[0-9]+)', apiviews.AddressApi, name="one-address"),

    re_path(r'^offers/?$', apiviews.OfferApi, name="all-offers"),
    re_path(r'^offers/(?P<id>[0-9]+)', apiviews.OfferApi, name="one-offer"),

    re_path(r'^venues/?$', apiviews.VenueApi, name="all-venues"),
    re_path(r'^venues/(?P<id>[0-9]+)', apiviews.VenueApi, name="one-venue"),

    re_path(r'^areas/?$', apiviews.AreaApi, name="all-areas"),
    re_path(r'^areas/(?P<id>[0-9]+)', apiviews.AreaApi, name="one-area"),

    re_path(r'^prices/?$', apiviews.PriceApi, name="all-prices"),
    re_path(r'^prices/(?P<id>[0-9]+)', apiviews.PriceApi, name="one-price"),

    re_path(r'^performers/?$', apiviews.PerformerApi, name="all-perfomers"),
    re_path(r'^performers/(?P<id>[0-9]+)', apiviews.PerformerApi, name="one-performer"),

    re_path(r'^genres/?$', apiviews.GenreApi, name="all-genres"),
    re_path(r'^genres/(?P<id>[0-9]+)', apiviews.GenreApi, name="one-genre"),

    re_path(r'^eventperformers/?$', apiviews.EventPerformerApi, name="all-eventperformers"),
    re_path(r'^eventperformers/(?P<id>[0-9]+)', apiviews.EventPerformerApi, name="one-eventperformer"),

    re_path(r'^eventgenres/?$', apiviews.EventGenreApi, name="all-eventgenres"),
    re_path(r'^eventgenres/(?P<id>[0-9]+)', apiviews.EventGenreApi, name="one-eventgenre"),

    re_path(r'^events/?$', apiviews.EventApi, name="all-events"),
    re_path(r'^events/(?P<id>[0-9]+)', apiviews.EventApi, name="one-event"),
    
]
