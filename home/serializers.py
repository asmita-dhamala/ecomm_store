from .models import *
from rest_framework import serializers

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = "__all__"
