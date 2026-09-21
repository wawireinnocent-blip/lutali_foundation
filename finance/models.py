from django.db import models
from members.models import Member
class Billing(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE); billing_type=models.CharField(max_length=20); amount=models.IntegerField(); description=models.CharField(max_length=100); month=models.IntegerField(null=True,blank=True); year=models.IntegerField(null=True,blank=True); date_created=models.DateTimeField(auto_now_add=True)
class Payment(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE); mpesa_code=models.CharField(max_length=20,unique=True); amount=models.IntegerField(); status=models.CharField(max_length=10,default='pending'); date=models.DateTimeField(auto_now_add=True)
class Expense(models.Model):
    description=models.CharField(max_length=100); amount=models.IntegerField(); date=models.DateTimeField(auto_now_add=True)
class Welfare(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE,null=True); wtype=models.CharField(max_length=20); amount=models.IntegerField(); date=models.DateTimeField(auto_now_add=True)
class Meeting(models.Model):
    title=models.CharField(max_length=100); date=models.DateTimeField(auto_now_add=True)
class Attendance(models.Model):
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE); member=models.ForeignKey(Member,on_delete=models.CASCADE); present=models.BooleanField(default=False)