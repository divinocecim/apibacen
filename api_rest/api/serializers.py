from rest_framework import serializers
from api_rest.models import *

class ChavepixSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblChavePix
        fields = '__all__'

class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblBanco
        fields = 'co_nome_banco'

class BcbResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblResponse
        fields = '__all__'

       