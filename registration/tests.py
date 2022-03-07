from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import RequestsClient
from registration.views import *
from registration.models import RegisteredUsers


# Create your tests here.
class SigninTest(TestCase):

    def setUp(self):

        self.client = RequestsClient()

    def test_create_user(self):
        view_user = Register.as_view()
        user = {"email": "testemail@mail.com",
                "password": "testpassword", "username": "testuser"}
        response = self.client.post(
            "http://localhost:8000/register/", json=user)
        assert response.status_code == 200

    def test_duplicate_user(self):
        view_user = Register.as_view()
        user1 = {"email": "testemail@mail.com",
                 "password": "testpassword", "username": "testuser"}  # register user
        user2 = {"email": "testemail1@mail.com",
                 "password": "testpassword", "username": "testuser"}  # duplicate username
        user3 = {"email": "testemail@mail.com",
                 "password": "testpassword", "username": "testuser1"}  # duplicate email

        response1 = self.client.post(
            "http://localhost:8000/register/", json=user1)
        response2 = self.client.post(
            "http://localhost:8000/register/", json=user2)
        response3 = self.client.post(
            "http://localhost:8000/register/", json=user3)

        assert response1.status_code == 200
        assert response2.status_code == 400
        assert response3.status_code == 400
