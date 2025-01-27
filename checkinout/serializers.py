from rest_framework import serializers
from .models import CheckinOut

class CheckinOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckinOut
        fields = '__all__'