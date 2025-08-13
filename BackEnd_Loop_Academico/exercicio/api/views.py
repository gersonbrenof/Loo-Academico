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
class DicaAlunoViewSet(viewsets.ModelViewSet):
    queryset = DicaAluno.objects.all()
    serializer_class = DicaAlunoSerilizer
    permission_classes = [IsAuthenticated]

    http_method_names = ['get']  # limita apenas ao GET
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
    
    
    def post(self, request, exercicio_id):
        try:
            exercicio = Exercicio.objects.get(id=exercicio_id)
        except Exercicio.DoesNotExist:
            return JsonResponse({'erro': 'Exercício não encontrado.'}, status=404)

        data = request.data.copy()
        data['exercicio'] = exercicio.id

        serializer = ResponderExercicioSerializer(data=data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        aluno = request.user.aluno
        codigo = serializer.validated_data['codigoDoExercicio']

        try:
            with open('temp.c', 'w') as f:
                f.write(codigo)

            compile = subprocess.run(['gcc', 'temp.c', '-o', 'temp.out'], capture_output=True, text=True)
            if compile.returncode != 0:
                return JsonResponse({'erro': 'Erro de compilação', 'detalhes': compile.stderr}, status=400)

            run = subprocess.run(
                ['./temp.out'],
                input=exercicio.entradaExemplo,
                capture_output=True,
                text=True,
                timeout=5
            )

            saida_obtida = run.stdout.strip()
            saida_esperada = exercicio.saidaExemplo.strip()
            resultado = 'Correto' if saida_obtida == saida_esperada else 'Incorreto'
            pontuacao = 10 if resultado == 'Correto' else 0

        except subprocess.TimeoutExpired:
            return JsonResponse({'erro': 'Tempo de execução excedido'}, status=400)

        except Exception as e:
            return JsonResponse({'erro': 'Erro ao executar código', 'detalhes': str(e)}, status=400)

        finally:
            for f in ['temp.c', 'temp.out']:
                if os.path.exists(f):
                    os.remove(f)

        resposta, created = ResponderExercicio.objects.update_or_create(
            exercicio=exercicio,
            aluno=aluno,
            defaults={
                'codigoDoExercicio': codigo,
                'resultado': resultado,
                'pontuacao': pontuacao,
            }
        )

        desempenho, _ = Desempenho.objects.get_or_create(aluno=aluno, turma=aluno.turma)
        desempenho.total_respostas += 1
        desempenho.tentativas += 1
        if resultado == 'Correto':
            desempenho.respostas_corretas += 1
            desempenho.pontuacaoAluno = (desempenho.pontuacaoAluno or 0) + pontuacao
        desempenho.save()

        exercicio.status = 'Respondido'
        exercicio.save()

        return Response({
            'mensagem': 'Resposta enviada com sucesso.',
            'resultado': resultado,
            'pontuacao': pontuacao
        }, status=201)