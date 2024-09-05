from django.urls import path, include
from rest_framework.routers import DefaultRouter
from duvidas.api.views import DuvidasViewSet, ExibirDuvidasView

router = DefaultRouter()
router.register(r'duvidas', DuvidasViewSet)

urlpatterns = [
    path("ExibirDuvidas/",ExibirDuvidasView.as_view(), name="exebirDuvidas"),
    path('', include(router.urls)),
]