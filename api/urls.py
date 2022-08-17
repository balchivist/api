"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework_nested import routers
from balchivist import views

api_router = routers.DefaultRouter()
api_router.register(r'families', views.FamilyV1ViewSet)
api_router.register(r'users', views.UserV1ViewSet)
api_router.register(r'nodes', views.NodeV1ViewSet)
api_router.register(r'tasks', views.TaskV1ViewSet)

datasets_router = routers.NestedSimpleRouter(api_router, r'families', lookup='family')
datasets_router.register(r'datasets', views.DatasetV1ViewSet, basename='datasets')

snapshots_router = routers.NestedSimpleRouter(datasets_router, r'datasets', lookup='dataset')
snapshots_router.register(r'snapshots', views.SnapshotV1ViewSet, basename='snapshots')

nodes_router = routers.NestedSimpleRouter(api_router, r'nodes', lookup='node')
nodes_router.register(r'configs', views.NodeConfigV1ViewSet, basename='configs')

user_router = routers.NestedSimpleRouter(api_router, r'users', lookup='user')
user_router.register(r'watchlists', views.WatchlistV1ViewSet, basename='watchlists')

v1apiurlpatterns = [
    path('', include(api_router.urls)),
    path('', include(datasets_router.urls)),
    path('', include(snapshots_router.urls)),
    path('', include(nodes_router.urls)),
    path('', include(user_router.urls)),
    path('converter', views.ConverterV1View.as_view())
]

# Wire up our API using automatic URL routing
# Additionally, we include login URLs for the browsable API
urlpatterns = [
    path('api/v1/', include(v1apiurlpatterns)),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
