from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Car(models.Model):
    model = models.TextField(blank=False, null=False)
    make = models.TextField(blank=False, null=False)
    brand = models.TextField(blank=False, null=False)
    year = models.IntegerField(default=2000, null=False)
    owner_id = models.ForeignKey(User, blank=True, null=True, related_name='user', related_query_name='user',
                                 on_delete=models.CASCADE)
    capacity = models.IntegerField(null=False, blank=False)
    condition = models.IntegerField(blank=False, null=False)
    approved = models.BooleanField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'cars'

    def __str__(self):
        strtemplate = "{} - {} - {}"
        stringified = strtemplate.format(self.owner_id, self.model, self.make)
        return stringified
