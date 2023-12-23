from django.db import models
from uuid import uuid4


class TblBanco(models.Model):
    co_cod_banco = models.CharField(primary_key=True, max_length=4, null=False)
    co_ispb_banco = models.CharField(blank=True, max_length=8)
    de_nome_banco = models.CharField(blank=True, max_length=100)
 
    def __str__(self):
        return f'Numero do Banco: {self.co_cod_banco} | Banco: {self.de_nome_banco} | ISPB: {self.co_ispb_banco}'

   

class TblChavePix(models.Model):
    co_chave_pix = models.CharField(max_length=100, primary_key=True, null=False)
    co_nome_titular = models.CharField(blank=True, max_length=100)
    co_numero_conta = models.CharField(blank=True, max_length=45)
    co_cod_banco = models.CharField(blank=False, max_length=4)

    def __str__(self):
        return __name__

   

class TblResponse(models.Model):
    bc_endtoendid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    bc_ts_request = models.DateTimeField(auto_now=True)
    bc_banco_pagador = models.CharField(max_length=4, blank=False)
    bc_conta_pagador = models.CharField(max_length=45, blank=False)
    bc_info_pagador = models.CharField(max_length=255, blank=False)
    bc_chave_pix = models.CharField(max_length=100, null=False)
    bc_nome_titular = models.CharField(blank=True, max_length=100)
    bc_numero_conta = models.CharField(blank=True, max_length=45)
    bc_cod_banco = models.CharField(blank=False, max_length=4)  
    bc_valor = models.DecimalField(default=1.0, decimal_places=2, max_digits=22)
    bc_status_request = models.CharField(max_length=25, null=False)

    def __str__(self):
        return __name__