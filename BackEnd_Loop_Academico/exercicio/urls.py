from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercicio.api.views import ExercicioViewSet, ResponderExercicioView, ListaExercicoViewSet, ExercicioStatusViewSet
from exercicio.api.views import ListaExericioStatusViewSet, DicaALunoListView
# Criar um roteador para o ViewSet
router = DefaultRouter()
router.register(r'exercicios', ExercicioViewSet, basename='exercicio')
router.register(r'status-do-exercicio', ExercicioStatusViewSet, basename='status-exercicio')
router.register(r'lista-exercicio', ListaExercicoViewSet, basename="lista-exercicio")
router.register(r'status-da-lista-exercicio', ListaExericioStatusViewSet, basename="status-lista-exercicio")

urlpatterns = [
   
    path('responder-exercicio/', ResponderExercicioView.as_view(), name='responder_exercicio'),
    path('DicaAluno/', DicaALunoListView.as_view(), name='dicaaluno' ),
     path('', include(router.urls)),
]