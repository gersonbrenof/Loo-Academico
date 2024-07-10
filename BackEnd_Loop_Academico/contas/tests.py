# contas/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from contas.models import Aluno
class AlunoAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/Api/Cadastrar/'
        self.login_url = '/Api/login/'
        self.aluno_data = {
            'nomeAluno': 'John Doe',
            'institucao': 'Universidade ABC',
            'matricula': '123456',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        }

    def test_registro_aluno(self):
        response = self.client.post(self.register_url, self.aluno_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['nomeAluno'], self.aluno_data['nomeAluno'])
    # def test_login_aluno(self):
    #     data = {
    #         'email': self.aluno_data['email'],
    #         'password': self.aluno_data['password']
    #     }
    #     response = self.client.post(self.login_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('tokens', response.data)
