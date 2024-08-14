from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from contas.api.views import AlunoRegisterAPI, LoginView,PerfilViewSet, AtualizarFotoPerfilView
from contas.api.views import ProtectedView

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r"Perfil-aluno",PerfilViewSet, basename="perfil-aluno")





urlpatterns = [
    # para gere a documentaçao da api 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # ------------------------------------------------------------------------------------------------


    path('admin/', admin.site.urls),
    path('api/cadastrar/', AlunoRegisterAPI.as_view(), name='aluno-register'),
    path('Api/login/', LoginView.as_view(), name='login'),
    path('perfil/<int:pk>/atualizar-foto-perfil/', AtualizarFotoPerfilView.as_view(), name='atualizar-foto-perfil'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('turma/', include('turma.urls')),
# forum
    path('Forum', include('forum.urls')),

# duvidas
    path('duvidas/', include('duvidas.urls')),

    # exercico
    path('exercicio/', include('exercicio.urls')),
    path('', include(router.urls),)
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)