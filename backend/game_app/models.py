from django.contrib.auth import get_user_model
from django.db import models

employee_model = get_user_model()

GAME_STATUS = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('deleted', 'Deleted'),
    ('canceled', 'Canceled'),
)


class Game(models.Model):
    employee = models.ForeignKey(employee_model, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=GAME_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'games'


class QRCode(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    eco_branch = models.ForeignKey('eco_app.EcoBranch', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    activity_time = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'qrcodes'
