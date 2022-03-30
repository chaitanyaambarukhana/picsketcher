from django.test import TestCase
# Create your tests here.
import json


class ImageTestCase(TestCase):
    def setUp(self):
        c
    def test_filter_image(self):
        self.bytes = self.data['data']['bytes']
        response = self.client.post("/upload/", data={
            'image_bytes': self.bytes
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[
                         'success'], True)