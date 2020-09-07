from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippet, LANGUAGE_CHOICES, SYTLE_CHOICES

class UserSerializer(serializers.ModelSerializer):
  snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

  class Meta:
    model = User
    fields = ['id', 'username', 'snippets']

class SnippetSerializer(serializers.ModelSerializer):
  # now that snippets are associated with the user that created them 
  # (see views/SnippetList), we need to reflect that here by adding this field
  # The untyped `ReadOnlyField` will only be used for serializing, but never
  # when mutating a model instance
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Snippet
    # also add owner here
    fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']