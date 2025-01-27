from django.db import models
from accounts.models import UserAccount  # Import the UserAccount model

class CheckinOut(models.Model):
    attendance_number = models.AutoField(primary_key=True, unique=True)
    USERID = models.ForeignKey(UserAccount, on_delete=models.CASCADE, to_field='uid')  # Foreign key to UserAccount's uid
    CHECKTIME = models.DateTimeField(null=False)
    CHECKTYPE = models.CharField(max_length=1, null=False)
    VERIFYCODE = models.IntegerField(null=False)
    SENSORID = models.IntegerField(null=False)
    Memoinfo = models.CharField(max_length=255, blank=True, null=True)
    WorkCode = models.IntegerField(blank=True, null=True)
    sn = models.CharField(max_length=50, blank=True, null=True)
    UserExtFmt = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.USERID)
