from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Create your views here.

class SnippetList(generics.ListCreateAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]