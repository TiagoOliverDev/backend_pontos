import unittest
import sys
import logging
sys.path.append('..')  # Adiciona o diretório pai ao sys.path

from server import create_app
from flask import json
from unittest.mock import patch, MagicMock

logging.basicConfig(level=logging.INFO)

class AuthBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        # Cria uma instância do app para testes
        self.app = create_app().test_client()
        self.app.testing = True

    @patch('app.routes.auth.auth_service')
    @patch('app.routes.auth.auth_repository')
    def test_login_successful(self, mock_auth_repository, mock_auth_service):
        # Configurando o comportamento do mock para o auth_repository
        mock_auth_repository.get_id_user.return_value = 1
        mock_auth_repository.get_type_permission_user.return_value = 'admin'
        mock_auth_repository.email_user_exists.return_value = True
        mock_auth_repository.get_user_password.return_value = 'hashed_password'
        
        # Configurando o comportamento do mock para o auth_service
        mock_auth_service.verify_password.return_value = True
        mock_auth_service.generate_token.return_value = 'token'

        # Executando o teste
        response = self.app.post('/auth/login', data=json.dumps({
            'email': 'user_teste2024@gmail.com',
            'password': 'teste123'
        }), content_type='application/json')

        if response.status_code == 404:
            logging.info(f"Rota não encontrada. Verifique a configuração das rotas. STATUS CODE: {response.status_code}")

        self.assertEqual(response.status_code, 200, "O status code deveria ser 200")
        if response.status_code == 200:
            logging.info(f'Teste da rota /auth/login foi realizado com sucesso! STATUS CODE: {response.status_code}')

        if response.data:
            data = json.loads(response.data.decode())
            self.assertIn('BearerToken', data, "A resposta deveria conter um 'BearerToken'")
        else:
            self.fail("A resposta não contém dados.")


    @patch('app.routes.auth.auth_service')  
    def test_register_successful(self, mock_auth_service):
        # Configuração do mock para registro
        mock_auth_service.register_user.return_value = ('user', None)

        # Teste de registro
        response = self.app.post('/auth/register', data=json.dumps({
            'name': 'John Doe',
            'email': 'john@example.com',
            'senha': 'password',
            'matricula': '123456',
            'tipo_permissao': 2
        }), content_type='application/json')

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', data['message'])


    # @patch('app.routes.auth.auth_service')
    # def test_register_successful(self, mock_auth_service):
    #     # Configuração do mock para simular um registro bem-sucedido
    #     mock_auth_service.register_user.return_value = ('user', None)

    #     # Executa o teste de registro
    #     response = self.app.post('/auth/register', data=json.dumps({
    #         'name': 'John Doe',
    #         'email': 'john@example.com',
    #         'senha': 'password',
    #         'matricula': '123456',
    #         'tipo_permissao': 2
    #     }), content_type='application/json')

    #     # Verificação para status code 404 (rota não encontrada)
    #     if response.status_code == 404:
    #         logging.info(f"Rota /auth/register não encontrada. Verifique a configuração das rotas. STATUS CODE: {response.status_code}")

    #     # Verificação para status code 201 (criado)
    #     self.assertEqual(response.status_code, 201, "O status code deveria ser 201")

    #     # Decodificação condicional do JSON e verificação de mensagem de sucesso
    #     if response.data:
    #         data = json.loads(response.data.decode())
    #         self.assertIn('User created successfully', data['message'], "A mensagem de sucesso deveria estar presente na resposta")
    #     else:
    #         self.fail("A resposta não contém dados.")

if __name__ == '__main__':
    unittest.main()
