# compilador/api/views.py
import os
import subprocess
import tempfile
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from exercicio.models import Compilador
from exercicio.api.serializers import CompiladorSerializer

class CompiladorViewSet(viewsets.ModelViewSet):
    queryset = Compilador.objects.all()
    serializer_class = CompiladorSerializer

    @action(detail=True, methods=['post'])
    def compilar_executar_c(self, request, pk=None):
        compilador = self.get_object()
        serializer = self.get_serializer(compilador)
        
        # Recebendo código C e entradas do usuário
        codigo_c = serializer.data['codigo_c']
        entradas = serializer.data['entradas']

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_c_file_path = os.path.join(temp_dir, 'temp.c')

                # Escrever o código C no arquivo temporário
                with open(temp_c_file_path, 'w') as temp_c_file:
                    temp_c_file.write(codigo_c)

                # Compilar o código C
                compile_process = subprocess.run(['gcc', temp_c_file_path, '-o', os.path.join(temp_dir, 'temp')],
                                                 capture_output=True, text=True)

                if compile_process.returncode != 0:
                    return Response({"resultado_execucao": f"Erro na compilação:\n\n{compile_process.stderr}"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Executar o programa compilado
                execute_process = subprocess.Popen([os.path.join(temp_dir, 'temp')],
                                                   stdin=subprocess.PIPE,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   text=True)

                # Passar as entradas para o programa compilado
                stdout, stderr = execute_process.communicate(input=entradas.encode())

                if execute_process.returncode != 0:
                    return Response({"resultado_execucao": f"Erro na execução:\n\n{stderr}"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Atualizar o resultado no objeto compilador
                compilador.resultado_execucao = stdout.strip()
                compilador.save()

                # Retornar resultado da execução
                return Response({"resultado_execucao": stdout.strip()}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"resultado_execucao": f"Erro ao compilar e executar o código C: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
