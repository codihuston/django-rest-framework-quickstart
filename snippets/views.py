import pdb;
from django.contrib.auth.models import User, Permission, Group
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.permissions import CanRetrieveSnippet
from snippets.serializers import SnippetSerializer, UserSerializer, PermissionSerializer, GroupSerializer

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
    Custom actions, get snippets owned by this user @ /users/1/snippets
    """
    user = self.get_object()
    return Response(UserSerializer(user, context={'request':request}).data['snippets'])

  @action(detail=True, methods=['get'])
  def groups(self, request, *args, **kwargs):
    """
    Custom actions, get this user's groups @ /users/1/groups
    """
    user = self.get_object()
    return Response(GroupSerializer(user.groups.all(), many=True, context={'request':request}).data)

  @action(detail=True, methods=['get'])
  def permissions(self, request, *args, **kwargs):
    """
    Custom actions, get this user's permissions @ /users/1/permissions
    """
    user = self.get_object()
    return Response(UserSerializer(user, context={'request':request}).data['permissions'])

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]
  queryset = Permission.objects.all()
  serializer_class = PermissionSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
  renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer]
  queryset = Group.objects.all()
  serializer_class = GroupSerializer

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
      return [permission() for permission in permission_classes]

  def perform_create(self, serializer):
    # perhaps the user id is not included in the request to create this
    # snippet; we don't need it, since the request object already has
    # the user object on it. To solidify this relationship, we can
    # pass this into the save method of the serializer. Since the 'owner'
    # field is mapped to the user model in the snippet model, the serializer
    # understands that we are assigning this user to this snippet
    serializer.save(owner=self.request.user)
      
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