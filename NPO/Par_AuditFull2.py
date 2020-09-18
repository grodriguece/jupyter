# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # par_aud
# . provides pdf with parame tert audit.
# . for tables LNBTS, LNCEL, WBTS y WCEL

from rfpack.par_audc import par_aud

dbfile = Path('C:/sqlite/20200522_sqlite.db')
tabfile = dbfile.parent / Path('tablasSQL.csv')
tabfileop = "audit2"
par_aud(dbfile, tabfile, tabfileop)  # audit2 column from csv table file
