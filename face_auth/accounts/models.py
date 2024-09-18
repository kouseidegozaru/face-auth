from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('ユーザーにはメールアドレスが必要です')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True  # スタッフ権限を明示
        user.is_superuser = True  # スーパーユーザー権限を設定
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='メールアドレス', max_length=255, unique=True)
    name = models.CharField(verbose_name='名前', max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # ログイン時に使用するフィールド
    REQUIRED_FIELDS = ['name']  # ユーザー作成時に必要なフィールド

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser  # スーパーユーザー権限がある場合のみTrue

    def has_module_perms(self, app_label):
        return self.is_superuser  # スーパーユーザー権限がある場合のみTrue
