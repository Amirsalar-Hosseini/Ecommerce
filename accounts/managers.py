from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password=None):
        if not phone_number:
            raise ValueError('phone number must be set')

        if not email:
            raise ValueError('email must be set')

        if not full_name:
            raise ValueError('full name must be set')

        user = self.model(phne_number=phone_number, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user