import pandas as pd
import pkg_resources

def filter_limno(df):
    r"""Filter limnology themed jobs from a pandas DataFrame.
    :param df: pandas DataFrame with 'subject' and 'body' columns
    """

    keywords = pd.read_csv(pkg_resources.resource_filename('limnojobs',
                                                           'keywords.csv'))
    filter_for = keywords['filter_for'].tolist()
    filter_for = [x for x in filter_for if str(x) != 'nan']
    filter_against = keywords['filter_against'].tolist()
    filter_against = [x for x in filter_against if str(x) != 'nan']

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
