from django.urls import path
from turma.api.views import valida_codico
urlpatterns = [
   path("valida-codico/", valida_codico, name="validacodico")
]