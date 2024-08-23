from django.urls import path, include
from rest_framework.routers import DefaultRouter
from forum.api.views import ForumViewSet, ResponderTopicoViewSet, ForumExibirViewSet

router = DefaultRouter()
router.register(r"ExibirForum", ForumExibirViewSet, basename='exibirforum')
router.register(r"Forum", ForumViewSet, basename="forum")
router.register(r"ResponderTopico", ResponderTopicoViewSet, basename="respondertopico")

urlpatterns = [
    path('', include(router.urls)),
]