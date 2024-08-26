from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materialApoio.api.views import VideoYoutubeViewSet,ArquivoPdfViewSet, MaterialApoioViewSet, ArquivoPdfViewSet, MaterialApoioSearchView

router = DefaultRouter()

router.register(r'material-apoio', MaterialApoioViewSet)
router.register(r'videos-youtube', VideoYoutubeViewSet)
router.register(r'arquivos-pdf', ArquivoPdfViewSet)

urlpatterns = [
    path("buscar-material-apoio/", MaterialApoioSearchView.as_view(), name="buscar-material-apoio"),
    path('', include(router.urls)),
]