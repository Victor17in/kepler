
__all__ = ["Efficiency", "restore_efficiencies"]


from Gaugi import GeV
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import StoreGate
from Gaugi import Logger
from Gaugi.messenger.macros import *

from kepler.analysis.constants import etabins, zee_etbins, mubins
from kepler.analysis.efficiency.utils import GetProfile, FillHistogram
from kepler.menu import get_chain_dict
from ROOT import TH1F, TH2F

import numpy as np
import array



#
# Efficiency 
#
class Efficiency( Logger ):
  
  __steps = ['L1Calo','L2Calo','L2','EFCalo','HLT']

  #
  # Constructor
  #
  def __init__(self, triggers, output,  etbins = zee_etbins, 
                                        etabins = etabins, 
                                        mubins = mubins ):

    Logger.__init__(self)
    self.triggers = triggers
    self.etbins = array.array('d',etbins) if not type(etbins) is array.array else etbins
    self.etabins = array.array('d',etabins) if not type(etabins) is array.array else etabins
    self.mubins = array.array('d',mubins) if not type(mubins) is array.array else mubins

    if type(output) is str: # We should create a new store gate
      MSG_INFO(self, "Creating the StoreGate service with path: %s", output)
      self.__store = StoreGate(output)
      self.configure()
    elif type(output) is StoreGate: # Using an external store gate
      self.__store = output
    else:
      MSG_FATAL(self, "Output type should be a str (path) or the StoreGate object.")


  def __del__(self):
    self.store().write()
    

  #
  # Get the store gate service
  #
  def store(self):
    return self.__store


  #
  # Initialize
  #
  def configure(self):

    sg = self.store()

    # Loop over all triggers
    for trigger in self.triggers:
      # Loop over all trigger steps
      for step in self.__steps :

        sg.mkdir( trigger+'/'+step )
        sg.addHistogram(TH1F('et','E_{T} distribution;E_{T};Count', len(self.etbins)-1, self.etbins ))
        sg.addHistogram(TH1F('eta','#eta distribution;#eta;Count', len(self.etabins)-1, self.etabins))
        sg.addHistogram(TH1F("phi", "#phi distribution; #phi ; Count", 20, -3.2, 3.2))
        sg.addHistogram(TH1F('mu' ,'<#mu> distribution;<#mu>;Count', len(self.mubins)-1, self.mubins))
        sg.addHistogram(TH1F('match_et','E_{T} matched distribution;E_{T};Count', len(self.etbins)-1, self.etbins))
        sg.addHistogram(TH1F('match_eta','#eta matched distribution;#eta;Count', len(self.etabins)-1, self.etabins))
        sg.addHistogram(TH1F("match_phi", "#phi matched distribution; #phi ; Count", 20, -3.2, 3.2))
        sg.addHistogram(TH1F('match_mu' ,'<#mu> matched distribution;<#mu>;Count', len(self.mubins)-1, self.mubins))

        # for boosted analysis
        #deltaR_bins = np.arange(0, 5, step=0.1)
        #sg.addHistogram(TH1F('deltaR','#\Delta R distribution;#\Delta R;Count', len(deltaR_bins)-1, deltaR_bins))
        #sg.addHistogram(TH1F('match_deltaR','#\Delta R matched distribution;#\Delta R;Count', len(deltaR_bins)-1, deltaR_bins))
        #sg.addHistogram(TProfile('eff_deltaR', "#\epsilon(#\Delta R); #\Delta R ; Efficiency" , len(deltaR_bins)-1, deltaR_bins))


  #
  # Fill a specific trigger
  #
  def fill(self, df, trigger, pidname = None):
  
    sg = self.store()
    d = get_chain_dict(trigger)
    etthr = d['etthr']
    if pidname:
      df_temp = df.loc[ (df[pidname] == True) & (df['et'] >= (etthr - 5)*GeV) & (abs(df['eta']) <= 2.47) ]  
    else: # in case of non-electron samples, we should not applied any offline requirement
      df_temp = df.loc[ (df['et'] >= (etthr - 5)*GeV) & (abs(df['eta']) <= 2.47) ]

    # Fill efficiency histograms
    def fill_histograms( path, df , col_name, etthr):
      # Fill denominator
      FillHistogram( sg.histogram(path+'/et'), df['et'].values / GeV )
      # et > etthr + 1
      df_temp = df.loc[ (df['et'] > (etthr + 1)*GeV ) ]
      FillHistogram( sg.histogram(path+'/eta'), df_temp['eta'].values )
      FillHistogram( sg.histogram(path+'/phi'), df_temp['phi'].values )
      FillHistogram( sg.histogram(path+'/mu' ), df_temp['avgmu'].values )
      # Fill numerator
      df_temp = df.loc[ df[col_name] == True ]
      FillHistogram( sg.histogram(path+'/match_et'), df_temp['et'].values / GeV )
      df_temp = df_temp.loc[ (df_temp['et'] > (etthr + 1)*GeV ) ]
      FillHistogram( sg.histogram( path+'/match_eta' ), df_temp['eta'].values )
      FillHistogram( sg.histogram( path+'/match_phi' ), df_temp['phi'].values )
      FillHistogram( sg.histogram( path+'/match_mu'  ), df_temp['avgmu'].values )

    # Fill each trigger step
    fill_histograms(trigger+'/L1Calo', df_temp, 'L1Calo_'+trigger, etthr )
    fill_histograms(trigger+'/L2Calo', df_temp, 'L2Calo_'+trigger, etthr )
    fill_histograms(trigger+'/L2'    , df_temp, 'L2_'    +trigger, etthr )
    fill_histograms(trigger+'/EFCalo', df_temp, 'EFCalo_'+trigger, etthr )
    fill_histograms(trigger+'/HLT'   , df_temp, 'HLT_'   +trigger, etthr )  



  def numerator(self, trigger, var):
    step = trigger.split('_')[0]
    name = trigger.replace(step+'_', '')
    return self.store().histogram(name+'/'+step+'/match_'+var)

  def denominator(self, trigger, var):
    step = trigger.split('_')[0]
    name = trigger.replace(step+'_', '')
    return self.store().histogram(name+'/'+step+'/'+var)

  def profile(self, trigger, var):
    return GetProfile(self.numerator(trigger,var), self.denominator(trigger,var))



#
# Load all efficiencies from a ROOT file
#
def restore_efficiencies( path ):
  from Gaugi import restoreStoreGate
  store = restoreStoreGate(path)
  dirs = store.getDirs()
  triggers = np.unique([ dir.split('/')[1] for dir in dirs]).tolist()
  return Efficiency( triggers, store )




