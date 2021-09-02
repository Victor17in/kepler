
__all__ = ["FastCaloSelectorTool", "FastPhotonSelectorTool", "RingerSelectorTool"]

from Gaugi.messenger.macros import *
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi import ToolSvc

from kepler.menu import treat_trigger_dict_type
from kepler.emulator import Accept
from kepler.utils import get_bin_indexs, load_ringer_models

from tensorflow.keras.models import model_from_json

import numpy as np
import os 

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


#
# Selector tool
#
class FastPhotonSelectorTool( Algorithm ):

  __property = [ "WPName"]

  #
  # Contructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)
    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)


  #
  # Initialize method
  #
  def initialize(self):
    self.__hypos = []
    thrs = [0.0, 12.0,17.0,22.0,32.0,44.0]
    for idx, threshold in enumerate(thrs):
      from kepler.emulator.TrigEgammaFastPhotonHypoTool import configure
      hypo = configure( self._name + "_" + str(idx) , threshold, pidname)
      if hypo.initialize().isFailure():
        return StatusCode.FAILURE
      self.__hypos.append(hypo)

    self.init_lock()
    return StatusCode.SUCCESS



   #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):

    fc = context.getHandler( "HLT__TrigEMClusterContainer" )
    et = fc.et()
    passed = False  
    if et < 10*GeV:
      passed = self.__hypos[0].accept(context)
    elif et>=10*GeV and et < 15*GeV:
      passed = self.__hypos[1].accept(context)
    elif et>=15*GeV and et < 20*GeV:
      passed = self.__hypos[2].accept(context)
    elif et>=20*GeV and et < 30*GeV:
      passed = self.__hypos[3].accept(context)
    elif et>=30*GeV and et < 40*GeV:
      passed = self.__hypos[4].accept(context)
    else:
      passed =  self.__hypos[5].accept(context)
    return passed



  #
  # Finalize method
  #
  def finalize(self):
    for hypo in self.__hypos:
      if hypo.finalize().isFailure():
        return StatusCode.FAILURE

    return StatusCode.SUCCESS







#
# Selector tool
#
class FastCaloSelectorTool( Algorithm ):

  __property = [ "WPName"]

  #
  # Contructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)
    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)


  #
  # Initialize method
  #
  def initialize(self):
    self.__hypos = []
    thrs = [0.0, 15.0, 28] # dummy thrsholds to select the energy range inside of L2CaloCutMaps

    for idx, threshold in enumerate(thrs):
      from kepler.emulator.TrigEgammaFastCaloHypoTool import configure
      hypo = configure( self._name + "_" + str(idx) , threshold, pidname)
      if hypo.initialize().isFailure():
        return StatusCode.FAILURE
      self.__hypos.append(hypo)

    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):

    fc = context.getHandler( "HLT__TrigEMClusterContainer" )
    et = fc.et()
    passed = False
    if et < 12*GeV:
      passed = self.__hypos[0].accept(context)
    elif et>=12*GeV and et < 22*GeV:
      passed = self.__hypos[1].accept(context)
    else:
      passed =  self.__hypos[2].accept(context)

    return passed


  #
  # Finalize method
  #
  def finalize(self):
    for hypo in self.__hypos:
      if hypo.finalize().isFailure():
        return StatusCode.FAILURE

    return StatusCode.SUCCESS



#
# Hypo tool
#
class RingerSelectorTool(Algorithm):

  __property = [ "ConfigFile" ]

  #
  # Constructor
  #
  def __init__(self, name, generator ,**kw  ):

    Algorithm.__init__(self, name)

    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)
    self.__generator = generator


  #
  # Inialize the selector
  #
  def initialize(self):

    configPath = self.getProperty( "ConfigFile" )
    self.__tuning, version = load_ringer_models(configPath)
    MSG_INFO( self, "Tuning version: %s" , version )
    MSG_INFO( self, "Loaded %d models for inference." , len(self.__model))
    MSG_INFO( self, "Loaded %d threshold for decision" , len(self.__tuning))

    return StatusCode.SUCCESS



  def accept( self, context):

    accept = Accept(self.name(), [('Pass', False)])
    accept.setDecor( "discriminant",-999 )
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    eventInfo = context.getHandler( "EventInfoContainer" )
    avgmu = eventInfo.avgmu()

    eta = abs(fc.eta())
    if eta>2.5: eta=2.5
    et = fc.et()/GeV # in GeV

    etBinIdx, etaBinIdx = get_bin_indexs( et, eta, self.__tuning['model_etBins'], 
                                          self.__tuning['model_etaBins'], logger=self._logger )
    # If not fount, return false
    if etBinIdx < 0 or etaBinIdx < 0:
      return accept

    # get the model for inference
    model = self.__tuning['models'][etBinIdx][etaBinIdx]

    etBinIdx, etaBinIdx = get_bin_indexs( et, eta, self.__tuning['threshold_etBins'], 
                                          self.__tuning['threshold_etaBins'], logger=self._logger )
    # If not fount, return false
    if etBinIdx < 0 or etaBinIdx < 0:
      return accept

    # get the threshold
    cut = self.__tuning['thresholds'][etBinIdx][etaBinIdx]



    # Until here, we have all to run it!
    data = self.__generator( context )
    # compute the output
    if data:
      output = model.predict( data )[0][0].numpy()
    else:
      return accept

    accept.setDecor("discriminant", output)

    # If the output is below of the cut, reprove it
    if output <= (cut['slope']*avgmu + cut['offset']):
      return accept

    # If arrive until here, so the event was passed by the ringer
    accept.setCutResult( "Pass", True )
    return accept






