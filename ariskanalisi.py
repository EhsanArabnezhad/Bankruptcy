"""
This module operates a number of analysis on the company data based on the information we pass to functions
"""
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import numpy as np
import pandas as pd
from importlib import reload
import pickle
from datetime import date

from treeinterpreter import treeinterpreter as ti
from jinja2 import Environment, FileSystemLoader

import ariskutil as util
import ariskparametri

reload(sys)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def read_and_transform(my_file, sheet):
    """
    : param my_file name of the excel file to open with pandas
    : param sheet name of excel file to open with pandas
    """
    data = pd.read_excel(my_file, sheet_name=sheet)
    for col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    data.loc[data['ATT10'] < 0, 'ATT10'] = 0
    data['ATT10'] = np.log1p(data['ATT10'])
    data['ATT13'] = np.log1p(data['ATT13'])
    data['ATT14'] = np.log1p(data['ATT14'])
    data['ATT15'] = np.log1p(data['ATT15'])
    data['ATT17'] = np.log1p(data['ATT17'])
    data['ATT19'] = np.log1p(data['ATT19'])
    data['ATT20'] = np.log1p(data['ATT20'])
    data['ATT21'] = np.log1p(data['ATT21'])
    data['ATT24'] = np.log1p(data['ATT24'])

    data['ATT12AbsLog'] = np.log1p(np.absolute(data['ATT12']))
    data['ATT12'] = np.sign(data['ATT12'])
    data['ATT23AbsLog'] = np.log1p(np.absolute(data['ATT23']))
    data['ATT23'] = np.sign(data['ATT23'])

    return data


def analize_company_explain(loaded_model, y_predict_r, my_company_data):
    """
    : param loaded_model machine learning model
    : param y_predict_r rounded prediction of company
    : param my_company_data data for company
    """
    y_predict_r = np.round(y_predict_r, 1)

    optimised_random_forest = loaded_model.steps[-1]
    prediction, bias, contributions = ti.predict(optimised_random_forest[1][1], my_company_data)
    util.myprint(prediction)
    util.myprint(bias)
    local_res = list()

    y_pred_r_colors = list()
    for i in range(len(y_predict_r)):
        if y_predict_r[i] > ariskparametri.YearlyYellow:
            if y_predict_r[i] > ariskparametri.YearlyRed:
                y_pred_r_colors.append(ariskparametri.ReportBarRosso)
            else:
                y_pred_r_colors.append(ariskparametri.ReportBarGiallo)
        else:
            y_pred_r_colors.append(ariskparametri.ReportBarVerde)

    for i in range(len(contributions)):
        res0, res1 = map(list, zip(*contributions[i]))
        util.myprint(res0)
        local_res.append(res1)

    return local_res


def analyze_company(my_company_info, my_company_data, ind_familiarita):
    """
    : param my_company_info information of company
    : param my_company_data data od company
    : param ind_familiarita I still don't know
    """
    y_pred_r = list()

    my_company_data = my_company_data.values.reshape(1, -1)

    util.myprint(os.getcwd())
    loaded_model = pickle.load(open(ariskparametri.fileTrain1Y, 'rb'))
    y_pred_r.extend(loaded_model.predict_proba(my_company_data)[:, 1])

    loaded_model = pickle.load(open(ariskparametri.fileTrain2Y, 'rb'))
    y_pred_r.extend(loaded_model.predict_proba(my_company_data)[:, 1])

    loaded_model = pickle.load(open(ariskparametri.fileTrain3Y, 'rb'))
    y_pred_r.extend(loaded_model.predict_proba(my_company_data)[:, 1])

    y_pred_r = np.round(y_pred_r, 1)

    util.myprint(y_pred_r)
    print(my_company_data[0])
    print(len(my_company_data))
    optimised_random_forest = loaded_model.steps[-1]
    prediction, bias, contributions = ti.predict(optimised_random_forest[1][1], my_company_data)
    util.myprint(bias)
    util.myprint(prediction)
    res = list()

    y_pred_r_colors = list()
    for i in range(len(y_pred_r)):
        if y_pred_r[i] > ariskparametri.YearlyYellow:
            if y_pred_r[i] > ariskparametri.YearlyRed:
                y_pred_r_colors.append(ariskparametri.ReportBarRosso)
            else:
                y_pred_r_colors.append(ariskparametri.ReportBarGiallo)
        else:
            y_pred_r_colors.append(ariskparametri.ReportBarVerde)

    all_value = 0.0
    for i in range(3):
        all_value = all_value + y_pred_r[i] * ariskparametri.mediaPesataAnni[i]

    if all_value > ariskparametri.OverallYellow:
        if all_value > ariskparametri.OverallRed:
            all_value_color = ariskparametri.ReportBarRosso
            all_table_color = ariskparametri.ReportSfondoRosso
        else:
            all_value_color = ariskparametri.ReportBarGiallo
            all_table_color = ariskparametri.ReportSfondoGiallo
    else:
        all_value_color = ariskparametri.ReportBarVerde
        all_table_color = ariskparametri.ReportSfondoVerde

    for i in range(len(contributions)):
        res0, res1 = map(list, zip(*contributions[i]))
        util.myprint(res0)
        res.append(res1)

    util.myprint(res)
    red_det_res_names = list()
    red_det_res_values = list()
    red_det_res_idx = list()
    flatten_data = my_company_data.flatten()
    util.myprint(np.sort(res))
    for i in np.argsort(np.negative(res)).flatten():
        if res[0][i] >= 0.001:
            util.myprint(str(res[0][i]) + " " + ariskparametri.indices[i])
            red_det_res_names.append(ariskparametri.indices[i])
            red_det_res_values.append(flatten_data[i])
            red_det_res_idx.append(i)

    ai_4_bc_predict_input = my_company_data
    delta, ai_4_bc_pred_value, ai_4_bc_names = \
        analyze_company_bc(ai_4_bc_predict_input, red_det_res_idx, ind_familiarita)

    util.myprint("delta " + str(delta))
    util.myprint(ai_4_bc_pred_value)
    util.myprint(ai_4_bc_names)

    if ai_4_bc_pred_value > ariskparametri.AI4BCYellow:
        if ai_4_bc_pred_value > ariskparametri.AI4BCRed:
            ai_4_bc_color = ariskparametri.ReportSfondoRosso
        else:
            ai_4_bc_color = ariskparametri.ReportSfondoGiallo
    else:
        ai_4_bc_color = ariskparametri.ReportSfondoVerde

    delta = 0.7
    ai_4_risk_pred_input = my_company_data
    for idx, item in enumerate(red_det_res_idx):
        ai_4_risk_pred_input[0][red_det_res_idx[idx]] = ai_4_risk_pred_input[0][red_det_res_idx[idx]] * (1 + delta)

    ai_4_risks_pred_value = 0.0

    loaded_model = pickle.load(open(ariskparametri.fileTrain1Y, 'rb'))
    ai_4_risks_pred_value = ai_4_risks_pred_value + (loaded_model.predict_proba(ai_4_risk_pred_input)[:, 1])
    loaded_model = pickle.load(open(ariskparametri.fileTrain2Y, 'rb'))
    ai_4_risks_pred_value = ai_4_risks_pred_value + (loaded_model.predict_proba(ai_4_risk_pred_input)[:, 1])
    loaded_model = pickle.load(open(ariskparametri.fileTrain3Y, 'rb'))
    ai_4_risks_pred_value = ai_4_risks_pred_value + (loaded_model.predict_proba(ai_4_risk_pred_input)[:, 1])
    ai_4_risks_pred_value = ai_4_risks_pred_value / 3

    if ai_4_risks_pred_value > ariskparametri.AI4RiskYellow:
        if ai_4_risks_pred_value > ariskparametri.AI4RiskRed:
            ai_4_risk_color = ariskparametri.ReportSfondoRosso
        else:
            ai_4_risk_color = ariskparametri.ReportSfondoGiallo
    else:
        ai_4_risk_color = ariskparametri.ReportSfondoVerde

    ai_4_risk_names = list()
    ai_4_risk_names.append('Rapporto Soci/Governance')
    # print(ai_4_bc_names)
    # print(os.path.join(os.path.dirname(__file__)))
    print(my_company_info)
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template-report')))
    template = env.get_template('template-short.html')
    report = template.render(Azienda=my_company_info['ATT1'].values[0],
                             companyAnagr=['Azienda', 'Partita IVA', 'Codice ATECO 2007'],
                             companyAnagrValue=[my_company_info['ATT1'].values[0], my_company_info['ATT3'].values[0],
                                                my_company_info['ATT6'].values[0]],
                             companyData=ariskparametri.indices,
                             companyDataValue=flatten_data,
                             Values=y_pred_r,
                             ScoreParams=red_det_res_names,
                             ScoreParamsValue=red_det_res_values,
                             ScoreParamsText=red_det_res_names,
                             OverallValue=all_value,
                             OverallValueColor=all_value_color,
                             ValuesColor=y_pred_r_colors,
                             AI4BCValue=ai_4_bc_pred_value,
                             AI4RisksValue=ai_4_risks_pred_value,
                             reportCreated=date.today(),
                             EQFStart=my_company_info['EQFStart'].values[0],
                             EQFEnd=my_company_info['EQFEnd'].values[0],
                             AQStart=my_company_info['AQStart'].values[0],
                             AQEnd=my_company_info['AQStart'].values[0],
                             AI4REDFlagsLevelColor=all_table_color,
                             AI4BCLevelColor=ai_4_bc_color,
                             AI4RiskLevelColor=ai_4_risk_color,
                             AI4BCScoreParams=ai_4_bc_names,
                             AI4RiskScoreParams=ai_4_risk_names
                             )
    # print(report)
    return report


def get_crisis(train, trained_filename, level):
    """
    : param train data file to do prediction and analyse
    : param trained_filename machine learning model pickle
    : param level threshold to check failure of company
     """
    loaded_model = pickle.load(open(trained_filename, 'rb'))
    y_pred = (loaded_model.predict_proba(train)[:, 1] >= level)
    y_pred_r = loaded_model.predict_proba(train)[:, 1]
    y_pred_r = np.round(y_pred_r, 1)

    return y_pred, y_pred_r


def get_detailed_report(train, trained_filename):
    """
    : param train data file to do prediction and analyse
    : param trained_filename machine learning model pickle
    """
    loaded_model = pickle.load(open(trained_filename, 'rb'))

    optimised_random_forest = loaded_model.steps[-1]
    prediction, bias, contributions = ti.predict(optimised_random_forest[1][1], train)
    util.myprint(prediction)
    util.myprint(bias)
    indices = [
        'Ricavi delle vendite',
        'EBITDA/Vendite (%)',
        'EBITDA migl EUR',
        'Indice di liquidità',
        'Indice corrente',
        'Indice di indebitam. a lungo',
        'Indice di copertura delle immob. (patrimoniale)',
        'Grado di ammortamento',
        'Debiti v/banche su fatt. (%)',
        'Grado di copertura degli interessi passivi',
        'Giac. media delle scorte (gg)',
        'Giorni copertura scorte (gg)',
        'Redditività di tutto il capitale investito (ROI) (%)',
        'Flusso di cassa di gestione',
        'Oneri finanz. su fatt. (%)'
    ]

    for i in range(5):

        print("Feature contributions:")
        res0, res1 = map(list, zip(*contributions[i]))
        util.myprint(res0)
        for idx, feature in sorted(zip(res1, indices), key=lambda x: -abs(x[0])):
            print(feature, abs(round(idx, 2)))
        print("-" * 20)

    res = list()
    for i in range(len(contributions)):
        res0, res1 = map(list, zip(*contributions[i]))
        util.myprint(res0)
        res.append(res1)

    det_res = pd.DataFrame(np.abs(res))

    return det_res


def json_data_empty(json_data_to_check):
    """
    :param json_data_to_check to check in json file is not empty
    """
    check_result = True
    if (json_data_to_check is None) or (str(json_data_to_check).strip() == ""):
        check_result = False
    return check_result


def check_survey_data(json_data):
    """
    : param json_data json file to check correctness
    """
    check_result = True

    ind_finanziari = json_data['InData']['AQ']['input'][2]['fixedRows']
    check_result = check_result and json_data_empty(ind_finanziari[8]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[9]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[10]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[5]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[11]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[12]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[13]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[14]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[15]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[16]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[17]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[18]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[19]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[20]['values'][0]['value'])
    check_result = check_result and json_data_empty(ind_finanziari[21]['values'][0]['value'])

    return check_result


def analyze_company_bc(pred_input, red_det_res_idx, bc_data):
    """
    make the prediction for A!4BC
    :param pred_input: Input of the Machine Learning
    :param red_det_res_idx: Indexes of the PredInput that can be modified
    :param bc_data: Data for making the analisys
    :return: myDelda: delta modifications of the finance, predValues: values of the data oin BCData that forced the
    prediction, predSources: texts to be discplayed related to the values that made the prediction
    """

    pred_sources = list()
    my_delta = 0.0

    maggioranza = int(bc_data[1]['fixedRows'][0]['values'][0]['value'] or 0)
    util.myprint(len(bc_data[0]['value']))
    util.myprint(maggioranza)
    percsoci = list()
    socipermaggioranza = int(0)
    quotamaggioranza = int(0)

    if len(bc_data[0]['value']) == 0:
        quotamaggioranza = 0

    if len(bc_data[0]['value']) > 0:
        for i in range(len(bc_data[0]['value'])):
            percsoci.append(int(bc_data[0]['value'][i]['QUOTE'] or 0))
        percsoci.sort(reverse=True)
        for idx, item in enumerate(percsoci):
            if quotamaggioranza <= 51:
                socipermaggioranza = socipermaggioranza + 1
                quotamaggioranza += percsoci[idx]
        util.myprint(socipermaggioranza)
        util.myprint(quotamaggioranza)

    socipermaggioranza = max(socipermaggioranza, maggioranza)

    if socipermaggioranza == 0:
        my_delta = ariskparametri.myDelta[2]
        pred_sources.append(ariskparametri.ai4BCErrors[0])
    elif socipermaggioranza <= 1:
        my_delta = ariskparametri.myDelta[2]
        pred_sources.append(ariskparametri.ai4BCErrors[2])
    elif socipermaggioranza <= 3:
        my_delta = ariskparametri.myDelta[1]
        pred_sources.append(ariskparametri.ai4BCErrors[3])
    else:
        my_delta = max(my_delta, ariskparametri.myDelta[0])

    util.myprint(pred_input)

    for idx, item in enumerate(red_det_res_idx):
        pred_input[0][red_det_res_idx[idx]] = pred_input[0][red_det_res_idx[idx]] * (1 + my_delta)

    print('tutto ok')

    util.myprint(pred_input)
    pred_values = 0.0

    loaded_model = pickle.load(open(ariskparametri.fileTrain1Y, 'rb'))
    pred_values = \
        pred_values + np.round((loaded_model.predict_proba(pred_input)[:, 1]), 1) * ariskparametri.mediaPesataAnniBC[0]
    print(pred_values, '1')
    util.myprint("anno 1" + " " + str(loaded_model.predict_proba(pred_input)[:, 1]))
    loaded_model = pickle.load(open(ariskparametri.fileTrain2Y, 'rb'))
    pred_values = \
        pred_values + np.round((loaded_model.predict_proba(pred_input)[:, 1]), 1) * ariskparametri.mediaPesataAnniBC[1]
    print(pred_values, '2')
    util.myprint("anno 2" + " " + str(loaded_model.predict_proba(pred_input)[:, 1]))
    loaded_model = pickle.load(open(ariskparametri.fileTrain3Y, 'rb'))
    pred_values = \
        pred_values + np.round((loaded_model.predict_proba(pred_input)[:, 1]), 1) * ariskparametri.mediaPesataAnniBC[1]
    print(pred_values, '3')
    util.myprint("anno 3" + " " + str(loaded_model.predict_proba(pred_input)[:, 1]))
    print(my_delta)
    print(pred_values)
    print(pred_sources)

    return my_delta, pred_values, pred_sources
