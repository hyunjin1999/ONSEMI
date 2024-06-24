from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

# Create your models here.

# 추상 클래스 = 틀
# 연극 역할 -> 안의 배우는 다 다름 이병헌, 손승헌
# User.save() ->db에 들어감 -> 비밀번호가 암호화가 안됨


# 그래서 아래거 사용
class UserManager(BaseUserManager):

    def create_user(self, username, phone_number, email, user_type, password=None):
        if not username:
            raise ValueError("username doesn't exist")

        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, user_type):
        if not username:
            raise ValueError("username doesn't exist")

        user = self.create_user(
            username=username, password=password, email=email, user_type=user_type
        )
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True)  # 150글자
    password = models.CharField(max_length=128)  # 128글자
    register_date = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)  # true, false (0, 1 -> int)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=50)  # FAMILY, VOLUNTEER, ADMIN

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "user_type"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser
