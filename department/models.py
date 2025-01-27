from django.db import models
from django.utils import timezone

class Department(models.Model):
    # Define the fields based on the provided JSON data
    
    deptid = models.AutoField(primary_key=True, unique=True)
    dept_name = models.CharField(max_length=100, unique=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)

  

    def __str__(self):
        return str(self.deptid)
