from rest_framework import serializers
from django.contrib.auth.models import User, Permission, Group
from snippets.models import Snippet, LANGUAGE_CHOICES, SYTLE_CHOICES


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
  # now that snippets are associated with the user that created them 
  # (see views/SnippetList), we need to reflect that here by adding this field
  # The untyped `ReadOnlyField` will only be used for serializing, but never
  # when mutating a model instance
  owner = serializers.ReadOnlyField(source='owner.username')
  # replace the line above with the line below to get href to user instead
  #owner = serializers.HyperlinkedIdentityField(view_name='user-detail')
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
  snippets = SnippetSerializer(many=True)
  groups = GroupSerializer(many=True)
  user_permissions = PermissionSerializer(many=True)
  #snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

  class Meta:
    model = User
    fields = ['id', 'username', 'snippets', 'groups', 'user_permissions']
