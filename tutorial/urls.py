"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing (since we are using ViewSets,
# we can register them with the router to auto-generate URL configuration for
# the API). If we needed more control over API URLs, we can simply drop
# down to using regular class-based views, and writing the URL conf explicitly.
# Additionally, we include login URLs for the browsable API
urlpatterns = [
  #path('', include(router.urls)),
  path('', include('snippets.urls')),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
