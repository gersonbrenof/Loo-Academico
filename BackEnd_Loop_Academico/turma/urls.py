from django.urls import path, include
from turma.api.views import AtualizarMinhaTurmaView
from  rest_framework.routers import DefaultRouter
router = DefaultRouter()


urlpatterns = [
   path('', include(router.urls)),
   path('vincular-codico/', AtualizarMinhaTurmaView.as_view(), name='atualizar-minha-turma'),

]