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
    print(view.action)
    if view.action in ['retrieve']:
      return request.user.has_perm("snippets.view_snippet")
    return True

  def has_object_permission(self, request, view, obj):    
    # write permissions are only allowed to the ownwer of the snippet
    print(view.action)
    if view.action in ['retrieve']:
      return obj.owner == request.user
    return True


