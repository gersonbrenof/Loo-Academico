from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from emblemas.models import Emblema
from emblemas.api.serializers import EmblemaSerializer, EmblemaListaTudoSerializer, EmblemaAlunoSerializer, EmblemaAluno
from exercicio.models import ResponderExercicio
from contas.models import Aluno
from duvidas.models import Duvidas
from desempenho.models import Desempenho
from materialApoio.models import MaterialApoio
from emblemas.models import EmblemaAluno
from django.db import models

#Lsita os embelma do aluno

class ListaEmblemaALunoView(generics.ListAPIView):
    serializer_class = EmblemaAlunoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        aluno = self.request.user.aluno
        
        if aluno is None:
            return Emblema.objects.none()
        
        # Desbloquear emblemas automaticamente para o aluno atual
        self.desbloquear_emblemas(aluno)
        
        # Retornar os emblemas desbloqueados associados ao aluno
        return EmblemaAluno.objects.filter(aluno=aluno, status='desbloqueado')

    
    def verificar_condicoes_para_emblema(self, aluno, emblema):
        mensagens_erro = []

        # Condição para o emblema "#0010" - "Novo Usuário"
        if emblema.codigoEmblema == "#0010":
            if not ResponderExercicio.objects.filter(aluno=aluno).exists():
                mensagens_erro.append("Resolva pelo menos um exercício para desbloquear o emblema 'Novo Usuário'.")

        # Condição para o emblema "#0101" - "Eu Questiono"
        elif emblema.codigoEmblema == "#0101":
            if not Duvidas.objects.filter(aluno=aluno).exists():
                mensagens_erro.append("Envie pelo menos uma dúvida para desbloquear o emblema 'Eu Questiono'.")

        # Condição para o emblema "#0110" - "Eu Estudo"
        elif emblema.codigoEmblema == "#0110":
            if not MaterialApoio.objects.filter(visualizacoes__gte=1).exists():
                mensagens_erro.append("Consulte pelo menos um material de apoio para desbloquear o emblema 'Eu Estudo'.")

        # Condição para o emblema "#1000" - "Que Desempenho!"
        elif emblema.codigoEmblema == "#1000":
            # Busca os desempenhos do aluno
            desempenho = Desempenho.objects.filter(aluno=aluno)

            if desempenho.exists():
                desempenho_total = desempenho.aggregate(
                    total_respostas=models.Sum('total_respostas'),
                    respostas_corretas=models.Sum('respostas_corretas')
                )

                total_respostas = desempenho_total['total_respostas'] or 0
                respostas_corretas = desempenho_total['respostas_corretas'] or 0

                # Verifica se o aluno resolveu pelo menos 3 exercícios
                if total_respostas >= 3:
                    # Calcula a porcentagem de acertos
                    porcentagem_acertos = (respostas_corretas / total_respostas) * 100 if total_respostas > 0 else 0

                    # Verifica se a porcentagem de acertos é igual ou maior que 80%
                    if porcentagem_acertos < 50:
                        mensagens_erro.append("Obtenha pelo menos 50% de acertos em 3 ou mais exercícios para desbloquear o emblema 'Que Desempenho!'.")
                else:
                    mensagens_erro.append("Resolva pelo menos 3 exercícios para desbloquear o emblema 'Que Desempenho!'.")
            else:
                mensagens_erro.append("Você ainda não tem desempenho registrado para desbloquear o emblema 'Que Desempenho!'.")

        # Verifica se há erros nas condições para desbloquear o emblema
        if mensagens_erro:
            return False, mensagens_erro

        return True, "Todas as condições foram atendidas"

    def desbloquear_emblemas(self, aluno):
        # Lista de emblemas globais que podem ser desbloqueados (não associados a alunos)
        emblemas_nao_desbloqueados = Emblema.objects.all()

        mensagens_erro = []
        
        # Verificar se o aluno já tem o emblema desbloqueado ou não
        for emblema in emblemas_nao_desbloqueados:
            emblema_aluno, criado = EmblemaAluno.objects.get_or_create(aluno=aluno, emblema=emblema)

            if emblema_aluno.status == 'desbloqueado':
                continue  # Se já estiver desbloqueado, pula para o próximo emblema

            # Verificar se o aluno atende às condições para desbloquear o emblema
            condicoes_atendidas, mensagem = self.verificar_condicoes_para_emblema(aluno, emblema)
            if condicoes_atendidas:
                emblema_aluno.status = 'desbloqueado'
                emblema_aluno.save()  # Salva o emblema como desbloqueado para esse aluno
            else:
                mensagens_erro.extend(mensagem)
        
        # Se houver mensagens de erro, retorná-las
        if mensagens_erro:
            return Response({"errors": mensagens_erro}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Emblemas atualizados com sucesso."}, status=status.HTTP_200_OK)

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
            # Inicializa o status como 'nao_desbloqueado'
            emblema.status = 'nao_desbloqueado'
            emblema_aluno, _ = EmblemaAluno.objects.get_or_create(aluno=aluno, emblema=emblema)

            if emblema_aluno.status == 'desbloqueado':
                emblema.status = 'desbloqueado'
            else:
                # Verifica se o aluno ainda atende às condições para manter o emblema desbloqueado
                condicoes_atendidas, _ = self.verificar_condicoes_para_emblema(aluno, emblema)
                if condicoes_atendidas:
                    emblema.status = 'desbloqueado'

            # Adiciona o emblema à lista de emblemas atualizados
            emblemas_atualizados.append(emblema)

        return emblemas_atualizados

    def verificar_condicoes_para_emblema(self, aluno, emblema):
        mensagens_erro = []

        # Condição para o emblema "#0010" - "Novo Usuário"
        if emblema.codigoEmblema == "#0010":
            if not ResponderExercicio.objects.filter(aluno=aluno).exists():
                mensagens_erro.append("Resolva pelo menos um exercício para desbloquear o emblema 'Novo Usuário'.")

        # Condição para o emblema "#0101" - "Eu Questiono"
        elif emblema.codigoEmblema == "#0101":
            if not Duvidas.objects.filter(aluno=aluno).exists():
                mensagens_erro.append("Envie pelo menos uma dúvida para desbloquear o emblema 'Eu Questiono'.")

        # Condição para o emblema "#0110" - "Eu Estudo"
        elif emblema.codigoEmblema == "#0110":
            if not MaterialApoio.objects.filter(visualizacoes__gte=1).exists():
                mensagens_erro.append("Consulte pelo menos um material de apoio para desbloquear o emblema 'Eu Estudo'.")

        # Condição para o emblema "#1000" - "Que Desempenho!"
        elif emblema.codigoEmblema == "#1000":
            desempenho = Desempenho.objects.filter(aluno=aluno)

            if desempenho.exists():
                desempenho_total = desempenho.aggregate(
                    total_respostas=models.Sum('total_respostas'),
                    respostas_corretas=models.Sum('respostas_corretas')
                )

                total_respostas = desempenho_total['total_respostas'] or 0
                respostas_corretas = desempenho_total['respostas_corretas'] or 0

                if total_respostas >= 3:
                    porcentagem_acertos = (respostas_corretas / total_respostas) * 100 if total_respostas > 0 else 0
                    if porcentagem_acertos < 80:
                        mensagens_erro.append("Obtenha pelo menos 80% de acertos em 3 ou mais exercícios para desbloquear o emblema 'Que Desempenho!'.")
                else:
                    mensagens_erro.append("Resolva pelo menos 3 exercícios para desbloquear o emblema 'Que Desempenho!'.")
            else:
                mensagens_erro.append("Você ainda não tem desempenho registrado para desbloquear o emblema 'Que Desempenho!'.")
        
        # Verifica se há erros nas condições para desbloquear o emblema
        if mensagens_erro:
            return False, mensagens_erro

        return True, "Todas as condições foram atendidas"