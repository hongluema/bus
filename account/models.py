from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField("出生日期",blank=True, null=True)
    photo = models.ImageField('头像路径',upload_to='users/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name_plural = "用户简介"

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)