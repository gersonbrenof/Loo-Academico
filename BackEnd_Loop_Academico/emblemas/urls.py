from django.urls import path
from emblemas.api.views import ListaEmblemaALunoView, ListaTodosEmblemasView, DesbloquearEmblemaView

urlpatterns = [
    path('lista-emblema/', ListaEmblemaALunoView.as_view(), name='lista_emblemas_aluno'),
    path("lista-todos-emblema/", ListaTodosEmblemasView.as_view(), name="lista-todos-emblemas"),
    path("desbloquer-emblema/", DesbloquearEmblemaView.as_view(), name="desbloquear-emblemas")
]