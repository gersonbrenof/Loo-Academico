from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercicio.api.views import ExercicioViewSet, ResponderExercicioView, ListaExercicoViewSet, ExercicioStatusViewSet
from exercicio.api.views import ListaExericioStatusViewSet, DicaAlunoViewSet
# Criar um roteador para o ViewSet
router = DefaultRouter()
router.register(r'exercicios', ExercicioViewSet, basename='exercicio')
router.register(r'status-do-exercicio', ExercicioStatusViewSet, basename='status-exercicio')
router.register(r'lista-exercicio', ListaExercicoViewSet, basename="lista-exercicio")
router.register(r'status-da-lista-exercicio', ListaExericioStatusViewSet, basename="status-lista-exercicio")
router.register(r'dicas', DicaAlunoViewSet, basename='dicas')
urlpatterns = [
   
   path('exercicio/responder-exercicio/<int:exercicio_id>/', ResponderExercicioView.as_view()),
   # path('DicaAluno/', DicaALunoListView.as_view(), name='dicaaluno' ),
   # path('dicas/aluno/<int:id>/', DicaALunoListByIdView.as_view(), name='dicas-aluno-id'),
   path('', include(router.urls)),
]