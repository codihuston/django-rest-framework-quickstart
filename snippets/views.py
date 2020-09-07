
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Create your views here.

class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]

  """
  List all code snippets, or create a new snippet
  """
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)