from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from contas.api.views import AlunoRegisterAPI, login_aluno
from exercicio.api.views import CompiladorViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'compiladores', CompiladorViewSet)



urlpatterns = [
    # para gere a documentaçao da api 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # ------------------------------------------------------------------------------------------------


    path('admin/', admin.site.urls),
    path('Api/Cadastrar/', AlunoRegisterAPI.as_view(), name='aluno-register'),
    path('Api/login/', login_aluno, name='login-aluno'),

    path('turma/', include('turma.urls')),
    path('Forum', include('forum.urls')),


    path('', include(router.urls),)
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)