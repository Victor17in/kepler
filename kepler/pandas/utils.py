
__all__ = ['load', 'drop_ring_columns']

import gc
from Gaugi import Logger
from Gaugi.messenger.macros import *
from Gaugi import load as gload
from Gaugi import GeV

import pandas as pd
import numpy as np

from kepler.utils import load_ringer_models

#
# Load npz format from kepler dumper and convert to pandas like
#
def load( path ):
    '''
    This function will get a .npz file and transform into a pandas DataFrame. 
    The .npz has three types of data: float, int and bool this function will concatenate these features and reorder them.

    Arguments:
    path (str) - the full path to .npz file
    '''
    # open the file
    d = dict(np.load(path, allow_pickle=True))    
    # create a list of temporary dataframes that should be concateneted into a final one
    df_list = []
    for itype in ['float', 'int', 'bool', 'object']:
        df_list.append(pd.DataFrame(data=d['data_%s' %itype], columns=d['features_%s' %itype]))
    # concat the list
    df = pd.concat(df_list, axis=1)
    # return the DataFrame with ordered features.
    df = df[d['ordered_features']]
    # add the target information
    df['target'] = d['target']
    # remove the list of DataFrame and collect into garbage collector
    del df_list, d
    gc.collect()
    return df

#
# Helper to drop all rings
#
def drop_ring_columns( df , rings=100):
    '''
    This function is a shortcut to drop the rings column from a given dataframe.
    
    Arguments:
    df (pd.DataFrame) - a pandas DataFrame that has rings;
    rings (int) - the number of rings that want remove from DataFrame.
    '''
    if type(rings) is int:
        rings = [idx for idx in range(rings)]
    df.drop( ['trig_L2_cl_ring_%d'%i for i in rings], axis=1, inplace=True )

