from django.contrib.auth.models import User as AuthUser
from django.db import models

# Create your models here.


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'roles'
        managed = True

    def __str__(self):
        return f"{self.role_id} - {self.role_name}"


class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    postal_address = models.CharField(max_length=255)
    physical_address = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return f"{self.user.id} - {self.user.username}"


class StaffRecords(models.Model):
    staff_record_id = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=255)
    experience = models.TextField()
    skill_set = models.TextField()
    grade = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_records'
        managed = True

    def __str__(self):
        return f"{self.staff_record_id} - {self.user.user.username}"
