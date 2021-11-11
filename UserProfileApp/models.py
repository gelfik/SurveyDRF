import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.contrib.auth.models import Group


def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


class UserManager(BaseUserManager):
    def create_user(self, email, lastName, firstName, password=None):
        if email is None:
            raise TypeError('Email обязательное поле.')
        if lastName is None:
            raise TypeError('Фамилия обязательное поле.')
        if firstName is None:
            raise TypeError('Имя обязательное поле.')

        new_username = transliterate(firstName[:1] + lastName)
        user = self.model(username=new_username, email=self.normalize_email(email))
        user.firstName = firstName
        user.lastName = lastName
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, lastName, firstName, password):
        if email is None:
            raise TypeError('Email обязательное поле.')
        if lastName is None:
            raise TypeError('Фамилия обязательное поле.')
        if firstName is None:
            raise TypeError('Имя обязательное поле.')
        if password is None:
            raise TypeError('Пароль обязательное поле.')

        user = self.create_user(email, lastName, firstName, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)
    lastName = models.CharField('Фамилия', max_length=255, default=None)
    firstName = models.CharField('Имя', max_length=255, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['lastName', 'firstName', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'Users'

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        return jwt.encode({'user_data': {'id': self.pk, 'username': self.username,
                                         'created_date': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))},
                           'exp': datetime.now() + timedelta(days=60),
                           'iat': datetime.now(),
                           }, settings.SECRET_KEY, algorithm='HS256')
