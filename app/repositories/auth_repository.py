from passlib.hash import bcrypt

class AuthRepository():
    def __init__(self):
        self.users = {
            'user1': {'password': 'hashed_password1'},
            'user2': {'password': 'hashed_password2'}
        }

    def user_exists(self, username):
        return username in self.users

    def get_user_password(self, username):
        if self.user_exists(username):
            return self.users[username]['password']
        return None
    
    def get_user_by_email(self, email):
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None

    def create_user(self, name, email, password, matricula, tipo_permissao):
        hashed_password = bcrypt.hash(password)

        # Consulta SQL para inserir um novo usuário
        sql = """
            INSERT INTO USUARIO (nome, email, senha, matricula, tipo_permissao)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """
        
        cursor = self.conn.cursor()
        cursor.execute(sql, (name, email, hashed_password, matricula, tipo_permissao))
        self.conn.commit()
        user = cursor.fetchone()
        cursor.close()
        return user
    

