from django.urls import path
from desempenho.api.views import DesempenhoDetailView, DesempenhoListaView

urlpatterns = [
     path('desempenho/', DesempenhoDetailView.as_view(), name='desempenho-detail'),
     path('desempenho-lista/', DesempenhoListaView.as_view(), name='desempenho-lista'),
]