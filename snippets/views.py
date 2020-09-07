from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer

class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class SnippetList(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]

  def perform_create(self, serializer):
    """
    We need to override this, because as incoming data comes in, we need
    to associate it with a user. With the line below, the '.create()' method
    in the serializer will now be passed an additional 'owner' field, along
    with the validated data from the request.

    After this change, now you need to update the serializer to handle this.
    """
    serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]