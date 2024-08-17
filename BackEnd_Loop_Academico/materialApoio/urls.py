from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materialApoio.api.views import VideoYoutubeViewSet,ArquivosPdfViewSet

router = DefaultRouter()

router.register(r'video-youtube', VideoYoutubeViewSet, basename='video-youtube')
router.register(r'arquivos', ArquivosPdfViewSet, basename='arquivos')

urlpatterns = [
    path('', include(router.urls)),
]