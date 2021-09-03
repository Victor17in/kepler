
__all__ = ['load', 'drop_ring_columns', 'RingerDecorator']

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
    df = pd.DataFrame( d['data'], columns=d['features'] )
    # concatenate the target
    target = d['target']
    df['target'] = target
    return df

#
# Helper to drop all rings
#
def drop_ring_columns( df , rings=100):
    if type(rings) is int:
        rings = [idx for idx in range(rings)]
    df.drop( ['trig_L2_cl_ring_%d'%i for i in rings], axis=1, inplace=True )


#
# Class responsible to propagate the ringer decision throut the pandas frame and append the decision and output
#
class RingerDecorator(Logger):

    #
    # Constructor
    #
    def __init__( self, path, generator , et_column = 'trig_L2_cl_et', eta_column = 'trig_L2_cl_eta'):

        Logger.__init__(self)
        self.path = path
        # function to prepare data input
        self.__generator = generator
        self.et_column = et_column
        self.eta_column = eta_column

        # configure 
        self.configure()


    #
    # Load the tuning
    #
    def configure(self):
        MSG_INFO(self, 'Reading... %s', self.path)
        self.__tuning, _ = load_ringer_models(self.path)


    #
    # Decorate the pandas dataframe with output and decision and store into col_name
    #
    def apply(self, df, col_name):

        df[col_name+'_output'] = np.nan
        df[col_name] = np.nan

        et_bins = self.__tuning['model_etBins']
        eta_bins = self.__tuning['model_etaBins']
   
        # Get L2 values
        et = df[self.et_column].values / GeV
        eta = abs(df[self.eta_column].values)

        # Get the et/eta bin
        etBinIdx = np.digitize( et, et_bins, right=False) - 1
        etaBinIdx = np.digitize( eta, eta_bins, right=False) - 1

        df['etBinIdx'] = etBinIdx
        df['etaBinIdx'] = etaBinIdx

        # Propagate the input and append the output into the dataframe
        for et_bin in df['etBinIdx'].unique():
            for eta_bin in df['etaBinIdx'].unique():
                df_temp = df.loc[ (df['etBinIdx'] == et_bin) & (df['etaBinIdx'] == eta_bin) ]
                if df_temp.shape[0] > 0:
                    MSG_INFO(self, 'Propagate for bin (%d, %d)', et_bin, eta_bin) 
                    model = self.__tuning['models'][et_bin][eta_bin]
                    output = model.predict(self.__generator(df_temp), verbose=1)
                    df.at[df_temp.index, col_name+'_output'] = output

        if df[col_name+'_output'].isnull().sum():
            MSG_WARNING(self, 'There is nan values into the %s_output column. Please check!', col_name)

        #
        # Now lets take the decision using the output
        #
        et_bins = self.__tuning['threshold_etBins']
        eta_bins = self.__tuning['threshold_etaBins']
        # Get the et/eta bin
        etBinIdx = np.digitize( et, et_bins, right=False) - 1
        etaBinIdx = np.digitize( eta, eta_bins, right=False) - 1

        df['etBinIdx'] = etBinIdx
        df['etaBinIdx'] = etaBinIdx

        # Take the decision
        for et_bin in df['etBinIdx'].unique():
            for eta_bin in df['etaBinIdx'].unique():
                df_temp = df.loc[ (df['etBinIdx'] == et_bin) & (df['etaBinIdx'] == eta_bin) ]
                if df_temp.shape[0] > 0:
                    MSG_INFO(self, 'Decide for bin (%d, %d)', et_bin, eta_bin) 
                    c = self.__tuning['thresholds'][et_bin][eta_bin]
                    output = df_temp[col_name+'_output'].values 
                    thresholds = (df_temp['avgmu'].values * c['slope'] + c['offset'])
                    df.at[df_temp.index, col_name] = np.greater( output, thresholds )
        #df.drop('etBinIdx')

        if df[col_name].isnull().sum():
            MSG_WARNING(self, 'There is nan values into the %s_output column. Please check!', col_name)

        # drop temp columns
        df.drop(['etBinIdx', 'etaBinIdx'], axis=1, inplace=True)
