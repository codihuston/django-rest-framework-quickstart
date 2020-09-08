from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.permissions import CanRetrieveSnippet
from snippets.serializers import SnippetSerializer, UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
  })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `detail` actions
  """
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]
  queryset = User.objects.all()
  serializer_class = UserSerializer

  @action(detail=True, methods=['get'])
  def snippets(self, request, *args, **kwargs):
    """
    Custom actions, get snippets owned by this user
    """
    snippets = self.get_object()
    return Response(UserSerializer(snippets, context={'request':request}).data['snippets'])

class SnippetViewSet(viewsets.ModelViewSet):
  """
  This viewset automatically provides `list`, `create`, `retrieve`,
  `update`, and `destroy` actions.

  Additionally, we provide the extra `highlight` action
  """
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer

  def get_permissions(self):
      """
      Instantiates and returns the list of permissions that this view requires.
      """
      permission_classes = []
      if self.action == 'retrieve':
        permission_classes = [permissions.IsAuthenticated, CanRetrieveSnippet]
        print(permission_classes)
      return [permission() for permission in permission_classes]
      
  @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
  def highlight(self, request, *args, **kwargs):
    """
    Custom actions respond to GET by default; use the methods= kwarg if you
    want to change that (to POST, for example).

    If you want to change the URL path, you can provide the `url_path` kwarg
    to change it.
    """
    snippet = self.get_object()
    return Response(snippet.highlighted)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)