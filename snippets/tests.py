from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser, User
from snippets.models import Snippet
import json

# Create your tests here.
class UserTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create(username="test")

  def test_user_exists(self):
    user = User.objects.get(username="test")
    self.assertEqual(user.username, "test")

class UserViewSetTestCase(TestCase):
  def setUp(self):
    self.client = Client()

  def test_details_with_anon_user(self):
    response = self.client.get('/users')
    self.assertEqual(response.status_code, 200)

class SnippetViewSetTestCase(TestCase):
  def setUp(self):
    self.password = "123"
    self.client = Client()
    self.user = User.objects.create(username="test_user")
    self.user.set_password(self.password)
    self.user.save()

  def test_put_snippet_with_anon_user(self):
    # create a snippet
    snippet = Snippet.objects.create(code="testcode", owner=self.user)

    # update a snippet (without login)
    response = self.client.put('/snippets/' + str(snippet.id), {"code":"abcdefg"})
    self.assertEqual(response.status_code, 403)

  def test_put_snippet_as_owner(self):
    #login
    login = self.client.login(username=self.user.username, password=self.password)
    self.assertEqual(login, True)
    
    # create a snippet
    snippet = Snippet.objects.create(code="testcode", owner=self.user)

    # update a snippet
    response = self.client.put('/snippets/' + str(snippet.id), {"code":"abcdefg"}, content_type="application/json")
    self.assertEqual(response.status_code, 200)

