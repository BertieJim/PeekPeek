from django.db import models

# Create your models here.

from django.db import models


class Person(models.Model):

    name = models.CharField(max_length=30)

    age = models.IntegerField()

    # birthday=models.DateField()

    def __unicode__(self):
        return 'name:' + self.name + ';age:' + str(self.age)