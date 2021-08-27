__all__ = ['Filter', 'EtCutType', 'SelectionType']


from Gaugi import GeV
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import StatusWTD # use this to stop the sequence and skip the event
from Gaugi import EnumStringification
from Gaugi.messenger.macros import *

from kepler.core import Dataframe as DataframeEnum

import collections


#
# Enumeration et cut type
#
class EtCutType(EnumStringification):
  OfflineAbove = -1
  OfflineBelow = -2
  L1CaloAbove  = -3
  L1CaloBelow  = -4
  L2CaloAbove  = -5
  L2CaloBelow  = -6
  EFCaloAbove  = -7
  EFCaloBelow  = -8
  HLTAbove     = -9
  HLTBelow     = -10


#
# Enumeration selection type
#
class SelectionType(EnumStringification):

  # @brief: selection from Data taken events
  SelectionData = 0
  # @brief: selection only Z candidates (Monte Carlo)
  SelectionZ = 1
  # @brief: selection only W candidates (Monte Carlo)
  SelectionW = 2
  # @brief: selection only Fakes candidates
  SelectionFakes = 3
  # @brief: Select only events between a lb range
  SelectionLumiblockRange = 4
  # @brief: Select only events by run number
  SelectionRunNumber = 5
  # @brief: Select only events with online ringer calo rings
  SelectionOnlineWithRings = 6
  # @brief: Select only events with  offline ringer calo rings
  SelectionOfflineWithRings = 7
  # @brief: Select by PID
  SelectionPID = 8
  # @brief: Select events with trig electron container > 0
  SelectionOnlineWithTrigElectrons = 9
  # @brief: Select events by its origin (only for MC data)
  SelectionFromOrigin = 10
  
  SelectionFromType = 11

  SelectionPhoton = 12

  SelectionJet = 13






#
# Event selection
#
class Filter( Algorithm ):

  #
  # Constructor
  #
  def __init__(self, name):

    Algorithm.__init__(self, name)

    # Cut type and values
    self.__cutValues = collections.OrderedDict()


  #
  # Initialize method
  #
  def initialize(self):
    return StatusCode.SUCCESS

  #
  # Set cut value
  #
  def setCutValue(self, cutType, value=None):
    self.__cutValues[cutType] = value


  #
  # Execute method
  #
  def execute(self, context):
    
    if self._dataframe is DataframeEnum.Electron_v1:
      elCont    = context.getHandler( "ElectronContainer" )
    elif self._dataframe is DataframeEnum.Photon_v1:
      elCont    = context.getHandler( "PhotonContainer" )
    else:
      elCont    = context.getHandler( "ElectronContainer" )

    fc        = context.getHandler( "HLT__TrigEMClusterContainer" )
    fc_el     = context.getHandler( "HLT__TrigElectronContainer" )
    mc        = context.getHandler( "MonteCarloContainer")
    eventInfo = context.getHandler( "EventInfoContainer" )

    # Apply all et cut values setted in the dict
    for key, value in self.__cutValues.items():

      MSG_DEBUG( self, 'Apply Selection cut for %s',EtCutType.tostring(key))
      MSG_DEBUG( self, 'Apply Selection cut for %s',SelectionType.tostring(key))
      el=elCont
      if key is EtCutType.OfflineAbove and el.et()/GeV < value:
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Reproved by Et cut value. Et = %1.3f < EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS

      if key is EtCutType.OfflineBelow and el.et()/GeV >= value:
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Reproved by Et cut value. Et = %1.3f >= EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS

      elif key is EtCutType.L2CaloAbove and fc.et()/GeV < value:
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Reproved by Et cut value. Et = %1.3f < EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS

      elif key is EtCutType.L2CaloBelow and fc.et()/GeV >= value:
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Reproved by Et cut > value. Et = %1.3f >= EtCut = %1.3f',el.et()/GeV,value)
        return StatusCode.SUCCESS


      elif key is EtCutType.HLTAbove or key is EtCutType.HLTBelow:
        passed = False
        for eg in elCont:
          # Et cut value for each electron object
          if key is EtCutType.HLTAbove and eg.et()/GeV >= value:  passed=True; break
          if key is EtCutType.HLTBelow and eg.et()/GeV < value:  passed=True; break

        # Loop over electrons from HLT
        if not passed:
          self.wtd = StatusWTD.ENABLE
          MSG_DEBUG( self, 'Reproved by Et cut value. Et = %1.3f and EtCut = %1.3f',el.et()/GeV,value)
          return StatusCode.SUCCESS


      # Is good ringer
      elif key is SelectionType.SelectionOnlineWithRings and not fc.isGoodRinger():
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Event dont contain the online ringer rings values. skip...')
        return StatusCode.SUCCESS
      
      # Is good trig electrons
      elif key is SelectionType.SelectionOnlineWithTrigElectrons and fc_el.size() == 0:
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Event dont contain the online trigger electrons objects. skip...')
        return StatusCode.SUCCESS

      # Is good ringer
      elif key is SelectionType.SelectionOfflineWithRings and not el.isGoodRinger():
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Event dont contain the offline ringer rings values. skip...')
        return StatusCode.SUCCESS

      # Monte Carlo event selection truth cuts
      elif key is SelectionType.SelectionFakes and mc.isMC() and mc.isEfromZ():
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Fakes: is Z! reject')
        return StatusCode.SUCCESS

      # Monte Carlo event selection truth cuts
      elif key is SelectionType.SelectionZ and mc.isMC() and not mc.isEfromZ():
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Z: is not Z! reject')
        return StatusCode.SUCCESS

      elif key is SelectionType.SelectionRunNumber and (int(eventInfo.RunNumber()) != int(value)):
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Reject event by RunNumber. skip...')
        return StatusCode.SUCCESS

      elif key is SelectionType.SelectionPhoton and  not mc.isTruthPhotonFromAny():
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Photon: is not Photon! reject')
        return StatusCode.SUCCESS

      elif key is SelectionType.SelectionJet and not mc.isTruthJetFromAny():
        self.wtd = StatusWTD.ENABLE
        MSG_DEBUG( self, 'Jet: is not Jet! reject')
        return StatusCode.SUCCESS

      # Offline recostruction cut by PID selectors
      elif key is SelectionType.SelectionPID:
        pidname = value
        MSG_DEBUG( self, 'Apply PID selection...')
        # is this a veto criteria?
        isVeto = True if '!' in pidname else False
        # remove the not (!) charactere in the pidname
        pidname = pidname.replace('!','') if isVeto else pidname
        # Get the bool accept from some pidname branch or decoration inside of the electron object

        passed=False
        for eg in elCont:
          passed = eg.accept(pidname)
          if passed: break

        # Apply veto event selection
        MSG_DEBUG( self, 'PID (%s) is %d',pidname,passed)
        if isVeto and passed:
          self.wtd = StatusWTD.ENABLE
          return StatusCode.SUCCESS
        if not isVeto and not passed:
          self.wtd = StatusWTD.ENABLE
          return StatusCode.SUCCESS
      
      elif key is SelectionType.SelectionFromOrigin:
        origin = mc.origin()
        if origin != value:
          self.wtd = StatusWTD.ENABLE
          MSG_DEBUG( self, 'Reproved by Origin value. Origin = %1.3f != OriginCut = %1.3f',mc.origin(),value)
          return StatusCode.SUCCESS
      
      elif key is SelectionType.SelectionFromType:
        type = mc.type()
        if type != value:
          self.wtd = StatusWTD.ENABLE
          MSG_DEBUG( self, 'Reproved by Type value. Type = %1.3f != TypeCut = %1.3f',mc.type(),value)
          return StatusCode.SUCCESS
      else:
        MSG_DEBUG( self, 'Selection cut (%s) approved.',key)


    self.wtd = StatusWTD.DISABLE
    return StatusCode.SUCCESS


  #
  # Finalize method
  #
  def finalize(self):
    return StatusCode.SUCCESS






