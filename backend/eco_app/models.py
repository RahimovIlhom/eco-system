from django.contrib.auth import get_user_model
from django.db import models

employee_model = get_user_model()


WORKING_DAYS = (
    ('monday_to_friday', 'From Monday to Friday'),
    ('monday_to_saturday', 'From Monday to Saturday'),
    ('all_days', 'All days'),
)


class EcoBranch(models.Model):
    employee = models.ForeignKey(employee_model, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey('address_app.Address', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('address_app.Location', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    working_days = models.CharField(max_length=25, choices=WORKING_DAYS, default='all_days')
    information = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'eco_branches'

    def __str__(self):
        return f"{self.address} {self.working_days}"
