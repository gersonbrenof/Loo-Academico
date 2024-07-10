from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ValidarCodicoTurmaSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def valida_codico(request):
    serializer = ValidarCodicoTurmaSerializer(data=request.data)
    if serializer.is_valid():
        return Response({"message": "Código válido."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)