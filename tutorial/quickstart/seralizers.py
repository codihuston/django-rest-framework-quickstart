"""
Serializers are used for data representation.
"""
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSeralizer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ['url', 'name']