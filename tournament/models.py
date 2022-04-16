from email.policy import default
from tabnanny import verbose
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator, validate_image_file_extension
from .validators import *
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Tank(models.Model):
    class TankLevelChoice(models.TextChoices):
        TT = 'ТТ'
        ST = 'СТ'
        PT = 'ПТ'
        LT = 'ЛТ'
        CAU = 'САУ'
        
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='название',
    )
    
    level = models.IntegerField(
        validators=[tank_level_validators],
        verbose_name='уровен',
    )
    
    tank_type = models.CharField(
        verbose_name='тип',
        choices=TankLevelChoice.choices,
        max_length=5
    )
    
    is_premium = models.BooleanField(
        verbose_name='премиумный',
        default=False,
    )
    
    image = models.ImageField(
        verbose_name='фото',
        upload_to='tanks/',
        default='tanks/default_tank_icon.png',
        help_text = 'размер фотографии должен быть 1x1\n в формате png',
        validators = [
            FileExtensionValidator(allowed_extensions=['png']),
            # ImageSizeValidator(),
        ],
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['level', 'tank_type', 'name']
        verbose_name = 'Танк'
        verbose_name_plural = 'Танки'
        
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

     

class Tournament(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='название',
    )
    
    rules = models.TextField(
        verbose_name='правила',
    )
    
    goal = models.TextField(
        verbose_name='задача'
    )
    
    required_battles_count = models.PositiveIntegerField(
        verbose_name='необходимое количество боёв',
        help_text='сколько боёв необходимо сыграть чтобы результат был защитан',
        default=100,
    )
    
    tanks = models.ManyToManyField(
        'Tank',
        verbose_name='Танки',
    )
    
    total_prize = models.PositiveIntegerField(
        verbose_name='призовой фонд',
        default=0,
    )
    
    prize_first_place = models.PositiveIntegerField(
        verbose_name='приз за первое место',
    )
    
    prize_second_place = models.PositiveIntegerField(
        verbose_name='приз за второе место',
    )
    
    prize_third_place = models.PositiveIntegerField(
        verbose_name='приз за третье место',
    )
    
    start_time = models.DateTimeField(
        verbose_name='время начала'
    )
    
    end_time = models.DateTimeField(
        verbose_name='время окончания'
    )
    
    is_active = models.BooleanField(
        default=False,
        verbose_name='активен',
        # editable=False,
    )
    
    is_over = models.BooleanField(
        default=False,
        verbose_name='закончился',
        # editable=False,
    )
    
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания',
        editable=False,
    )
    
    players = models.ManyToManyField(
        User,
        through='TournamentRecord',
    )
    
    preview = models.ImageField(
        verbose_name='превью',
        upload_to='tournaments/',
        default='tournaments/default_tournament_preview.png',
        help_text = 'размер фотографии должен быть 10x2\n в формате png',
        validators = [
            validate_image_file_extension,
            # ImageSizeValidator(10, 2),
        ],
    )
    
    class Meta:
        ordering = ['start_time']
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        default_related_name='tournaments'
        
        permissions = (
            ('can_enter', 'может учавствовать в турнирах'),
        )
        
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("tournament:tournament_detail", kwargs={"pk": self.pk})
    
        

class TournamentRecord(models.Model):
    tournament = models.ForeignKey(
        'Tournament',
        on_delete=models.CASCADE,
        verbose_name='турнир',
        related_name='tournament_records'
    )
    
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='игрок',
    )
    
    battle_count = models.PositiveIntegerField(
        verbose_name='количество боёв в турнире',
        default=0,
    )
    
    win_rate = models.FloatField(
        verbose_name='процент побед в турнире',
        default=0,
    )
    
    average_damage = models.FloatField(
        verbose_name='средний дамаг в турнире',
        default=0,
    )
    
    is_tracked = models.BooleanField(
        verbose_name='отслеживать прогресс',
        default=False,
    )
    
    account_battle_count = models.PositiveIntegerField(
        verbose_name='количество боёв на аккаунте',
        null=True,
        blank=True,
    )
    
    account_win_rate = models.FloatField(
        verbose_name='процент побед на аккаунте',
        null=True,
        blank=True,
    )
    
    account_average_damage = models.FloatField(
        verbose_name='средний дамаг на аккаунте',
        null=True,
        blank=True,
    )
    
    class Meta:
        verbose_name = 'Запись в турнирной таблице'
        verbose_name_plural = 'Записи в турнирной таблице'
        default_related_name = 'tournament_records'
        unique_together = ('tournament', 'player')
        
    def __str__(self):
        return f'{self.tournament} - {self.player} - {self.battle_count}'