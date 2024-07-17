from django.contrib.auth import get_user_model
from django.db import models


employee_model = get_user_model()


class EcoBranchEmployee(models.Model):
    tg_id = models.CharField(max_length=255, primary_key=True, unique=True)
    employee = models.OneToOneField(employee_model, on_delete=models.SET_NULL, null=True, blank=True)
    eco_branch = models.ForeignKey('eco_app.EcoBranch', on_delete=models.SET_NULL, null=True, blank=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    inn = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'eco_branch_employees'


class Participant(models.Model):
    tg_id = models.CharField(max_length=255, primary_key=True, unique=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    address = models.ForeignKey('address_app.Address', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('address_app.Location', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'participants'


class RegisteredQRCode(models.Model):
    participant = models.ForeignKey('users.Participant', on_delete=models.CASCADE)
    qrcode = models.ForeignKey('game_app.QRCode', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('address_app.Location', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.participant} {self.qrcode}"

    class Meta:
        db_table = 'registered_qrcodes'


class Winner(models.Model):
    registered_qrcode = models.ForeignKey('users.RegisteredQRCode', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registered_qrcode}"

    class Meta:
        db_table = 'winners'
