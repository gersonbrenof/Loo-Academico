from django.urls import path, include
from rest_framework.routers import DefaultRouter
from duvidas.api.views import DuvidasViewSet

router = DefaultRouter()
router.register(r'duvidas', DuvidasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]