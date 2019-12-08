import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import urlencode

from flask import url_for

from geoservice.app import app


class TestGeocode(unittest.TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.patcher = patch('geoservice.app.tasks.geocode.delay')
        self.app = app.test_client()
        self.app.testing = True
        self.task_id = '123456'
        mock = self.patcher.start()

        geocode_task = MagicMock()
        setattr(geocode_task, 'id', self.task_id)
        mock.return_value = geocode_task

    def tearDown(self):
        self.patcher.stop()

    def test_valid_request(self):
        true_address = "H. C. Andersens Blvd. 27, 1553 København V, Denmark"
        query_param = urlencode({"address": true_address})

        response = self.app.get("/geocode?" + query_param)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.headers.get('Location'),
                         url_for('geocode_task_status', task_id=self.task_id, _external=True))

    def test_request_wo_query(self):
        response = self.app.get("/geocode")
        self.assertEqual(response.status_code, 400)


class TestGeocodeTask(unittest.TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.patcher = patch('geoservice.app.tasks.geocode.AsyncResult')
        self.app = app.test_client()
        self.app.testing = True
        self.task_id = '123456'

    def tearDown(self):
        self.patcher.stop()

    def test_valid_response(self):
        mock = self.patcher.start()
        gt = {'task_id': self.task_id, 'state': 'SUCCESS', 'result': [55.674146, 12.569553]}
        geocode_task = MagicMock()
        setattr(geocode_task, 'state', gt['state'])
        setattr(geocode_task, 'info', gt['result'])
        mock.return_value = geocode_task

        url = url_for('geocode_task_status', task_id=self.task_id)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, gt)

    def test_error_response(self):
        mock = self.patcher.start()
        gt = {'task_id': self.task_id, 'state': 'SUCCESS', 'error': 'code 123'}
        geocode_task = MagicMock()
        setattr(geocode_task, 'state', gt['state'])
        setattr(geocode_task, 'info', {'error': gt['error']})
        mock.return_value = geocode_task

        url = url_for('geocode_task_status', task_id=self.task_id)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, gt)

    def test_request_wo_query(self):
        mock = self.patcher.start()
        url = url_for('geocode_task_status', task_id=self.task_id)
        response = self.app.delete(url)
        self.assertEqual(response.status_code, 204)


class TestReverseGeocode(unittest.TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.patcher = patch('geoservice.app.tasks.reverse_geocode.delay')
        self.app = app.test_client()
        self.app.testing = True
        self.task_id = '987654'
        mock = self.patcher.start()

        geocode_task = MagicMock()
        setattr(geocode_task, 'id', self.task_id)
        mock.return_value = geocode_task

    def tearDown(self):
        self.patcher.stop()

    def test_valid_request(self):
        coord = "55.674146,12.569553"
        query_param = urlencode({"coordinate": coord})

        response = self.app.get("/reverse-geocode?" + query_param)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(
            response.headers.get('Location'),
            url_for('reverse_geocode_task_status', task_id=self.task_id, _external=True)
        )

    def test_request_wi_invalid_coord(self):
        coord = "155.674146,12.569553"
        query_param = urlencode({"coordinate": coord})

        response = self.app.get("/reverse-geocode?" + query_param)
        self.assertEqual(response.status_code, 400)

    def test_request_missing_one_coord(self):
        coord = "155.674146"
        query_param = urlencode({"coordinate": coord})

        response = self.app.get("/reverse-geocode?" + query_param)
        self.assertEqual(response.status_code, 400)

    def test_request_wo_query(self):
        response = self.app.get("/reverse-geocode")
        self.assertEqual(response.status_code, 400)


class TestReverseGeocodeTask(unittest.TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.patcher = patch('geoservice.app.tasks.reverse_geocode.AsyncResult')
        self.app = app.test_client()
        self.app.testing = True
        self.task_id = '123456'

    def tearDown(self):
        self.patcher.stop()

    def test_valid_response(self):
        mock = self.patcher.start()
        gt = {'task_id': self.task_id, 'state': 'SUCCESS', 'result': 'copenhagen'}
        geocode_task = MagicMock()
        setattr(geocode_task, 'state', gt['state'])
        setattr(geocode_task, 'info', gt['result'])
        mock.return_value = geocode_task

        url = url_for('reverse_geocode_task_status', task_id=self.task_id)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, gt)

    def test_error_response(self):
        mock = self.patcher.start()
        gt = {'task_id': self.task_id, 'state': 'SUCCESS', 'error': 'code 123'}
        geocode_task = MagicMock()
        setattr(geocode_task, 'state', gt['state'])
        setattr(geocode_task, 'info', {'error': gt['error']})
        mock.return_value = geocode_task

        url = url_for('reverse_geocode_task_status', task_id=self.task_id)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, gt)

    def test_request_wo_query(self):
        mock = self.patcher.start()
        url = url_for('reverse_geocode_task_status', task_id=self.task_id)
        response = self.app.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
