from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Sin, Radians
from .models import Incident
from .serializers import IncidentSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

# Create your views here.
class IncidentViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            return Incident.objects.all()

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
        max_km = float(max_km) if max_km else 10


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
    
    def _format_choices(self, choices):
        return [{"value": v, "label": l} for v, l in choices]
    
    @action(detail=False, methods=["get"], url_path="choices")
    def choices(self, request):
        """
        Endpoint: /incident/choices/
        Devuelve los choices de category, severity y status
        """
        return Response({
            "category": self._format_choices(Incident.CATEGORY_CHOICES),
            "severity": self._format_choices(Incident.SEVERITY_CHOICES),
            "status": self._format_choices(Incident.STATUS_CHOICES),
        })