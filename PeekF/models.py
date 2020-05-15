from django.db import models

# Create your models here.

from django.db import models


class Person(models.Model):

    name = models.CharField(max_length=30)

    age = models.IntegerField()

    # birthday=models.DateField()

    def __unicode__(self):
        return 'name:' + self.name + ';age:' + str(self.age)


class Groupinfo(models.Model):
    group = models.CharField(primary_key=True, max_length=50)
    num = models.CharField(unique=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'groupinfo'

    def __unicode__(self):
        return 'name:' + self.group + ';age:' + self.num

class ClangWineFunc(models.Model):
    func_name = models.CharField(primary_key=True, max_length=100)
    dll_name = models.CharField(max_length=50)
    file_name = models.CharField(max_length=50, blank=True, null=True)
    ret_type = models.CharField(max_length=50, blank=True, null=True)
    var_type = models.CharField(max_length=2000, blank=True, null=True)
    var_name = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clang_wine_func'
        unique_together = (('func_name', 'dll_name'),)



class BigBigtext(models.Model):
    linenum =  models.IntegerField(primary_key=True)
    id = models.IntegerField()
    pid = models.IntegerField()
    childnum = models.CharField(max_length=10, blank=True, null=True)
    threadn = models.CharField(max_length=10)
    processn = models.CharField(max_length=10)
    nameshow = models.CharField(max_length=100, blank=True, null=True)
    inputval = models.CharField(max_length=2000, blank=True, null=True)
    retval = models.CharField(max_length=2000, blank=True, null=True)
    inputtype = models.CharField(max_length=2000, blank=True, null=True)
    rettype = models.CharField(max_length=2000, blank=True, null=True)
    group = models.CharField(max_length=500, blank=True, null=True)
    file = models.CharField(max_length=100, blank=True, null=True)


class originaltext(models.Model):
    linenum =  models.IntegerField(primary_key=True)
    id = models.IntegerField()
    pid = models.IntegerField()
    childnum = models.CharField(max_length=10, blank=True, null=True)
    threadn = models.CharField(max_length=10)
    processn = models.CharField(max_length=10)
    nameshow = models.CharField(max_length=100, blank=True, null=True)
    inputval = models.CharField(max_length=2000, blank=True, null=True)
    retval = models.CharField(max_length=2000, blank=True, null=True)
    inputtype = models.CharField(max_length=2000, blank=True, null=True)
    rettype = models.CharField(max_length=2000, blank=True, null=True)
    group = models.CharField(max_length=500, blank=True, null=True)
    file = models.CharField(max_length=100, blank=True, null=True)



class Funcgroup(models.Model):
    funcname = models.CharField(primary_key=True, max_length=100)
    dllname = models.CharField(max_length=50)
    group0 = models.CharField(max_length=100, blank=True, null=True)
    group1 = models.CharField(max_length=100, blank=True, null=True)
    group2 = models.CharField(max_length=100, blank=True, null=True)
    group3 = models.CharField(max_length=100, blank=True, null=True)
    group4 = models.CharField(max_length=100, blank=True, null=True)
    group5 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funcgroup'
        unique_together = (('funcname', 'dllname'),)

class KeyTrace(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    nameshow = models.CharField(max_length=100, blank=True, null=True)
    inputval = models.CharField(max_length=2000, blank=True, null=True)
    retval = models.CharField(max_length=2000, blank=True, null=True)

class PalPals(models.Model):
    index = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    palsnum = models.IntegerField()
    state = models.IntegerField()
    nameshow2 = models.CharField(max_length=100, blank=True, null=True)
    inputval2 = models.CharField(max_length=2000, blank=True, null=True)
    retval2 = models.CharField(max_length=2000, blank=True, null=True)
class PalPals2(models.Model):
    index = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    palsnum = models.IntegerField()
    state = models.IntegerField()
    nameshow2 = models.CharField(max_length=100, blank=True, null=True)
    inputval2 = models.CharField(max_length=2000, blank=True, null=True)
    retval2 = models.CharField(max_length=2000, blank=True, null=True)

class ProcessInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    app_name = models.CharField(max_length=100, blank=True, null=True)