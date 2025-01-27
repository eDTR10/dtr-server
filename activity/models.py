from django.db import models
from accounts.models import UserAccount

class Activity(models.Model):
    # Define the fields based on the provided JSON data
    
    activity_id = models.AutoField(primary_key=True, unique=True)
    USERID = models.ForeignKey(UserAccount, on_delete=models.CASCADE, to_field='uid') 
    fromDate = models.DateField(null=False)
    toDate = models.DateField(null=False)
    status = models.IntegerField(default=1)
    period = models.IntegerField(default=1)

    description = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

  

    def __str__(self):
        return str(self.activity_id)
