from django.contrib.auth import get_user_model
from django.db import models


employee_model = get_user_model()

LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)


class Admin(models.Model):
    tg_id = models.CharField(max_length=255, primary_key=True, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz')

    def __str__(self):
        return self.tg_id

    class Meta:
        db_table = 'admins'


class EcoBranchEmployee(models.Model):
    tg_id = models.CharField(max_length=255, primary_key=True, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    eco_branch = models.ForeignKey('eco_app.EcoBranch', on_delete=models.SET_NULL, null=True, blank=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    inn = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'eco_branch_employees'


class Participant(models.Model):
    tg_id = models.CharField(max_length=255, primary_key=True, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    suggested = models.ForeignKey('Participant', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'participants'


class RegisteredQRCode(models.Model):
    participant = models.ForeignKey('users.Participant', on_delete=models.CASCADE)
    qrcode = models.OneToOneField('game_app.QRCode', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('address_app.Location', on_delete=models.SET_NULL, null=True, blank=True)
    winner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.participant} {self.qrcode}"

    class Meta:
        db_table = 'registered_qrcodes'


CARD_TYPES = (
    ('uzcard', 'Uzcard'),
    ('humo', 'Humo'),
)


class PlasticCard(models.Model):
    participant = models.ForeignKey('users.Participant', on_delete=models.CASCADE)
    card_type = models.CharField(max_length=15, choices=CARD_TYPES, default='uzcard')
    card_number = models.BinaryField()
    card_date = models.DateField(null=True, blank=True)
    card_cvv = models.CharField(max_length=3, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    card_image = models.ImageField(upload_to='card_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.participant} - {self.card_type}"

    class Meta:
        db_table = 'plastic_cards'
