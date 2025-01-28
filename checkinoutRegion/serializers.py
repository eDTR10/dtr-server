from rest_framework import serializers
from .models import CheckinOutRegion

class CheckinOutRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckinOutRegion
        fields = '__all__'