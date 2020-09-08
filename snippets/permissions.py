from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit it.
  """
  def has_object_permission(self, request, view, obj):
    # read permissions are allowed to any request
    # so we'll always allow GET, HEAD, or OPTIONS requests
    if request.method in permissions.SAFE_METHODS:
      return True
    
    # write permissions are only allowed to the ownwer of the snippet
    return obj.owner == request.user

class CanRetrieveSnippet(permissions.BasePermission):
  """
  One may only list snippets if they
  - can view snippets AND own the snippet
  """
  def has_permission(self, request, view):
    return request.user.has_perm("snippets.view_snippet")

  def has_object_permission(self, request, view, obj):
    return obj.owner == request.user


