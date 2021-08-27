
__all__ = ['TrigElectron']

from Gaugi import EDM
from Gaugi  import StatusCode
from Gaugi import stdvector_to_list
import numpy as np
from kepler.core import Dataframe as DataframeEnum


class TrigElectron(EDM):

    __eventBranches = {
                      'Electron_v1':
                    [
                      'trig_L2_el_trackAlgID',
                      'trig_L2_el_pt',
                      'trig_L2_el_caloEta',
                      'trig_L2_el_eta',
                      'trig_L2_el_phi',
                      'trig_L2_el_charge',
                      'trig_L2_el_nTRTHits',
                      'trig_L2_el_nTRTHiThresholdHits',
                      'trig_L2_el_etOverPt',
                      'trig_L2_el_trkClusDeta',
                      'trig_L2_el_trkClusDphi',

                    ]
                }

    def __init__(self):
        EDM.__init__(self)

    def initialize(self):
        """
          Initialize all branches
        """
        if self._dataframe is DataframeEnum.Electron_v1:
           self.link( self.__eventBranches["Electron_v1"] )
           return StatusCode.SUCCESS
        else:
           self._logger.warning( "Can not initialize the FastElectron object. Dataframe not available." )
           return StatusCode.FAILURE



    def pt(self):
        """
          Retrieve the pt information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_pt[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of pt. Unknow dataframe")


    def eta(self):
        """
        Retrieve the eta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_eta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_phi[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")

    def charge(self):
        """
         Retrieve the charge information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_charge[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of charge. Unknow dataframe")

    def caloEta(self):
        """
        Retrieve the caloEta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_caloEta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of caloEta. Unknow dataframe")

    def numberOfTRTHits(self):
        """
        Retrieve the number of TRT hits information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_nTRTHits[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of nTRTHits. Unknow dataframe")

    def numberOfTRTHiThresholdHits(self):
        """
        Retrieve the number of TRT high thresholdhits information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_nTRTHiThresholdHits[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of nTRTHiThrehsoldHits. Unknow dataframe")


    def etOverPt(self):
        """
        Retrieve the et/pt information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_etOverPt[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of et/pt. Unknow dataframe")

    def trkClusDeta(self):
        """
        Retrieve the trkClusDeta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_trkClusDeta[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of trkClusDeta. Unknow dataframe")

    def trkClusDphi(self):
        """
        Retrieve the trkClusDphi information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.trig_L2_el_trkClusDphi[self.getPos()]
        else:
            self._logger.warning("Impossible to retrieve the value of trkClusDphi. Unknow dataframe")


    def size(self):
        return self._event.trig_L2_el_pt.size()



    def setToBeClosestThanCluster( self ):
      idx = 0; minDeltaR = 999
      for trk in self:
        dR = self.deltaR( 0.0, 0.0, trk.trkClusDeta(), trk.trkClusDphi() )
        if dR < minDeltaR:
          minDeltaR = dR
          idx = self.getPos()
      self.setPos(idx)


    def deltaR( self, eta1, phi1, eta2, phi2 ):
      deta = abs( eta1 - eta2 )
      dphi = abs( phi1 - phi2 ) if abs(phi1 - phi2) < np.pi else (2*np.pi-abs(phi1-phi2))
      return np.sqrt( deta*deta + dphi*dphi )







