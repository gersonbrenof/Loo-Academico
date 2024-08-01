from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from contas.models import Aluno
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class AlunoAPITests(APITestCase):
    def setUp(self):
        # Cria um usuário e perfil associados
        self.aluno = Aluno.objects.create(
            user=User.objects.create_user(
                username='aluno@example.com',
                email='aluno@example.com',
                password='senha123'
            ),
            nomeAluno='Aluno Teste',
            matricula='123456',
            instituicao='Instituição Teste',
            email='aluno@example.com'
        )
        self.login_url = reverse('login')  # Ajuste a URL conforme necessário
        self.protected_url = reverse('protected')  # Ajuste a URL conforme necessário

    def test_access_protected_endpoint_with_token(self):
        # Login para obter o token
        response = self.client.post(self.login_url, {'email': 'aluno@example.com', 'password': 'senha123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        access_token = response.data['access']

        # Acessar endpoint protegido com o token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'This is a protected endpoint')
