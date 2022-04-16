from email import message
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model

class Player(AbstractUser):
    like_pancackes = models.BooleanField(
        verbose_name='любишь блинчики',
        default=False,
    )
    
    def get_absolute_url(self):
        return reverse("profile")
    

class Message(models.Model):
    class TankLevelChoice(models.TextChoices):
        personal = 'p', 'личное сообщение'
        alarm = 'a', 'оповещение'
        global_m = 'g', 'для всех'
        
    text = models.TextField(
        verbose_name='текст',
        max_length=1000,
    )
    
    sender = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name='отправитель',
        related_name='sended_messages',
    )
    
    type = models.CharField(
        verbose_name='тип',
        choices=TankLevelChoice.choices,
        max_length=3,
    )
    
    time_created = models.DateTimeField(
        verbose_name='время отправки',
        auto_now_add=True,
        editable=False,
    )
    
    is_readed = models.BooleanField(
        editable=False,
        default=False,
    )
    
    dialog = models.ForeignKey(
        'Dialog',
        on_delete=models.CASCADE,
        null=True,
        editable=False,
        related_name='messages'
    )
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        
    def __str__(self):
        return getattr(self.sender, 'username', 'wot_tournament')
    
    
class Dialog(models.Model):
    users = models.ManyToManyField(
        Player,
    )