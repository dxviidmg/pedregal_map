from django.db import models
import requests
from django.conf import settings


class Incident(models.Model):
    CATEGORY_CHOICES = [
        ('A', 'Accidentes'),
        ('B', 'Basura'),
        ('U', 'Urbanidad'),
        ('V', 'Vialidad'),
    ]

    SEVERITY_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]

    STATUS_CHOICES = [
        ('A', 'Abierto'),
        ('E', 'En proceso'),
        ('C', 'Cerrado'),
    ]

    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=1, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.title
    
#    AIzaSyC3XFQeaSvg8FTnDbAmsbR5sZzSHCaQRtA
    def get_address_osm(self):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "json",
            "lat": self.latitude,
            "lon": self.longitude,
            "addressdetails": 1
        }

        headers = {
            "User-Agent": "tu_app_nombre"  # OBLIGATORIO
        }

        r = requests.get(url, params=params, headers=headers)
        data = r.json()
        print(data)

        address = data.get("address", {})

        return {
            "street": address.get("road"),
            "number": address.get("house_number"),
            "neighborhood": address.get("neighbourhood"),
            "city": address.get("city") or address.get("town"),
            "state": address.get("state"),
            "country": address.get("country"),
            "zip_code": address.get("postcode"),
            "full_address": data.get("display_name")
        }
    
    def get_address_google(self):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{self.latitude},{self.longitude}",
            "key": settings.GOOGLE_MAPS_KEY,
            "language": "es"
        }

        r = requests.get(url, params=params)
        data = r.json()
        print()

        if data["status"] != "OK":
            return None

        components = data["results"][0]["address_components"]
        formatted_address = data["results"][0]["formatted_address"]
#        print(data["results"][0])
        result = {'full_address': formatted_address}

        for c in components:
#            print(c)
            t = c["types"]
            print(t, c["long_name"])
            if "route" in t:
                result["street"] = c["long_name"]
            elif "street_number" in t:
                result["number"] = c["long_name"]
            elif "sublocality" in t:
                print(c["long_name"])
                result["neighborhood"] = c["long_name"]
            elif "locality" in t:
                result["city"] = c["long_name"]
            elif "administrative_area_level_1" in t:
                result["state"] = c["long_name"]
            elif "country" in t:
                result["country"] = c["long_name"]
            elif "postal_code" in t:
                result["zip_code"] = c["long_name"]
            
        return result
