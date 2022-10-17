from email.headerregistry import Address
from django.db import models

# Create your models here.
class Employee(models.Model):
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    name = models.CharField(max_length=100, null=False, blank=False)
    email=models.CharField(max_length=100, null=True, blank=True)
    phone=models.CharField(max_length=100, null=True, blank=True)
    addr=models.CharField(max_length=100, null=True, blank=True)
    details=models.TextField(null=True,blank=True)
    progress=models.CharField(max_length=200, null=True,blank=True)
    task=models.CharField(max_length=200, null=True,blank=True)
    tempc=models.CharField(max_length=100, null=True,blank=True)
    tempp=models.CharField(max_length=200, null=True,blank=True)
    tempt=models.CharField(max_length=200, null=True,blank=True)
    completed=models.CharField(max_length=100, null=True,blank=True)


    def __str__(self):
        return self.name
class Job(models.Model):
    class Meta:
        verbose_name ='Job'
        verbose_name_plural = "Jobs"
    sdate=models.CharField(max_length=50,null=True,blank=True)
    day=models.CharField(max_length=50, null=True,blank=False)
    fdate=models.CharField(max_length=50,null=True,blank=True)
    jobname=models.CharField(max_length=200, null=True,blank=True)
    task=models.CharField(max_length=200, null=True,blank=True)
    ref=models.CharField(max_length=200, null=True,blank=True)
    status=models.CharField(max_length=200, null=True,blank=True)
    remark=models.CharField(max_length=200, null=True,blank=True)
    user=models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.jobname