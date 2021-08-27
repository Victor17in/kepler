
__all__ = ["TDT", "DecisionCore", "AcceptType"]




from Gaugi import EDM
from kepler.core import Dataframe as DataframeEnum
from Gaugi  import StatusCode, EnumStringification
from Gaugi import stdvector_to_list
from Gaugi.messenger.macros import *
import ROOT


class AcceptType(EnumStringification):

    L1Calo = 0
    L2Calo = 1
    L2     = 2
    EFCalo = 3
    HLT    = 4


class DecisionCore(EnumStringification):
    # Athena navigation core
    TriggerDecisionTool = 0
    # Athena e/g emulation tool
    TrigEgammaEmulationTool = 1





class TDT(EDM):
    # define all skimmed branches here.
    __eventBranches = {
            "Electron_v1":[
                'trig_tdt_L1_calo_accept',
                'trig_tdt_L2_calo_accept',
                'trig_tdt_L2_el_accept',
                'trig_tdt_EF_calo_accept',
                'trig_tdt_EF_el_accept',
                'trig_tdt_emu_L1_calo_accept',
                'trig_tdt_emu_L2_calo_accept',
                'trig_tdt_emu_L2_el_accept',
                'trig_tdt_emu_EF_calo_accept',
                'trig_tdt_emu_EF_el_accept',
                ],

            "Photon_v1":[
                'trig_tdt_L1_calo_accept',
                'trig_tdt_L2_calo_accept',
                'trig_tdt_L2_ph_accept',
                'trig_tdt_EF_calo_accept',
                'trig_tdt_EF_ph_accept',
                'trig_tdt_emu_L1_calo_accept',
                'trig_tdt_emu_L2_calo_accept',
                'trig_tdt_emu_L2_ph_accept',
                'trig_tdt_emu_EF_calo_accept',
                'trig_tdt_emu_EF_ph_accept',
                ],
            }

    def __init__(self):
        EDM.__init__(self)
        # force this class to hold some extra params to read the external information
        # into a root file. This is call by metadata information. Usually, this metadata
        # is stored into the same basepath as the main ttree (event).
        self._useMetadataParams = True
        # the name of the ttree metadata where is stored the information
        # do not change is name.
        self._metadataName = 'tdt'
        # decision core (default)
        self._core = DecisionCore.TriggerDecisionTool


    def core(self, core):
        if core is (DecisionCore.TriggerDecisionTool) or (DecisionCore.TrigEgammaEmulationTool):
            self._core = core
        else:
            MSG_ERROR( self, 'DecisionCore type unknow')


    def initialize(self):


        if self._dataframe is DataframeEnum.Electron_v1:
            branches = self.__eventBranches["Electron_v1"]
        elif self._dataframe is DataframeEnum.Photon_v1:
            branches = self.__eventBranches["Photon_v1"]
        else:
            MSG_WARNING( self, 'Not possible to initialize this metadata using this dataframe. skip!')
            return StatusCode.SUCCESS


        inputFile = self._metadataParams['file']
        # Check if file exists
        f  = ROOT.TFile.Open(inputFile, 'read')
        if not f or f.IsZombie():
            MSG_WARNING( self, 'Couldn''t open file: %s', inputFile)
            return StatusCode.FAILURE

        # Inform user whether TTree exists, and which options are available:
        MSG_DEBUG( self, "Adding file: %s", inputFile)
        treePath = self._metadataParams['basepath'] + '/' + self._metadataName
        obj = f.Get(treePath)
        if not obj:
            MSG_WARNING( self, "Couldn't retrieve TTree (%s)!", treePath)
            MSG_INFO( self, "File available info:")
            f.ReadAll()
            f.ReadKeys()
            f.ls()
            return StatusCode.FAILURE
        elif not isinstance(obj, ROOT.TTree):
            MSG_FATAL( self, "%s is not an instance of TTree!", treePath, ValueError)
        try:
            obj.GetEntry(0)
            self._triggerList = stdvector_to_list(obj.trig_tdt_triggerList)
            for trigItem in self._triggerList:
                MSG_INFO( self, "Metadata trigger: %s", trigItem)
        except:
            MSG_ERROR( self, "Can not extract the trigger list from the metadata file.")
            return StatusCode.FAILURE

        try:
            self.link( branches )
            return StatusCode.SUCCESS
        except:
            MSG_WARNING( self, "Impossible to create the TDTMetaData Container")
            return StatusCode.FAILURE


    def isPassed(self, trigItem):
        return self.ancestorPassed(trigitem,AcceptType.HLT, ignoreDeactivateRois=True)

    def isActive(self, trigItem):
        if trigItem in self._triggerList:
            #for idx , t in enumerate(self._triggerList):
            #  print idx,' = ',t,' = ',self._event.trig_tdt_EF_calo_accept[idx], '---> bool? ', bool(self._event.trig_tdt_EF_calo_accept[idx])
            idx = self._triggerList.index(trigItem)
            isGood = (self._event.trig_tdt_L1_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L1_calo_accept[idx])
            return False if isGood<0 else True
        else:
            return False


    def getTriggerList(self):
      return self._triggerList


    def ancestorPassed( self, trigItem, acceptType ):
        """
        Method to retireve the bool accept for a trigger. To use this:
        l2caloPassed = tdt.ancestorPassed("HLT_e28_lhtight_nod0_ivarloose", AcceptType.L2Calo)
        """
        if trigItem in self._triggerList:
            # Has TE match with the offline electron/photon object
          idx = self._triggerList.index(trigItem)
          isGood = (self._event.trig_tdt_L1_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L1_calo_accept[idx])
          if isGood<0:
              return False
          if   acceptType is AcceptType.L1Calo:
              return bool(self._event.trig_tdt_L1_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L1_calo_accept[idx])
          elif acceptType is AcceptType.L2Calo:
              return bool(self._event.trig_tdt_L2_calo_accept[idx]if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L2_calo_accept[idx])
          elif acceptType is AcceptType.L2:
              if self._dataframe is DataframeEnum.Electron_v1:
                return bool(self._event.trig_tdt_L2_el_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L2_el_accept[idx])
              elif self._dataframe is DataframeEnum.Photon_v1:
                return bool(self._event.trig_tdt_L2_ph_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_L2_ph_accept[idx])
          elif acceptType is AcceptType.EFCalo:
              ef = bool(self._event.trig_tdt_EF_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_calo_accept[idx])
              return bool(self._event.trig_tdt_EF_calo_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_calo_accept[idx])
          elif acceptType is AcceptType.HLT:
              if self._dataframe is DataframeEnum.Electron_v1:
                return bool(self._event.trig_tdt_EF_el_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_el_accept[idx])
              if self._dataframe is DataframeEnum.Photon_v1:
                return bool(self._event.trig_tdt_EF_ph_accept[idx] if self._core is DecisionCore.TriggerDecisionTool else self._event.trig_tdt_emu_EF_ph_accept[idx])

          else:
              print(trigItem)
              MSG_ERROR( self, 'Trigger type not suppported.')
        else:
            MSG_WARNING( self, 'Trigger %s not storage in TDT metadata.',trigItem)





