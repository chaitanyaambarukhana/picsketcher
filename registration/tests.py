from django.test import TestCase
# Create your tests here.
import json


class RegisterTestCase(TestCase):
    def setUp(self):
        with open("registration/testData.json") as jsonFile:
            self.data = json.load(jsonFile)
            jsonFile.close()

    def test_home_url(self):
        response = self.client.post("/index/")
        self.assertEqual(response.status_code, 200)

    def test_signup_login(self):
        self.email = self.data['data1']['email']
        self.password = self.data['data1']['password']
        self.firstname = self.data['data1']['firstname']
        self.lastname = self.data['data1']['lastname']
        response = self.client.post("/register/", data={
            'email': self.email,
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[
                         'success'], True, json.loads(response.content)['message'])

        #login
        response_login = self.client.post("/login/", data={
            'email': self.email,
            'password': self.password
        })
        self.assertEqual(response_login.status_code, 200)
        self.assertEqual(json.loads(response_login.content)['success'],True,json.loads(response_login.content)['message'])
        pass
    def test_signup_incorrect_email_format(self):
        self.email = self.data['data2']['email']
        self.password = self.data['data2']['password']
        self.firstname = self.data['data2']['firstname']
        self.lastname = self.data['data2']['lastname']
        response = self.client.post("/register/", data={
            'email': self.email,
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[
                         'success'], False, json.loads(response.content)['message'])

        pass
    def test_signup_incorrect_pwd_format(self):
        self.email = self.data['data3']['email']
        self.password = self.data['data3']['password']
        self.firstname = self.data['data3']['firstname']
        self.lastname = self.data['data3']['lastname']
        response = self.client.post("/register/", data={
            'email': self.email,
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[
                         'success'], False, json.loads(response.content)['message'])

        pass
