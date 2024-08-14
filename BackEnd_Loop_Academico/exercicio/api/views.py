import io
import sys
import os
import subprocess
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from exercicio.models import ResponderExercicio, Exercicio
from exercicio.api.serializers import ResponderExercicioSerializer, ExercicioSerializer
# class ListaExercicoViewSet:
class ExercicioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()
class ResponderExercicioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResponderExercicioSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            aluno = request.user.aluno
            if aluno is None:
                return JsonResponse({'status': 'Erro', 'detail': 'Usuário não está associado a um aluno.'}, status=status.HTTP_400_BAD_REQUEST)
            
            exercicio_id = serializer.validated_data['exercicio'].id
            codigo_aluno = serializer.validated_data['codigoDoExercicio']
            codicoDoExercicio = serializer.validated_data['codigoDoExercicio']

            try:
                exercicio = Exercicio.objects.get(id=exercicio_id)
            except Exercicio.DoesNotExist:
                return JsonResponse({'status': 'Erro', 'detail': 'Exercício não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            entrada = exercicio.entradaExemplo
            saida_esperada = exercicio.saidaExemplo

            try:
                # Criar arquivos temporários para o código C
                with open('temp_program.c', 'w') as file:
                    file.write(codigo_aluno)

                # Compilar o código C
                compile_process = subprocess.run(
                    ['gcc', 'temp_program.c', '-o', 'temp_program'],
                    capture_output=True,
                    text=True
                )
                
                if compile_process.returncode != 0:
                    return JsonResponse({'status': 'Erro ao compilar código', 'error': compile_process.stderr}, status=status.HTTP_400_BAD_REQUEST)

                # Executar o programa C com timeout
                try:
                    exec_process = subprocess.run(
                        './temp_program',
                        input=entrada,
                        text=True,
                        capture_output=True,
                        timeout=120
                    )
                    saida_aluno = exec_process.stdout.strip()
                except subprocess.TimeoutExpired:
                    return JsonResponse({'status': 'Erro', 'detail': 'Tempo de execução excedido.'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return JsonResponse({'status': 'Erro ao executar código', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Avaliar a saída do aluno
                pontuacao = 10 if saida_aluno == saida_esperada.strip() else 0
                resultado = 'Correto' if pontuacao > 0 else 'Incorreto'
                # Salvar a resposta do exercício
                responder_exercicio = ResponderExercicio(
                    exercicio=exercicio,
                    aluno=aluno,
                    codigoDoExercicio=codicoDoExercicio,
                    resultado=resultado,
                    pontuacao=pontuacao,
                    dataEnvio=request.data.get('dataEnvio')
                )
                responder_exercicio.save()

                # Atualizar o status do exercício para "Respondido"
                exercicio.status = 'R'
                exercicio.save()

                return JsonResponse({'status': 'Resposta enviada', 'pontuacao': pontuacao}, status=status.HTTP_201_CREATED)

            finally:
                # Limpar arquivos temporários
                for filename in ['temp_program.c', 'temp_program']:
                    try:
                        if os.path.exists(filename):
                            os.remove(filename)
                    except Exception as e:
                        print(f"Erro ao remover arquivo {filename}: {e}")
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)