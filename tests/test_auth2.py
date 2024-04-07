import unittest
# import sys
# sys.path.append('..')  # Adiciona o diretório pai ao sys.path

from server import create_app
from flask import json
from unittest.mock import patch, MagicMock


class AuthBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.app = create_app().test_client()
        self.app.testing = True
        # Definindo variáveis para evitar valores hardcoded
        self.test_user_email = 'user_teste2024@gmail.com'
        self.test_user_password = 'teste123'
        self.test_user_name = 'John Doe'
        self.test_user_new_email = 'john@example.com'
        self.test_user_senha = 'password'
        self.test_user_matricula = '123456'
        self.test_user_tipo_permissao = 2

    @patch('app.routes.auth.auth_service')
    @patch('app.routes.auth.auth_repository')
    def test_login_successful(self, mock_auth_repository, mock_auth_service):
        """Testa o login bem-sucedido de um usuário."""
        # Configuração dos mocks
        mock_auth_repository.get_id_user.return_value = 1
        mock_auth_repository.get_type_permission_user.return_value = 'admin'
        mock_auth_repository.email_user_exists.return_value = True
        mock_auth_repository.get_user_password.return_value = 'hashed_password'
        
        mock_auth_service.verify_password.return_value = True
        mock_auth_service.generate_token.return_value = 'token'

        # Teste de login
        response = self.app.post('/auth/login', data=json.dumps({
            'email': self.test_user_email,
            'password': self.test_user_password
        }), content_type='application/json')

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('BearerToken', data)
        mock_auth_service.verify_password.assert_called_once()

    @patch('app.routes.auth.auth_service')  
    def test_registration_successful(self, mock_auth_service):
        """Testa o registro bem-sucedido de um usuário."""
        mock_auth_service.register_user.return_value = ('user', None)

        response = self.app.post('/auth/register', data=json.dumps({
            'name': self.test_user_name,
            'email': self.test_user_new_email,
            'senha': self.test_user_senha,
            'matricula': self.test_user_matricula,
            'tipo_permissao': self.test_user_tipo_permissao
        }), content_type='application/json')

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', data['message'])
        mock_auth_service.register_user.assert_called_once()

    @patch('app.routes.auth.auth_service')
    @patch('app.routes.auth.auth_repository')
    def test_login_failed_wrong_password(self, mock_auth_repository, mock_auth_service):
        """Testa o login com senha incorreta."""
        # Configuração dos mocks
        # O usuário existe, mas a senha está incorreta
        mock_auth_repository.get_id_user.return_value = 1
        mock_auth_repository.get_type_permission_user.return_value = 'admin'
        mock_auth_repository.email_user_exists.return_value = True
        mock_auth_repository.get_user_password.return_value = 'hashed_password'
        
        # A verificação da senha deve falhar
        mock_auth_service.verify_password.return_value = False

        # Teste de login com senha incorreta
        response = self.app.post('/auth/login', data=json.dumps({
            'email': self.test_user_email,
            'password': 'wrong_password'
        }), content_type='application/json')

        # Verifique se o código de status indica falha (por exemplo, 401 Não Autorizado)
        self.assertNotEqual(response.status_code, 200)
        
        # Verifique se a mensagem esperada de erro está na resposta (ajuste conforme sua aplicação)
        data = json.loads(response.data.decode())
        self.assertIn('Invalid password', data['message'])

        # Verifique se verify_password foi chamado uma vez
        mock_auth_service.verify_password.assert_called_once()
    
    @patch('app.routes.auth.auth_service')
    @patch('app.routes.auth.auth_repository')
    def test_login_failed_wrong_email(self, mock_auth_repository, mock_auth_service):
        """Testa o login com e-mail incorreto."""
        mock_auth_repository.email_user_exists.return_value = False

        response = self.app.post('/auth/login', data=json.dumps({
            'email': 'nonexistentemail@example.com',
            'password': self.test_user_password
        }), content_type='application/json')

        self.assertNotEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('User does not exist', data['message'])
        mock_auth_service.verify_password.assert_not_called()


if __name__ == '__main__':
    unittest.main()
