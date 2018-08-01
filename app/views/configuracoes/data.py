#!/home/alisson/www/envs/stokynovo/bin python
# -*- coding: utf-8 -*-
"""
    modulo que contem as buscas relaizadas na base de dados
    e utilizadas em configuracoes
"""
from app import db

# imports das models
from app.models.financeiro import CissFormaPagamento


def buscar_formas_pagamento():
    """
        retorna as formas de pagamento cadastradas no ciss
    """
    formas_pagamento = db.session.query(
        CissFormaPagamento
    ).order_by(
        CissFormaPagamento.descrrecebimento
    ).all()

    return formas_pagamento