# from django.contrib.auth.models import AbstractUser
# from django.db.models import CharField
# from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


# class User(AbstractUser):
#     """
#     Default custom user model for My Awesome Project.
#     If adding fields that need to be filled at user signup,
#     check forms.SignupForm and forms.SocialSignupForms accordingly.
#     """
#
#     # First and last name do not cover name patterns around the globe
#     name = CharField(_("Name of User"), blank=True, max_length=255)
#     first_name = None  # type: ignore
#     last_name = None  # type: ignore

# def get_absolute_url(self) -> str:
#     """Get URL for user's detail view.
#
#     Returns:
#         str: URL for user detail.
#
#     """
#     return reverse("users:detail", kwargs={"username": self.username})

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError(_('User should have a username'))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError(_('Password should not be None'))

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    username = models.CharField(max_length=50, unique=True, verbose_name=_('Username'), db_index=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name=_('Email'), db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=50, verbose_name=_('Full name'), null=True)
    phone = models.CharField(max_length=16, verbose_name=_('Phone Number'), null=True)
    image = models.ImageField(upload_to='accounts/', verbose_name=_('Account image'), null=True, blank=True)
    is_superuser = models.BooleanField(default=False, verbose_name=_('Super user'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff user'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active user'))
    # date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date modified'))
    # date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.full_name:
            return f'{self.full_name} ({self.username})'
        return f'{self.username}'

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
