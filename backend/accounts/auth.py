from rest_framework.exceptions import AuthenticationFalied, APIException

from django.contrib.auth.hashers import check_password, make_password

from accounts.models import User
from companies.models import Employee, Enterprise


class Authentication:
    def signin(self, email=None, password=None) -> None | None:
        exception_auth = AuthenticationFalied('Email e/ou senha incorreto(s)')

        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth
        
        return user
    
    def signup(self, name, email, password, type_account='owner', company_id=False):
        if not name or name == '':
            raise APIException('O nome não deve ser null')
        
        if not email or email == '':
            raise APIException('O email não deve ser null')
        
        if not password or password == '':
            raise APIException('O password não deve ser null')
        
        if type_account == 'employee' and not company_id:
            raise APIException('o id da empresa nao deve ser null')

        user = User
        if user.objects.filter(email=email).exists():
            raise APIException('Este email já existe na plataforma')
        
        password_hashed = make_password(password)

        created_use = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner = 0 if type_account == 'employee' else 1
        )

        if type_account == 'owner':
            create_enterprise = Enterprise.objects.create(
                name = 'Nome da empresa',
                user_id=created_use.id
            )
        
        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id or create_enterprise.id,
                user_id=created_use.id
            )

        return created_use