from .models import Incident
from rest_framework import serializers


class IncidentSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    severity_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    def get_address(self, obj):
        return obj.get_address_google()        


    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_severity_display(self, obj):
        return obj.get_severity_display()

    def get_status_display(self, obj):
        return obj.get_status_display()
    
    
    class Meta:
        model = Incident
        fields = '__all__'