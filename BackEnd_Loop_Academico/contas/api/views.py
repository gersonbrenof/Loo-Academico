from rest_framework.response import Response
from contas.models import Aluno
from contas.api.serializers import  RegisterAlunoSerializer, LoginSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
@permission_classes([AllowAny])

# Aqui e responsavel por realizar o cadastro do aluno
class AlunoRegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterAlunoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Cria o aluno usando o AlunoManager
                user = Aluno.objects.create_user(**serializer.validated_data)

                # Retorna a resposta JSON com o aluno criado, incluindo 'user' como um nó externo
                return Response({
                    "user": {
                        "id": user.id,
                        "nomeAluno": user.nomeAluno,
                        "institucao": user.institucao,
                        "matricula": user.matricula,
                        "email": user.email
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# funçao para fazer o login do aluno
@api_view(['POST'])
@permission_classes([AllowAny])
def login_aluno(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data['tokens'])
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)