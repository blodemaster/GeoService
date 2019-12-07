import geocoder
import requests

from geoservice import create_app, create_celery


app = create_app()
celery = create_celery(app)


@celery.task()
def geocode(address):
    """Get the coordinates of the given address using OpenStreetMap"""
    try:
        g = geocoder.osm(address)

        latitude = g.json['lat']
        longitude = g.json['lng']
        return latitude, longitude
    except requests.exceptions.ConnectionError:
        return 'Cannot connect to server'
    except KeyError:
        return 'osm API failed'


@celery.task()
def reverse_geocode(coordinate):
    """Get the address of the given coordinate using OpenStreetMap"""
    try:
        g = geocoder.osm(coordinate, method='reverse')
        address = g.json['address']
        return address
    except requests.exceptions.ConnectionError:
        return 'Cannot connect to server'
    except KeyError:
        return 'osm API failed'
