from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercicio.api.views import ExercicioViewSet, ResponderExercicioView, ListaExercicoViewSet, SintaxeViewSet

# Criar um roteador para o ViewSet
router = DefaultRouter()
router.register(r'exercicios', ExercicioViewSet, basename='exercicio')
router.register(r'lista-exerccio', ListaExercicoViewSet, basename="lista-exercicio")
router.register(r'sintaxe', SintaxeViewSet, basename='sintaxe')

urlpatterns = [
   
    path('responder-exercicio/', ResponderExercicioView.as_view(), name='responder_exercicio'),
     path('', include(router.urls)),
]