from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Property,PropertViews

class PropertySerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only = True)

    class Meta:
        model = Property
        exclude = ['updated_at','pkid','objects','published']

    def get_user(self,obj):
        return obj.user.username


class PropertyCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only = True)

    class Meta:
        model = Property
        exclude = ['updated_at','pkid']

class PropertyViewSerializer(serializers.ModelField):
    class Meta:
        model = PropertViews
        exclude = ['updated_at','pkid']