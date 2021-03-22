import gspread
import pandas as pd
import datetime

import utils

gc = gspread.service_account()


def pull_ecoevo():
    data_start_row = 3
    sh = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1hf_q-3gdyOlsk97I3OW97w_cmQXsKQVC-ZGDMgFnL2I/edit#gid=1954069648"
    )

    dt_raw_faculty = sh.values_batch_get(
        [
            "Faculty Jobs!G3:G",
            "Faculty Jobs!D3:D",
            "Faculty Jobs!B3:B",
            "Faculty Jobs!J3:J",
            "Faculty Jobs!E3:E",
            "Faculty Jobs!F3:F",
        ]
    )

    dt_faculty = pd.DataFrame(
        {
            "rank": dt_raw_faculty["valueRanges"][0]["values"],
            "subject": dt_raw_faculty["valueRanges"][1]["values"],
            "institution": dt_raw_faculty["valueRanges"][2]["values"],
            "notes": dt_raw_faculty["valueRanges"][3]["values"],
            "closing_date": dt_raw_faculty["valueRanges"][4]["values"],
            "url": dt_raw_faculty["valueRanges"][5]["values"],
        }
    )
    dt_faculty = dt_faculty.applymap(lambda x: "".join(map(str, x)))

    dt_raw_postdoc = sh.values_batch_get(
        [
            "Postdoc Jobs!G3:G",
            "Postdoc Jobs!D3:D",
            "Postdoc Jobs!B3:B",
            "Postdoc Jobs!I3:I",
            "Postdoc Jobs!F3:F",
            "Postdoc Jobs!G3:G",
        ]
    )

    dt_postdoc = pd.DataFrame(
        {
            "rank": dt_raw_postdoc["valueRanges"][0]["values"],
            "subject": dt_raw_postdoc["valueRanges"][1]["values"],
            "institution": dt_raw_postdoc["valueRanges"][2]["values"],
            # "notes": dt_raw_postdoc['valueRanges'][3]['values'],
            "closing_date": dt_raw_postdoc["valueRanges"][4]["values"],
            "url": dt_raw_postdoc["valueRanges"][5]["values"],
        }
    )
    dt_postdoc = dt_postdoc.applymap(lambda x: "".join(map(str, x)))
    dt_postdoc["rank"] = "Postdoc"
    # temporarily account for bad closing_date field
    # TODO: set nondate objects in the closing_date to an arbitrary future date
    dt_postdoc["closing_date"] = datetime.date.today().strftime("%m/%d/%Y")

    dt = pd.concat([dt_faculty, dt_postdoc])
    dt["source"] = "[ecoevojobs]"

    # remove closing_date < today
    dt["closing_date"] = pd.to_datetime(dt["closing_date"])
    dt = dt.loc[dt["closing_date"] >= pd.to_datetime(datetime.date.today())]

    subject = (
        dt["rank"]
        + " | "
        + dt["subject"]
        + " | "
        + dt["institution"]
        + " | "
        + dt["url"]
        + " | "
        + dt["source"]
    )
    body = dt["notes"]

    res = pd.DataFrame({"subject": subject, "body": body, "source": dt["source"]})

    res = utils.filter_limno(res)

    return res


def pull_earthenvscience():
    data_start_row = 7
    sh = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/16Qcgpe3_zx3EOCXe5vElev22OhiGtlI2YkukLHfNWf0/edit#gid=1017187727"
    )

    dt_raw = sh.values_batch_get(
        [
            "Faculty/Permanent Jobs!H8:H",  # rank
            "Faculty/Permanent Jobs!F8:F",  # subject
            "Faculty/Permanent Jobs!B8:B",  # institution
            "Faculty/Permanent Jobs!M8:M",  # notes
            "Faculty/Permanent Jobs!C8:C",  # closing_date
            "Faculty/Permanent Jobs!E8:E",  # url
        ]
    )

    dt = pd.DataFrame(
        {
            "rank": dt_raw["valueRanges"][0]["values"],
            "subject": dt_raw["valueRanges"][1]["values"],
            "institution": dt_raw["valueRanges"][2]["values"],
            # "notes": dt_raw['valueRanges'][3]['values'],
            "closing_date": dt_raw["valueRanges"][4]["values"],
            "url": dt_raw["valueRanges"][5]["values"],
        }
    )
    dt = dt.applymap(lambda x: "".join(map(str, x)))
    dt["source"] = "[earthenvscience]"

    # remove closing_date < today
    dt = dt.loc[dt["closing_date"].str.len() > 0]
    dt = dt.loc[dt["closing_date"].str.len() < 15]
    dt["closing_date"] = pd.to_datetime(dt["closing_date"])
    dt = dt.loc[dt["closing_date"] >= pd.to_datetime(datetime.date.today())]

    subject = (
        dt["rank"]
        + " | "
        + dt["subject"]
        + " | "
        + dt["institution"]
        + " | "
        + dt["url"]
        + " | "
        + dt["source"]
    )
    body = ""

    res = pd.DataFrame({"subject": subject, "body": body, "source": dt["source"]})

    res = utils.filter_limno(res)

    return res


# pull_ecophys