from rest_framework import serializers
from .models import MyTable


class BatterSerializer(serializers.Serializer):
    BATTER_ID = serializers.FloatField()
    BATTER = serializers.CharField(max_length=100)


class PitcherSerializer(serializers.Serializer):
    PITCHER_ID = serializers.FloatField()
    PITCHER = serializers.CharField(max_length=100)


class MyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTable
        fields = "__all__"
