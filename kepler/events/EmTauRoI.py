
__all__ = ['EmTauRoI']

from Gaugi import EDM
from Gaugi import StatusCode
from Gaugi import stdvector_to_list
from kepler.core import Dataframe as DataframeEnum


class EmTauRoI(EDM):

    __eventBranches = [
                'trig_L1_eta',
                'trig_L1_phi',
                'trig_L1_emClus',
                'trig_L1_tauClus',
                'trig_L1_emIsol',
                'trig_L1_hadIsol',
                ]


    def __init__(self):
        EDM.__init__(self)


    def initialize(self):
      """
        Link all branches
      """
      if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
          self.link(self.__eventBranches)
          return StatusCode.SUCCESS
      else:
          self._logger.warning( "CaloCluster object can''t retrieved" )
          return StatusCode.FAILURE



    def emClus(self):
        """
          Retrieve the L1 EmClus information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L1_emClus
        else:
            self._logger.warning("Impossible to retrieve the value of L1 EmClus. Unknow dataframe")

    def tauClus(self):
        """
          Retrieve the L1 tauClus information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L1_tauClus
        else:
            self._logger.warning("Impossible to retrieve the value of L1 tauClus. Unknow dataframe")

    def emIsol(self):
        """
          Retrieve the L1 emIsol information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L1_emIsol
        else:
            self._logger.warning("Impossible to retrieve the value of L1 EmIsol. Unknow dataframe")

    def hadCore(self):
        """
          Retrieve the L1 hadIsol information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L1_hadIsol
        else:
            self._logger.warning("Impossible to retrieve the value of L1 hadIsol. Unknow dataframe")

    def eta(self):
        """
          Retrieve the eta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L1_eta
        else:
            self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L1_phi
        else:
            self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")





