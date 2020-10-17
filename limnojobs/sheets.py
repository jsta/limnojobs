import gspread
import pandas as pd
import utils

gc = gspread.service_account()

# pull_ecoevo
data_start_row = 3
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1hf_q-3gdyOlsk97I3OW97w_cmQXsKQVC-ZGDMgFnL2I/edit#gid=1954069648")

dt_raw = sh.values_batch_get([
    'Faculty Jobs!G3:G',
    'Faculty Jobs!D3:D',
    'Faculty Jobs!B3:B',
    'Faculty Jobs!J3:J'    
    ])

dt = pd.DataFrame({
    "rank": dt_raw['valueRanges'][0]['values'],
    "subject": dt_raw['valueRanges'][1]['values'],
    "institution": dt_raw['valueRanges'][2]['values'], 
    "notes": dt_raw['valueRanges'][3]['values']    
})
dt = dt.applymap(lambda x:  ''.join(map(str, x)))

subject = dt['rank'] + ' | ' + dt['subject'] + ' | ' + dt['institution'] 
body = dt['notes']

res = pd.DataFrame({
    "subject": subject,
    "body": body
})

test = utils.filter_limno(res)

# subject = rank + subject_area + institution
# body = notes

str(inst_list)

# pull_earthenvscience
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/16Qcgpe3_zx3EOCXe5vElev22OhiGtlI2YkukLHfNWf0/edit#gid=1017187727")

# pull_ecophys