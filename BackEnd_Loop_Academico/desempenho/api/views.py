from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from desempenho.models import Desempenho
from desempenho.api.serializers import DesempenhoSerializer
from rest_framework.exceptions import PermissionDenied
from exercicio.models import ResponderExercicio
class DesempenhoDetailView(generics.RetrieveAPIView):
    serializer_class = DesempenhoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        aluno = self.request.user.aluno
        if aluno is None:
            raise PermissionDenied("Usuário não está associado a um aluno.")

        # Verifique se o aluno está associado a uma turma
        if aluno.turma is None:
            raise PermissionDenied("Aluno não está associado a uma turma.")

        # Obtém o desempenho do aluno na turma
        desempenho = Desempenho.objects.filter(aluno=aluno, turma=aluno.turma).first()
        
        if not desempenho:
            # Crie um novo desempenho se não existir
            desempenho = Desempenho(
                aluno=aluno,
                turma=aluno.turma,
                pontuacaoAluno=0,
                tentativas=0,
                status='Não Responido e Não enviado',
                total_respostas=0,
                respostas_corretas=0
            )
            desempenho.save()

        # Atualize o status do desempenho baseado nas respostas enviadas
        self.atualizar_status_desempenho(desempenho)
        
        return desempenho
    
    def atualizar_status_desempenho(self, desempenho):
        # Filtra todas as respostas do aluno (não relacionado à turma ou exercício específico)
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

        desempenho.save()