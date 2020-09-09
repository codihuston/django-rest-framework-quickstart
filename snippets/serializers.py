from rest_framework import serializers
from django.contrib.auth.models import User, Permission, Group
from snippets.models import Snippet, LANGUAGE_CHOICES, SYTLE_CHOICES


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
  # now that snippets are associated with the user that created them 
  # (see views/SnippetList), we need to reflect that here by adding this field
  # The untyped `ReadOnlyField` will only be used for serializing, but never
  # when mutating a model instance. We specify which value to display here.
  # Note that "owner" is set to a user instance as defined on the Snippet model
  #owner = serializers.ReadOnlyField(source='owner.username')
  # replace the line above with the line below to get href to user instead
  owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
  highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

  class Meta:
    model = Snippet
    # also add owner here
    fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner', 'highlight']


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Permission
    fields = ['id', 'codename', 'name']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ['id', 'name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
  # implement baked-in mapped relationships
  snippets = SnippetSerializer(many=True)
  groups = GroupSerializer(many=True)
  # implement a custom field
  permissions = serializers.SerializerMethodField()

  def get_permissions(self, obj):
    """
    Get ALL user's permissions (including group permissions!)
    OR together two querysets: https://docs.djangoproject.com/en/3.0/ref/models/querysets/
    De-duplicate perms that may exist on both the user and group
    """
    permissions = list(set(Permission.objects.filter(group__user=obj) | obj.user_permissions.all()))
    return PermissionSerializer(permissions, many=True).data

  class Meta:
    model = User
    fields = ['id', 'username', 'snippets', 'groups', 'permissions']
