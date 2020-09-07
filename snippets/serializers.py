from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippet, LANGUAGE_CHOICES, SYTLE_CHOICES

class UserSerializer(serializers.HyperlinkedModelSerializer):
  snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

  class Meta:
    model = User
    fields = ['id', 'username', 'snippets']

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