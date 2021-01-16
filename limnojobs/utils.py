import pandas as pd
import pkg_resources
import re
import numpy as np

def filter_limno(df):
    r"""Filter limnology themed jobs from a pandas DataFrame.
    :param df: pandas DataFrame with 'subject' and 'body' columns
    """

    keywords = pd.read_csv(pkg_resources.resource_filename('limnojobs',
                                                           'keywords.csv'))    
    filter_for = keywords['filter_for'].tolist()
    filter_for = [x for x in filter_for if str(x) != 'nan']
    filter_for = [x for x in filter_for if str(x) != ' ']
    filter_against = keywords['filter_against'].tolist()
    filter_against = [x for x in filter_against if str(x) != 'nan']
    filter_against = [x for x in filter_against if str(x) != ' ']

    # df = res
    df = df.reset_index()
    # df = df.iloc[0:2]

    has_limno_subject = df['subject'].str.contains('|'.join(filter_for),
                                               case = False)
    has_limno_body = df['body'].str.contains('|'.join(filter_for),
                                                   case = False)

    # save matching filter_for here
    is_limno = pd.DataFrame([has_limno_subject, has_limno_body]) \
        .transpose() \
        .sum(axis = 1) > 0

    df = df[is_limno]

    has_junk_subject = ~df['subject'].str.contains('|'.join(filter_against),
                                                   case = False)
    has_junk_body = ~df['body'].str.contains('|'.join(filter_against),
                                               case = False)

    # save matching filter_against here
    # if len(df.index) > 0:
    #     filter_against = keywords['filter_against'][
    #         keywords['filter_against'].apply(
    #             lambda x: df['body'].
    #             str.contains(x, case = False)).iloc[:, 0]]

    not_junk = pd.DataFrame([has_junk_subject, has_junk_body]) \
        .transpose() \
        .sum(axis = 1) == 2

    return df[not_junk]# ,
            #"filter_against": filter_against}

def get_maxlength_tuple(x):
    # x = test
    tuple_length = [len(y) for y in x]
    return x[tuple_length.index(max(tuple_length))]

def extract_url(body_raw):
    # breakpoint()
    body = [x.replace("=\\r\\n","") for x in body_raw]
    body = [x.replace("\\r\\n"," ") for x in body]
    body_split = re.split(r'\s', body[0])
    detect_url = lambda x: re.findall(r'((^\s.*\.edu(\/?)(\S+)?))|(((https?:\S+)))|(((www\.))\S+)', x)
    urls = [*map(detect_url, body_split)]
    if not any([len(url) > 0 for url in urls]):
        url = "https://www.esa.org/membership/ecolog/"
    else:        
        urls = np.array([get_maxlength_tuple(x[0]) if x != [] else x for x in urls], dtype="object")
        url = urls[np.array([len(x) > 0 for x in urls])][0]        
        url = "".join([x.replace(")","") for x in url])
        url = re.sub(r'\.$', '', url)
        url = re.sub(r'\,$', '', url)
        url = re.sub(r'\>$', '', url)

    # print(url)    
    return url
