
__all__ = ['RingerDecorator']

from Gaugi import Logger
from Gaugi.messenger.macros import *
from Gaugi import load, GeV

import pandas as pd
import numpy as np

from kepler.utils import load_ringer_models
from kepler.emulator import get_chain_dict




#
# Class responsible to propagate the ringer decision throut the pandas frame and append the decision and output
#
class RingerDecorator(Logger):

    #
    # Constructor
    #
    def __init__( self, tuning, generator , et_column = 'trig_L2_cl_et', eta_column = 'trig_L2_cl_eta'):

        Logger.__init__(self)

        if type(tuning) is str:
            MSG_INFO(self, 'Reading... %s', tuning)
            self.__tuning, _ = load_ringer_models(tuning)
        else:
            # Should be a dict([models,thresholds, model_et/etabins and threshold_et/etabins])
            self.__tuning = tuning 
        # function to prepare data input
        self.__generator = generator
        self.et_column = et_column
        self.eta_column = eta_column


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
