
import geocoder
import requests
from celery.exceptions import MaxRetriesExceededError

from geoservice import create_app, create_celery


app = create_app()
celery = create_celery(app)


@celery.task(bind=True, max_retries=3)
def geocode(self, address):
    """Get the coordinates of the given address using OpenStreetMap"""
    try:
        self.update_state(state='STARTED')
        g = geocoder.osm(address)
        if g.ok:
            latitude = g.json['lat']
            longitude = g.json['lng']

            return latitude, longitude
        else:
            return g.json['status']
    except requests.exceptions.ConnectionError:
        try:
            self.retry(countdown=2 ** self.request.retries)
        except MaxRetriesExceededError:
            return {'error': 'connect to the server failed'}
    except KeyError:
        return 'osm API failed'


@celery.task(bind=True, max_retries=3)
def reverse_geocode(self, coordinate):
    """Get the address of the given coordinate using OpenStreetMap"""
    try:
        self.update_state(state='STARTED')
        g = geocoder.osm(coordinate, method='reverse')
        if g.ok:
            address = g.json['address']
            return address
        else:
            return g.json['status']
    except requests.exceptions.ConnectionError:
        try:
            self.retry(countdown=2 ** self.request.retries)
        except MaxRetriesExceededError:
            return 'connect to the server failed'
    except KeyError:
        return 'osm API failed'
