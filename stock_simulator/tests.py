from django.test import TestCase
import pytest
from . models import User
from . helpers import lookup, usd
from django.urls import reverse
# Create your tests here.
@pytest.mark.django_db
def test_user_creation():
    User.objects.create_user(username='john', password='1234')
    assert User.objects.count() == 1

def test_lookup():
    symbol = 'NFLX'
    assert lookup(symbol) != None

def test_usd():
    assert usd(100) == '$100.00'