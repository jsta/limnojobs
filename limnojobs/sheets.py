import gspread
import pandas as pd
import datetime

import limnojobs.utils

gc = gspread.service_account()

def pull_ecoevo():
    data_start_row = 3
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1hf_q-3gdyOlsk97I3OW97w_cmQXsKQVC-ZGDMgFnL2I/edit#gid=1954069648")

    dt_raw = sh.values_batch_get([
        'Faculty Jobs!G3:G',
        'Faculty Jobs!D3:D',
        'Faculty Jobs!B3:B',
        'Faculty Jobs!J3:J',
        'Faculty Jobs!E3:E',
        'Faculty Jobs!F3:F'
        ])

    dt = pd.DataFrame({
        "rank": dt_raw['valueRanges'][0]['values'],
        "subject": dt_raw['valueRanges'][1]['values'],
        "institution": dt_raw['valueRanges'][2]['values'], 
        "notes": dt_raw['valueRanges'][3]['values'],
        "closing_date": dt_raw['valueRanges'][4]['values'],
        "url": dt_raw['valueRanges'][5]['values']
    })
    dt = dt.applymap(lambda x:  ''.join(map(str, x)))
    dt['source'] = "[ecoevojobs]"

    # remove closing_date < today
    dt['closing_date'] = pd.to_datetime(dt['closing_date'])
    dt = dt.loc[dt['closing_date'] >= pd.to_datetime(datetime.date.today())]

    subject = dt['rank'] + ' | ' + dt['subject'] + ' | ' + dt['institution'] + \
              ' | ' + dt['url'] + ' | ' + dt['source']
    body = dt['notes']

    res = pd.DataFrame({
        "subject": subject,
        "body": body,
        "source": dt['source']
    })

    res = utils.filter_limno(res)

    return res

def pull_earthenvscience():
    data_start_row = 7
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/16Qcgpe3_zx3EOCXe5vElev22OhiGtlI2YkukLHfNWf0/edit#gid=1017187727")

    dt_raw = sh.values_batch_get([
        'Faculty/Permanent Jobs!H8:H', # rank
        'Faculty/Permanent Jobs!F8:F', # subject
        'Faculty/Permanent Jobs!B8:B', # institution
        'Faculty/Permanent Jobs!M8:M', # notes
        'Faculty/Permanent Jobs!C8:C', # closing_date
        'Faculty/Permanent Jobs!E8:E' # url
        ])

    dt = pd.DataFrame({
        "rank": dt_raw['valueRanges'][0]['values'],
        "subject": dt_raw['valueRanges'][1]['values'],
        "institution": dt_raw['valueRanges'][2]['values'], 
        # "notes": dt_raw['valueRanges'][3]['values'],
        "closing_date": dt_raw['valueRanges'][4]['values'],
        "url": dt_raw['valueRanges'][5]['values']
    })
    dt = dt.applymap(lambda x:  ''.join(map(str, x)))
    dt['source'] = "[earthenvscience]"

    # remove closing_date < today
    dt['closing_date'] = pd.to_datetime(dt['closing_date'])
    dt = dt.loc[dt['closing_date'] >= pd.to_datetime(datetime.date.today())]

    subject = dt['rank'] + ' | ' + dt['subject'] + ' | ' + dt['institution'] + \
              ' | ' + dt['url'] + ' | ' + dt['source']
    body = ''

    res = pd.DataFrame({
        "subject": subject,
        "body": body,
        "source": dt['source']
    })

    res = utils.filter_limno(res)

    return res

# pull_ecophys