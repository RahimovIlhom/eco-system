from django.contrib.auth import get_user_model
from django.db import models

employee_model = get_user_model()


class EcoBranch(models.Model):
    employee = models.ForeignKey(employee_model, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        db_table = 'eco_branches'

    def __str__(self):
        return self.name
