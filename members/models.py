from django.db import models
from django.contrib.auth.models import User
class Member(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    full_name=models.CharField(max_length=100)
    member_no=models.CharField(max_length=20,unique=True)
    phone=models.CharField(max_length=15,unique=True)
    status=models.CharField(max_length=10,choices=[('active','active'),('inactive','inactive')],default='active')
    is_admin=models.BooleanField(default=False)
    joined_date=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.member_no