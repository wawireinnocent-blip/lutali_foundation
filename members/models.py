from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    member_no = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, default='active', choices=[('active','active'),('inactive','inactive')])
    joined_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.member_no} {self.full_name}"

class Bill(models.Model):
    BILL_TYPES = [('Registration','Registration'),('Monthly','Monthly'),('Fine','Fine'),('Welfare-Bereavement','Welfare-Bereavement'),('Welfare-Sickness','Welfare-Sickness')]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    bill_type = models.CharField(max_length=30, choices=BILL_TYPES)
    amount = models.IntegerField()
    month = models.CharField(max_length=20, blank=True, null=True) # e.g August 2026
    year = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [] # handled in view for monthly

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=20, unique=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, default='PENDING', choices=[('PENDING','PENDING'),('VERIFIED','VERIFIED'),('DECLINED','DECLINED')])
    created_at = models.DateTimeField(auto_now_add=True)

class Meeting(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)

class Welfare(models.Model):
    welfare_type = models.CharField(max_length=20, choices=[('Bereavement','Bereavement'),('Sickness','Sickness')])
    amount_per_member = models.IntegerField()
    beneficiary = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    members_charged = models.IntegerField(default=29)

class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
