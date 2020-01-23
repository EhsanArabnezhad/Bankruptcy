# -*- coding: utf-8 -*-

import os

# directories
# BaseDir = 'C:/Users/guido/OneDrive - Politecnico di Torino/Documenti/personali/startup/arisk/sviluppo/server-api'
# BaseDir = '/var/www/html/arisk-engine'

BaseDir = os.path.dirname(os.path.abspath(__file__))
ariskBaseDir = BaseDir
ariskStaticFiles = BaseDir+'/static/'
debug = False
# ariskBaseDir = 'D:/users/Guido/OneDrive -
# Politecnico di Torino/Documenti/personali/startup/arisk/modello-redflags/italy/'

# per Report
ReportBarVerde = "\"progress-bars1 cid-rCU8qeDahk\""
ReportBarRosso = "\"progress-bars1 cid-rCU9dON4cu\""
ReportBarGiallo = "\"progress-bars1 cid-rCU900AcwK\""

ReportFacciaRossa = "style=\"color: rgb(255, 51, 102); fill: rgb(255, 51, 102);\""
ReportFacciaGialla = "style=\"color: rgb(247, 237, 74); fill: rgb(247, 237, 74);\""

ReportSfondoRosso = "myerror"
ReportSfondoGiallo = "mywarning"
ReportSfondoVerde = "mysuccess"


OverallYellow = 0.4
OverallRed = 0.6

YearlyYellow = 0.5
YearlyRed = 0.7

AI4BCYellow = 0.4
AI4BCRed = 0.6

AI4RiskYellow = 0.4
AI4RiskRed = 0.6


indices = [
    'Ricavi delle vendite',
    'EBITDA/Vendite (%)',
    'EBITDA migl EUR',
    'Indice di liquidità',
    'Indice corrente',
    'Indice di indebitam. a lungo',
    'Indice di copertura delle immob. (patrimoniale)',
    'Grado di ammortamento',
    'Totale v/banche su fatt. (%)',
    'Grado di copertura degli interessi passivi',
    'Giac. media delle scorte (gg)',
    'Giorni copertura scorte (gg)',
    'Redditività di tutto il capitale investito (ROI) (%)',
    'Flusso di cassa di gestione',
    'Oneri finanz. su fatt. (%)',
    'aa',
    'bb'
]

indicesText = [
    'Ricavi delle vendite',
    'EBITDA/Vendite (%)',
    'EBITDA migl EUR',
    'Indice di liquidità',
    'Indice corrente',
    'Indice di indebitam. a lungo',
    'Indice di copertura delle immob. (patrimoniale)',
    'Grado di ammortamento',
    'Totale v/banche su fatt. (%)',
    'Grado di copertura degli interessi passivi',
    'Giac. media delle scorte (gg)',
    'Giorni copertura scorte (gg)',
    'Redditività di tutto il capitale investito (ROI) (%)',
    'Flusso di cassa di gestione',
    'Oneri finanz. su fatt. (%)'
]

fileTrain1Y = 'rf_clf1y.pkl'
fileTrain2Y = 'rf_clf2y.pkl'
fileTrain3Y = 'rf_clf3y.pkl'
fileTrain4Y = 'rf_clf4y.pkl'
fileTrain5Y = 'rf_clf5y.pkl'

mediaPesataAnni = [0.45, 0.32, 0.23]
# mediaPesataAnniBC = [0.34, 0.33, 0.33]
mediaPesataAnniBC = mediaPesataAnni

percentili = [0.9,
              0.855251142,
              0.823287671,
              0.8,
              0.763926941,
              0.731050228,
              0.68630137,
              0.631050228,
              0.522374429,
              0.4
              ]

myDelta = [0, 0.3, 0.9]

ai4BCErrors = ['Dati sulla compagine sociale inconsistenti',
               'Nulla da segnalare',
               'Numero di soci per la maggioranza minore di 2',
               'Numero di soci per la maggioranza minore di 4'
               ]

cols = ['ATT10', 'ATT11', 'ATT12', 'ATT13', 'ATT14', 'ATT15', 'ATT16', 'ATT17', 'ATT18', 'ATT19',
        'ATT20', 'ATT21', 'ATT22', 'ATT23', 'ATT24', 'ATT12AbsLog', 'ATT23AbsLog']

anagrafica_cols = [
        'ATT1',
        'ATT3',
        'ATT6'
    ]
