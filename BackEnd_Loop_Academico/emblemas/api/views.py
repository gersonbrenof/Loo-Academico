from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from emblemas.models import Emblema
from emblemas.api.serializers import EmblemaSerializer, EmblemaListaTudoSerializer
from exercicio.models import ResponderExercicio
from contas.models import Aluno
from duvidas.models import Duvidas
from desempenho.models import Desempenho
from materialApoio.models import MaterialApoio
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
        
        # Retornar os emblemas desbloqueados associados ao aluno
        return Emblema.objects.filter(aluno=aluno, status='desbloqueado')

    def verificar_condicoes_para_emblema(self, aluno, emblema):
        """
        Verifica se as condições necessárias para desbloquear um emblema são atendidas.
        """
        # Verifica se o cadastro do aluno está completo
        if emblema.codigoEmblema == "#0010":
            if not aluno.email or not aluno.nomeAluno or not ResponderExercicio.objects.filter(aluno=aluno).exists():
                return False, "Complete seu cadastro, configure seu ambiente e resolva um exercício para desbloquear o emblema 'Novo Usuário'"

        # Verifica se o aluno enviou uma dúvida
        if emblema.codigoEmblema == "#0101":
            if not Duvidas.objects.filter(aluno=aluno).exists():
                return False, "Envie uma dúvida para desbloquear o emblema 'Eu Questiono'"

        # Verifica se o aluno consultou um material de apoio
        if emblema.codigoEmblema == "#0110":
            if not MaterialApoio.objects.filter(aluno=aluno).exists():
                return False, "Consulte um material de apoio para desbloquear o emblema 'Eu Estudo'"

        # Verifica o desempenho do aluno nos exercícios
        if emblema.codigoEmblema == "#1000":
            if Desempenho.porcentagem_desempenho(aluno) < 50:
                return False, "Obtenha desempenho bom ou maior ao responder uma lista de exercícios para desbloquear o emblema 'Que Desempenho!'"
        
        return True, "Todas as condições foram atendidas"

    def desbloquear_emblemas(self, aluno):
        """
        Desbloqueia emblemas para o aluno se as condições forem atendidas.
        """
        # Filtrar emblemas que não estão associados a nenhum aluno e que ainda estão não desbloqueados
        emblemas = Emblema.objects.filter(aluno__isnull=True, status='nao_desbloqueado')

        for emblema in emblemas:
            condicoes_atendidas, _ = self.verificar_condicoes_para_emblema(aluno, emblema)
            if condicoes_atendidas:
                # Vincula o emblema ao aluno e atualiza o status para 'desbloqueado'
                emblema.aluno = aluno
                emblema.status = 'desbloqueado'
                emblema.save()
class ListaTodosEmblemasView(generics.ListAPIView):
    serializer_class = EmblemaListaTudoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        aluno = self.request.user.aluno

        if aluno is None:
            return Emblema.objects.none()

        # Recupera todos os emblemas
        emblemas = Emblema.objects.all()
        emblemas_atualizados = []

        for emblema in emblemas:
            if emblema.aluno == aluno:
                # Verifica se o aluno ainda atende às condições para manter o emblema desbloqueado
                condicoes_atendidas, _ = self.verificar_condicoes_para_emblema(aluno, emblema)
                if not condicoes_atendidas:
                    # Se as condições não forem mais atendidas, reverte o status para 'não desbloqueado'
                    emblema.status = 'nao_desbloqueado'
                    emblema.aluno = None
            else:
                # Emblema ainda não foi desbloqueado para o aluno
                emblema.status = 'nao_desbloqueado'

            # Adiciona o emblema à lista de emblemas atualizados
            emblemas_atualizados.append(emblema)

        return emblemas_atualizados

    def verificar_condicoes_para_emblema(self, aluno, emblema):
        # Verifica se o cadastro do aluno está completo
        if not aluno.email or not aluno.nomeAluno:
            return False, "Complete seu cadastro para desbloquear emblemas"
        
        # Verifica se o aluno concluiu pelo menos um exercício com resultado 'Correto'
        if not ResponderExercicio.objects.filter(aluno=aluno, resultado='Correto').exists():
            return False, "Resolva um exercício para desbloquear emblemas"

        # Verifica se o aluno enviou uma dúvida (para desbloquear o emblema "Eu Questiono")
        if emblema.codigoEmblema == "#0101" and not Duvidas.objects.filter(aluno=aluno).exists():
            return False, "Envie uma dúvida para desbloquear o emblema 'Eu Questiono'"
        
        # Verifica condições específicas para cada emblema, se houver
        return True, "Todas as condições foram atendidas"