import io
import sys
import logging
from datetime import datetime
import os
import subprocess
from django.http import JsonResponse
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from exercicio.models import ResponderExercicio, Exercicio
from exercicio.api.serializers import ResponderExercicioSerializer, ExercicioSerializer, ListaExercicioSerializer
from exercicio.api.serializers import Sintaxe, SintaxeSerializer, ListaExercicio, ExercicioStatusSerializer, ListaExercicioStatusSerilaizer
from exercicio.api.serializers import DicaAlunoSerilizer, DicaAluno
from contas.models import Aluno, User
from desempenho.models import Desempenho
from datetime import datetime, timedelta
class DicaALunoListView(generics.ListAPIView):
    queryset = DicaAluno.objects.all()
    serializer_class = DicaAlunoSerilizer
    permission_classes = [IsAuthenticated]


class ExercicioStatusViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExercicioStatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Exercicio.objects.all()

        try:
            aluno = Aluno.objects.get(user=self.request.user)
            respostas = ResponderExercicio.objects.filter(aluno=aluno)
            exercicios_ids = respostas.values_list('exercicio_id', flat=True)

            # Marcar todos os exercícios respondidos pelo aluno
            queryset = Exercicio.objects.all()
            for exercicio in queryset:
                if exercicio.id in exercicios_ids:
                    exercicio.status = 'Respondido'
                else:
                    exercicio.status = 'Não Respondido'
            
            return queryset

        except Aluno.DoesNotExist:
            return Exercicio.objects.none()
class ListaExericioStatusViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class =  ListaExercicioStatusSerilaizer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ListaExercicio.objects.all()

        try:
            aluno = self.request.user.aluno
            lista_exercicios = ListaExercicio.objects.all()

            # Atualiza o status das listas de exercícios com base nas respostas
            for lista in lista_exercicios:
                lista.verificar_respostas()

            # Filtra as listas de exercícios associadas ao aluno
            return ListaExercicio.objects.all()

        except Aluno.DoesNotExist:
            return ListaExercicio.objects.none()
class ListaExercicoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ListaExercicioSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ListaExercicio.objects.all()

        try:
            aluno = Aluno.objects.get(user=self.request.user)
            return ListaExercicio.objects.all()

        except Aluno.DoesNotExist:
            return ListaExercicio.objects.none()
class ExercicioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset()

    def perform_create(self, serializer):
        exercicio = serializer.save()
        exercicio.lista.atualizar_total_exercicios()

    def perform_destroy(self, instance):
        lista = instance.lista
        instance.delete()
        lista.atualizar_total_exercicios()
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

            try:
                exercicio = Exercicio.objects.get(id=exercicio_id)
            except Exercicio.DoesNotExist:
                return JsonResponse({'status': 'Erro', 'detail': 'Exercício não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            entrada = exercicio.entradaExemplo
            saida_esperada = exercicio.saidaExemplo

            try:
                with open('temp_program.c', 'w') as file:
                    file.write(codigo_aluno)

                compile_process = subprocess.run(
                    ['gcc', 'temp_program.c', '-o', 'temp_program'],
                    capture_output=True,
                    text=True
                )
                
                if compile_process.returncode != 0:
                    return JsonResponse({'status': 'Erro ao compilar código', 'error': compile_process.stderr}, status=status.HTTP_400_BAD_REQUEST)

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

                pontuacao = 10 if saida_aluno == saida_esperada.strip() else 0
                resultado = 'Correto' if pontuacao > 0 else 'Incorreto'
                
                resposta_existente = ResponderExercicio.objects.filter(exercicio=exercicio, aluno=aluno).first()
                
                if resposta_existente:
                    resposta_existente.codigoDoExercicio = codigo_aluno
                    resposta_existente.resultado = resultado
                    resposta_existente.pontuacao = pontuacao
                    resposta_existente.save()
                else:
                    resposta_existente = ResponderExercicio(
                        exercicio=exercicio,
                        aluno=aluno,
                        codigoDoExercicio=codigo_aluno,
                        resultado=resultado,
                        pontuacao=pontuacao
                    )
                    resposta_existente.save()

                # Atualizar ou criar o desempenho
                desempenho, created = Desempenho.objects.get_or_create(aluno=aluno, turma=aluno.turma)

                if not created:
                    desempenho.total_respostas += 1
                    if pontuacao > 0:
                        desempenho.respostas_corretas += 1
                    desempenho.pontuacaoAluno = (desempenho.pontuacaoAluno or 0) + pontuacao
                else:
                    desempenho.total_respostas = 1
                    desempenho.respostas_corretas = 1 if pontuacao > 0 else 0
                    desempenho.pontuacaoAluno = pontuacao

                # Atualizar outros campos do desempenho
                desempenho.tentativas += 1
                desempenho.save()

                exercicio.status = 'Respondido' if ResponderExercicio.objects.filter(exercicio=exercicio, aluno=aluno).exists() else 'Não Respondido'
                exercicio.save()

                return JsonResponse({'status': 'Resposta enviada', 'pontuacao': pontuacao, 'resultado': resultado}, status=status.HTTP_201_CREATED)

            finally:
                for filename in ['temp_program.c', 'temp_program']:
                    try:
                        if os.path.exists(filename):
                            os.remove(filename)
                    except Exception as e:
                        print(f"Erro ao remover arquivo {filename}: {e}")
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)