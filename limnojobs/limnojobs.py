import pandas as pd
import pkg_resources

keywords = pd.read_csv(pkg_resources.resource_filename('limnojobs',
                                                           'keywords.csv'))