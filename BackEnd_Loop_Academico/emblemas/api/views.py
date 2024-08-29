from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from emblemas.models import Emblema
from emblemas.api.serializers import EmblemaSerializer, EmblemaListaTudoSerializer
from exercicio.models import ResponderExercicio
from contas.models import Aluno
#Lsita os embelma do aluno
class ListaEmblemaALunoView(generics.ListAPIView):
    serializer_class = EmblemaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        aluno = self.request.user.aluno
        
        if aluno is None:
            return Emblema.objects.none()
        
        # Desbloquear emblemas automaticamente para o aluno atual
        self.desbloquear_emblemas(aluno)
        
        # Retornar os emblemas associados ao aluno
        return Emblema.objects.filter(aluno=aluno)

    def verificar_condicoes_para_emblema(self, aluno):
        # Verifica se o cadastro do aluno está completo
        if not aluno.email or not aluno.nomeAluno:
            return False, "Complete seu cadastro para desbloquear emblemas"
        
        # Verifica se o aluno concluiu pelo menos um exercício
        if not ResponderExercicio.objects.filter(aluno=aluno, resultado='Correto').exists():
            return False, "Resolva um exercício para desbloquear emblemas"

        return True, "Todas as condições foram atendidas"

    def desbloquear_emblemas(self, aluno):
        # Filtra apenas os emblemas que ainda não foram desbloqueados para o aluno atual
        emblemas = Emblema.objects.filter(status='nao_desbloqueado', aluno__isnull=True)

        for emblema in emblemas:
            condicoes_atendidas, mensagem = self.verificar_condicoes_para_emblema(aluno)
            if condicoes_atendidas:
                # Vincula o emblema ao aluno e atualiza o status para 'desbloqueado'
                emblema.aluno = aluno
                emblema.status = 'desbloqueado'
                emblema.save()

class ListaTodosEmblemasView(generics.ListAPIView):
    serializer_class = EmblemaListaTudoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Emblema.objects.all()

    

class DesbloquearEmblemaView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        aluno = self.request.user.aluno

        # Verificar e desbloquear emblemas automaticamente
        emblemas_desbloqueados = self.desbloquear_emblemas(aluno)

        if not emblemas_desbloqueados:
            return Response({"detail": "Nenhum emblema desbloqueado. Verifique se você atende aos requisitos."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Emblemas desbloqueados com sucesso!"}, status=status.HTTP_200_OK)

    def verificar_condicoes_para_emblema(self, aluno):
        # Verifica se o cadastro do aluno está completo
        if not aluno.email or not aluno.nomeAluno:
            return False, "Complete seu cadastro para desbloquear emblemas"
        
        # Verifica se o aluno concluiu pelo menos um exercício
        if not ResponderExercicio.objects.filter(aluno=aluno, resultado='Correto').exists():
            return False, "Resolva um exercício para desbloquear emblemas"

        return True, "Todas as condições foram atendidas"

    def desbloquear_emblemas(self, aluno):
        emblemas_desbloqueados = []
        emblemas = Emblema.objects.filter(status='nao_desbloqueado')

        for emblema in emblemas:
            condicoes_atendidas, mensagem = self.verificar_condicoes_para_emblema(aluno)
            if condicoes_atendidas:
                emblema.aluno = aluno
                emblema.status = 'desbloqueado'  # Atualizar o status para 'desbloqueado'
                emblema.save()
                emblemas_desbloqueados.append(emblema.id)

        return emblemas_desbloqueados