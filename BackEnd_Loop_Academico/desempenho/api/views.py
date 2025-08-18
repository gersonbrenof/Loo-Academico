from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from desempenho.models import Desempenho
from desempenho.api.serializers import DesempenhoSerializer, ListaDesempenhoSerializer, ListaExercicio, Exercicio, ResponderExercicio
from rest_framework.exceptions import PermissionDenied
from exercicio.models import ResponderExercicio
class DesempenhoDetailView(generics.RetrieveAPIView):
    serializer_class = DesempenhoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        aluno = self.request.user.aluno
        if aluno is None:
            raise PermissionDenied("Usuário não está associado a um aluno.")

        if aluno.turma is None:
            raise PermissionDenied("Aluno não está associado a uma turma.")

        desempenho, created = Desempenho.objects.get_or_create(
            aluno=aluno,
            turma=aluno.turma,
            defaults={
                'pontuacaoAluno': 0,
                'tentativas': 0,
                'status': 'Não Respondido e Não enviado',
                'total_respostas': 0,
                'respostas_corretas': 0
            }
        )

        # Chame a função de atualização de status do desempenho
        self.atualizar_status_desempenho(desempenho)

        return desempenho

    def atualizar_status_desempenho(self, desempenho):
        total_respostas = ResponderExercicio.objects.filter(
            aluno=desempenho.aluno
        ).count()

        respostas_corretas = ResponderExercicio.objects.filter(
            aluno=desempenho.aluno,
            resultado='Correto'
        ).count()

        desempenho.total_respostas = total_respostas
        desempenho.respostas_corretas = respostas_corretas

        if total_respostas == 0:
            desempenho.status = 'Não Respondido e Não enviado'
        elif respostas_corretas == total_respostas:
            desempenho.status = 'Resolução Correta'
        else:
            desempenho.status = 'Resolução Incorreta'

        # Salve o desempenho atualizado
        desempenho.save()
class DesempenhoListaView(generics.ListAPIView):
    serializer_class = ListaDesempenhoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna todas as listas de exercícios relacionadas ao aluno logado.
        """
        aluno = getattr(self.request.user, 'aluno', None)
        if aluno is None:
            return ListaExercicio.objects.none()

        # Retorna todas as listas que têm exercícios (relacionadas ao aluno pela turma)
        return ListaExercicio.objects.all().prefetch_related('exercicios')
    
    def get_serializer_context(self):
        """
        Passa o request no contexto para o serializer (necessário para calcular o status dos exercícios).
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context