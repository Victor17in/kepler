
__all__ = ['load', 'drop_ring_columns']

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
    d = gload(path)    
    columns = d['features'].tolist()
    dtype = d['dtypes'].tolist()
    df = pd.DataFrame( d['data'], columns = columns )
    df['target'] = d['target']
    columns.append('target')
    dtype.append('int')
    cdt={i[0]: eval(i[1]) for i in zip(columns, dtype)}
    df = df.astype(cdt)
    return df

#
# Helper to drop all rings
#
def drop_ring_columns( df , rings=100):
    if type(rings) is int:
        rings = [idx for idx in range(rings)]
    df.drop( ['trig_L2_cl_ring_%d'%i for i in rings], axis=1, inplace=True )

