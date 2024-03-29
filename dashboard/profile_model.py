from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True, null=True)
    dark_mode =  models.BooleanField(default=False)
    use_biometrics = models.BooleanField(default=False)

    # profile_pix = models.ImageField()
    # other profile attributes

    def __str__(self):
        return f'Profile of {self.user.username}'
        