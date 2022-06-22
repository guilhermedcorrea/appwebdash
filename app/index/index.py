from flask import Blueprint, render_template,current_app, jsonify, request
import os

import pandas as pd
from ..controllers.relatorios_index_controller import (select_resumo_infos, select_marca_prazo_fabricacao
,select_groupby_saldo_produto, vendas_mes_agrupado)


from config import TEMPLATE_FOLDER


index = Blueprint("index",__name__, 
        template_folder=os.path.join(TEMPLATE_FOLDER, "resources", "templates"), 
        static_folder=os.path.join(TEMPLATE_FOLDER, "resources", "static"))
    


@index.route("/", methods=["GET","POST"])
def home():
        datas = vendas_mes_agrupado()

        group_by_infos = select_resumo_infos()
        group_by_infos = group_by_infos[['Marca','SKU','NomeEstoque']]
        group_by_infos.groupby(['Marca','SKU','NomeEstoque']).size()
        #group_by_infos = group_by_infos.groupby(['Marca','NomeEstoque']).size().reset_index(name="Frequencia")
        #print(group_by_infos)
        frequencia = group_by_infos.groupby(['NomeEstoque'])['Marca'].value_counts().rename("Frequencia").groupby(level = 0).transform(lambda x: x/float(x.sum())) * 100
        frequencia = frequencia.reset_index(name='Frequencia')
        frequencia['Frequencia'] = frequencia['Frequencia'].apply(lambda x: round(float(x),2))
        jsons = frequencia.to_dict('records')
      

        marcasinfos = select_marca_prazo_fabricacao()

        return render_template("index.html",produtos = jsons, marcas = marcasinfos,datas=datas)