from django.test import TestCase

from django.contrib import auth
from .models import *

class AuthTestCase(TestCase):
    def setUp(self):
        self.u = MyAccountManager.objects.create_user('x@gmail.com', 'x', 'x', 'x', 'x')
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.save()

    def testLogin(self):
        self.client.login(email='x@x.com', password='x')