from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Sin, Radians
from .models import Incident
from .serializers import IncidentSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


# Create your views here.
class IncidentViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        latitude = self.request.GET.get("latitude")
        longitude = self.request.GET.get("longitude")
        max_km = self.request.GET.get("max_km")

        # 🔹 Si no mandan ubicación → devolver todo
        if not latitude or not longitude:
            raise ValidationError({
                "detail": "latitude and longitude are required"
            })
        
        latitude = float(latitude)
        longitude = float(longitude)
        max_km = float(max_km) if max_km else 5


        distance_expr = ExpressionWrapper(
            6371 * ACos(
                Cos(Radians(latitude)) *
                Cos(Radians(F('latitude'))) *
                Cos(Radians(F('longitude')) - Radians(longitude)) +
                Sin(Radians(latitude)) *
                Sin(Radians(F('latitude')))
            ),
            output_field=FloatField()
        )

        queryset = Incident.objects.annotate(distance=distance_expr).filter(distance__lte=max_km)
        return queryset
    

class ChoicesView(APIView):
    def _format_choices(self, choices):
        return [
            {"value": value, "label": label}
            for value, label in choices
        ]

    def get(self, request):
        return Response({
            "category": self._format_choices(Incident.CATEGORY_CHOICES),
            "severity": self._format_choices(Incident.SEVERITY_CHOICES),
            "status": self._format_choices(Incident.STATUS_CHOICES),
        })