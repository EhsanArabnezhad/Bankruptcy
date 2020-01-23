from __future__ import print_function

import os
from typing import Any
from datetime import datetime
from importlib import reload
import pandas as pd
from flask import Flask, request, jsonify
from json2html import json2html
from jinja2 import Environment, FileSystemLoader

import ariskanalisi as arisk
import ariskparametri

reload(ariskparametri)

app = Flask(__name__,
            instance_relative_config=True,
            static_folder='static',
            template_folder='templates')


@app.route("/hello")
def hello():
    my_output = "ARisk Engine V1.0.12"
    return my_output


@app.route("/red_flags_year", methods=['GET', 'POST'])
def red_flags_year():
    json_data = request.get_json()
    company = int(request.args['cID'])
    # output_type = int(request.args['oType'])    # 0 html, 1 JSon

    ind_familiarita = [json_data['InData']['EFQ']['input'][3],
                       json_data['InData']['EFQ']['input'][4],
                       json_data['InData']['EFQ']['input'][5],
                       json_data['InData']['EFQ']['input'][6]
                       ]

    # ti force recache of the library. To be removed when in the final version
    reload(arisk)
    reload(ariskparametri)
    os.chdir(ariskparametri.ariskBaseDir)
    all_data = arisk.read_and_transform('20190908-attive-all.xlsx', 'Risultati')
    my_company = all_data.loc[company]
    my_company_data = my_company[ariskparametri.cols]
    my_company_data = my_company_data.fillna(0)
    my_anagrafica = my_company[ariskparametri.anagrafica_cols]
    my_output = arisk.analyze_company(my_anagrafica, my_company_data, ind_familiarita)

    return my_output


@app.route("/RFRB", methods=['POST'])
def RFRB():
    if request.method == "POST":
        print("POST method")

    json_data = request.get_json(force=True)
    if request.is_json:
        print("is json")
    return json_data


@app.route("/RFRA", methods=['POST'])
def RFRA():
    json_data = request.get_json()

    reload(arisk)
    reload(ariskparametri)

    os.chdir(ariskparametri.ariskBaseDir)

    print(json_data)
    my_anagr_data = json_data['InData']['survey1']
    my_fin_data = json_data['inData']['survey2']

    ind_familiarita = [json_data['InData']['EFQ']['input'][3],
                       json_data['InData']['EFQ']['input'][4],
                       json_data['InData']['EFQ']['input'][5],
                       json_data['InData']['EFQ']['input'][6]
                       ]

    my_anagrafica = pd.DataFrame(columns=ariskparametri.anagrafica_cols)
    my_company_data = pd.DataFrame(columns=ariskparametri.cols)
    my_anagrafica = my_anagrafica.append(my_anagr_data, ignore_index=True)
    my_company_data = my_company_data.append(my_fin_data, ignore_index=True)

    my_output = arisk.analyze_company(my_anagrafica, my_company_data, ind_familiarita)

    return my_output


@app.route("/RFRAjson", methods=['POST'])
def RFRAjson():
    json_data = request.get_json()

    return json_data


@app.route("/PrintData", methods=['POST'])
def RFRC():
    json_data = request.get_json()

    ind_finanziari = json_data['InData']['AQ']['input'][2]['fixedRows']
    ind_finanziari_text = list()
    ind_finanziari_values = list()
    for idx, item in enumerate(ind_finanziari):
        ind_finanziari_text.append(ind_finanziari[idx]['title'])
        ind_finanziari_values.append(ind_finanziari[idx]['values'][0]['value'])

    return json_data


@app.route("/RFRBAI", methods=['POST'])
def RFRBAI():
    json_data = request.get_json()  # type: Any

    os.chdir(ariskparametri.ariskBaseDir)

    anagrafica_cols = [
        'ATT1',
        'ATT3',
        'ATT6',
        'EQFStart',
        'EQFEnd',
        'AQStart',
        'AQEnd'
    ]
    if not arisk.check_survey_data(json_data):
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template-report')))
        template = env.get_template('templateIncomplete.html')
        my_output = template.render(Azienda=json_data['InData']['ANA']['name'])
    else:
        my_anagr_data = [(json_data['InData']['ANA']['name'],
                          json_data['InData']['ANA']['piva'],
                          json_data['InData']['ANA']['ateco_2007_code'],
                          datetime.strptime(json_data['InData']['EFQ']['period_start'], '%Y-%m-%d %H:%M:%S').date(),
                          datetime.strptime(json_data['InData']['EFQ']['period_end'], '%Y-%m-%d %H:%M:%S').date(),
                          datetime.strptime(json_data['InData']['AQ']['period_start'], '%Y-%m-%d %H:%M:%S').date(),
                          datetime.strptime(json_data['InData']['AQ']['period_end'], '%Y-%m-%d %H:%M:%S').date(),)
                         ]

        ind_finanziari = json_data['InData']['AQ']['input'][2]['fixedRows']

        my_fin_data = [(float(ind_finanziari[8]['values'][0]['value']),
                        float(ind_finanziari[9]['values'][0]['value']),
                        float(ind_finanziari[10]['values'][0]['value']),
                        float(ind_finanziari[5]['values'][0]['value']),
                        float(ind_finanziari[11]['values'][0]['value']),
                        float(ind_finanziari[12]['values'][0]['value']),
                        float(ind_finanziari[13]['values'][0]['value']),
                        float(ind_finanziari[14]['values'][0]['value']),
                        float(ind_finanziari[15]['values'][0]['value']),
                        float(ind_finanziari[16]['values'][0]['value']),
                        float(ind_finanziari[17]['values'][0]['value']),
                        float(ind_finanziari[18]['values'][0]['value']),
                        float(ind_finanziari[19]['values'][0]['value']),
                        float(ind_finanziari[20]['values'][0]['value']),
                        float(ind_finanziari[21]['values'][0]['value']),
                        0,
                        0)
                       ]

        ind_familiarita = [json_data['InData']['EFQ']['input'][3],
                           json_data['InData']['EFQ']['input'][4],
                           json_data['InData']['EFQ']['input'][5],
                           json_data['InData']['EFQ']['input'][6]
                           ]

        my_anagrafica = pd.DataFrame.from_records(my_anagr_data, columns=anagrafica_cols)
        print(my_anagr_data)
        print(my_anagrafica)
        my_company_data = pd.DataFrame.from_records(my_fin_data, columns=ariskparametri.cols)
        my_output = arisk.analyze_company(my_anagrafica, my_company_data, ind_familiarita)

    return my_output


@app.route("/RFRCAI", methods=['POST'])
def RFRCAI():
    json_data = request.get_json()

    if json_data["oType"] == 0:
        result = json2html.convert(json=json_data)
    else:
        result = jsonify(json_data)

    return result


if __name__ == "__main__":
    # app.run(debug=True, port=5957)
    app.run(debug=True)
