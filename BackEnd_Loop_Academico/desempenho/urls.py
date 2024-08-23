from django.urls import path
from desempenho.api.views import DesempenhoDetailView

urlpatterns = [
     path('desempenho/', DesempenhoDetailView.as_view(), name='desempenho-detail'),
]