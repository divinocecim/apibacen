from uuid import uuid4, uuid1

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api_rest.models import *
from .serializers import *

import json

#        print(f'Favorecido: {favorecido}')
#Favorecido:
#  {
#   'co_chave_pix': '34768416187',
#   'co_nome_titular': 'Divino Cecim da Silva',
#   'co_numero_conta': '48670162',
#   'co_cod_banco': '0260',
#   'de_nome_banco': 'NuBank'
#  }
# Gerar o EndToEndId e efetuar o PIX
#Request:
#  {
#    'valor': '12.34',
#    'pagador':
#       {
#           'banco': '0001',
#           'conta': '551055',
#           'infoPagador': 'Segue o pagamento da conta'
#       },
#   'favorecido':
#       {
#           'chavepix': '34768416187',
#           'contaBanco':
#               {
#                   'nome': 'Nome Favorecido',
#                   'cpf': '00000000000',
#                   'codigoBanco': '09089356',
#                   'agencia': '1',
#                   'conta': '123453',
#                   'tipoConta': 'cacc'
#               }
#       }
#   }

global statusf

# Monta retorno definitivo da chamada Send PIX
def bcb_monta_retorno_final(data):
#    print(data["bc_endtoendid"])

    bcbresponse = {"header": {"bc_endtoendid":"","bc_ts_request": ""},
                   "pagador": {'bc_banco_pagador': '','bc_conta_pagador':  '', 'bc_info_pagador': ''},
                   "favorecido": {'bc_chave_pix': '', 'bc_nome_titular': '', 'bc_numero_conta': '',
                                  'bc_cod_banco': '', 'bc_valor': '', 'bc_status_request':''
                                  }
                   }

    bcbresponse["header"]["bc_endtoendid"] = data["bc_endtoendid"]
    bcbresponse['header']["bc_ts_request"] = data['bc_ts_request']
    bcbresponse['pagador']['bc_banco_pagador'] = data['bc_banco_pagador']
    bcbresponse['pagador']['bc_conta_pagador'] = data['bc_conta_pagador']
    bcbresponse['pagador']['bc_info_pagador'] = data['bc_info_pagador']
    bcbresponse['favorecido']['bc_chave_pix'] = data['bc_chave_pix']
    bcbresponse['favorecido']['bc_nome_titular'] = data['bc_nome_titular']
    bcbresponse['favorecido']['bc_numero_conta'] = data['bc_numero_conta']
    bcbresponse['favorecido']['bc_cod_banco'] = data['bc_cod_banco']
    bcbresponse['favorecido']['bc_valor'] = data['bc_valor']
    bcbresponse['favorecido']['bc_status_request'] = data['bc_status_request']

    print('Montando retorno Final')
#    print(f'Status: {statusf}')
    return bcbresponse

def bcb_monta_retorno(data):
    try:
    # Verificar se a chave pix é valida e, se for, trazer dados do favorecido.
        favorecido = get_favorecido(data['favorecido']['chavepix'])
        statusf = status.HTTP_200_OK
        print(f'Status após ler favorecido: {statusf}')
    except:
        statusf = 'Erro ao consultar dados do favorecido'
        return statusf

# Monta Json de retorno
    bcbjsontrans = {}
    bcbjsontrans['bc_endtoendid'] = ""
    bcbjsontrans['bc_ts_request'] = ""
    bcbjsontrans['bc_banco_pagador'] = data['pagador']['banco']
    bcbjsontrans['bc_conta_pagador'] = data['pagador']['conta']
    bcbjsontrans['bc_info_pagador'] = data['pagador']['infoPagador']
    bcbjsontrans['bc_chave_pix'] = favorecido['co_chave_pix']
    bcbjsontrans['bc_nome_titular'] = favorecido['co_nome_titular']
    bcbjsontrans['bc_numero_conta'] = favorecido['co_numero_conta']
    bcbjsontrans['bc_cod_banco'] = favorecido['co_cod_banco'] 
    bcbjsontrans['bc_valor'] = data['valor']
    bcbjsontrans['bc_status_request'] = "EM_PROCESSAMENTO"
    print(type(bcbjsontrans))

    serializer = BcbResponseSerializer(data=bcbjsontrans)
#    print(f'serializer: {serializer}')
# Grava transação PIX
    if serializer.is_valid():
        print('Registro valido!!!!')
        serializer.save()
        statusf = status.HTTP_201_CREATED
        print(f'Status após gravar retorno: {statusf}')
    else:
        statusf = status.HTTP_400_BAD_REQUEST

    retorno = bcb_monta_retorno_final(serializer.data)
    return retorno, statusf

def get_favorecido(chavepix):
    try:
#        print(f'Favorecido: {chavepix}')
#          
        jcliente = ChavepixSerializer(TblChavePix.objects.get(pk=chavepix))
#            print('Leu cliente')
#            print(jcliente.data['co_cod_banco'])
        try:
    #        print(f'Codigo do Banco: {jcliente.co_cod_banco}')
            nome_banco = TblBanco.objects.get(pk=jcliente.data['co_cod_banco'])
#            print(nome_banco)
        except:
            print('Consulta com erro')
            statusf = status.HTTP_406_NOT_ACCEPTABLE
            return 'Consulta Banco com erro'
    except:
        statusf = status.HTTP_404_NOT_FOUND
        return 'Chave Pix não encontrada...'

    resposta = jcliente.data
#
    resposta['de_nome_banco'] = nome_banco.de_nome_banco   
#  
    return resposta

# Atualiza WebHook   
def atualiza_webhook():
    i = 0
    registro = TblResponse.objects.exclude(bc_status_request='REALIZADO')
    if registro.count() == 0:
        return None

    queryset1 = BcbResponseSerializer(registro, many=True)

    for r in queryset1.data:
        try:
           response_updated = TblResponse.objects.get(pk=r["bc_endtoendid"])
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

        r["bc_status_request"] = 'REALIZADO'
        print(type(r))

        queryset2 = BcbResponseSerializer(response_updated, data=r)
        if queryset2.is_valid():
            queryset2.save()
    return None

@api_view(['GET'])
def get_chave_pix(request,chavepix):
    statusf = status.HTTP_100_CONTINUE
    if request.method == 'GET':
#        print(f"Chave pix: {chavepix}")
        resposta = get_favorecido(chavepix)
#        print(f"Resposta da Consulta: {resposta}")
        return Response(resposta)

@api_view(['GET'])
def get_lan_pix(request,endtoend):
#    print(f"EndToEnd: {endtoend}")
    try:
#        print('farei busca')
        registros = TblResponse.objects.filter(bc_endtoendid=endtoend)
        resposta =  BcbResponseSerializer(registros, many=True)
        statusf = status.HTTP_200_OK
    except:
        statusf = status.HTTP_400_BAD_REQUEST
#    print(f'BcbResponse: {resposta.data} Status: {statusf}')
    nadaver = resposta.data
    nda = atualiza_webhook()
    return Response(nadaver)
#    return Response(statusf)

@api_view(['POST','PUT'])
def send_pix(request):
    nda = atualiza_webhook()
#    statusf = status.HTTP_100_CONTINUE
    bcbresponse, statusf = bcb_monta_retorno(request.data)
#    print(statusf)
    if statusf == 200:
        return Response(bcbresponse, status=status.HTTP_200_OK)
    elif statusf == 201:
        return Response(bcbresponse,status=status.HTTP_201_CREATED)
    elif statusf == 400:
        return Response(bcbresponse,status=status.HTTP_400_BAD_REQUEST)
    elif statusf == 404:
        return Response(bcbresponse,status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(bcbresponse,status=status.HTTP_417_EXPECTATION_FAILED)