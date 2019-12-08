import unittest
from unittest.mock import patch, MagicMock

import requests

from geoservice.tasks import geocode, reverse_geocode


class TestGeocodeTask(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('geoservice.tasks.geocoder.osm')

    def tearDown(self):
        self.patcher.stop()

    @patch('geoservice.tasks.geocode.update_state')
    def test_return_valid_coordinates(self, update_state):
        mock = self.patcher.start()
        gt = (55.674146, 12.569553)
        geocode_task = MagicMock()
        setattr(geocode_task, 'ok', True)
        setattr(geocode_task, 'json', {'lat': gt[0], 'lng': gt[1]})
        mock.return_value = geocode_task

        address = "H. C. Andersens Blvd. 27, 1553 København V, Denmark"
        result = geocode(address)

        self.assertEqual(result[0], gt[0])
        self.assertEqual(result[1], gt[1])

    @patch('geoservice.tasks.geocode.update_state')
    def test_cannot_find_coordinates(self, update_state):
        mock = self.patcher.start()
        gt = 'ERROR - No results found'
        geocode_task = MagicMock()
        setattr(geocode_task, 'ok', False)
        setattr(geocode_task, 'json', {'status': gt})
        mock.return_value = geocode_task

        address = "H. C. Andersens Blvd. 27, 1553 København V, Denmark"
        result = geocode(address)

        self.assertEqual(result, gt)

    @patch('geoservice.tasks.geocode.update_state')
    @patch('geoservice.tasks.geocode.retry')
    def test_connection_error(self, update_state, retry):
        mock = self.patcher.start()
        mock.side_effect = requests.exceptions.ConnectionError

        address = "H. C. Andersens Blvd. 27, 1553 København V, Denmark"
        geocode(address)

        retry.assert_called()


class ReverseTestGeocodeTask(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('geoservice.tasks.geocoder.osm')

    def tearDown(self):
        self.patcher.stop()

    @patch('geoservice.tasks.reverse_geocode.update_state')
    def test_return_valid_coordinates(self, update_state):
        mock = self.patcher.start()

        gt = "H. C. Andersens Blvd. 27, 1553 København V, Denmark"
        reverse_geocode_task = MagicMock()
        setattr(reverse_geocode_task, 'ok', True)
        setattr(reverse_geocode_task, 'json', {'address': gt})
        mock.return_value = reverse_geocode_task

        coord = [55.674146, 12.569553]
        result = reverse_geocode(coord)

        self.assertEqual(result, gt)

    @patch('geoservice.tasks.reverse_geocode.update_state')
    def test_cannot_find_coordinates(self, update_state):
        mock = self.patcher.start()
        gt = 'ERROR - No results found'
        reverse_geocode_task = MagicMock()
        setattr(reverse_geocode_task, 'ok', False)
        setattr(reverse_geocode_task, 'json', {'status': gt})
        mock.return_value = reverse_geocode_task

        coord = [55.674146, 12.569553]
        result = reverse_geocode(coord)

        self.assertEqual(result, gt)

    @patch('geoservice.tasks.reverse_geocode.update_state')
    @patch('geoservice.tasks.reverse_geocode.retry')
    def test_connection_error(self, update_state, retry):
        mock = self.patcher.start()
        mock.side_effect = requests.exceptions.ConnectionError

        coord = [55.674146, 12.569553]
        reverse_geocode(coord)

        retry.assert_called()


if __name__ == '__main__':
    unittest.main()
