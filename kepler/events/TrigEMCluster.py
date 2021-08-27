
__all__ = ['TrigEMCluster', 'CaloSampling']

from Gaugi import EDM
from Gaugi  import StatusCode
from Gaugi import stdvector_to_list
from kepler.core import Dataframe as DataframeEnum
from math import cosh
import numpy as np
import math


class CaloSampling(object):
    # LAr barrel
                PreSamplerB  =  0
                EMB1         =  1
                EMB2         =  2
                EMB3         =  3
          # LAr EM endcap
                PreSamplerE  =  4
                EME1         =  5
                EME2         =  6
                EME3         =  7
                # Hadronic endcap
                HEC0         =  8
                HEC1         =  9
                HEC2         = 10
                HEC3         = 11
                # Tile barrel
                TileBar0     = 12
                TileBar1     = 13
                TileBar2     = 14
                # Tile gap (ITC & scint)
                TileGap1     = 15
                TileGap2     = 16
                TileGap3     = 17
                # Tile extended barrel
                TileExt0     = 18
                TileExt1     = 19
                TileExt2     = 20
                # Forward EM endcap
                FCAL0        = 21
                FCAL1        = 22
                FCAL2        = 23
                # MiniFCAL
                MINIFCAL0    =  24
                MINIFCAL1    =  25
                MINIFCAL2    =  26
                MINIFCAL3    =  27

# FastCalo object is similar to TrigEmCluster in xAOD framework
class TrigEMCluster(EDM):
    # set branches here!
    __eventBranches = {

            'v1': # for photon and electron
            [
                'trig_L2_calo_et',
                'trig_L2_calo_eta',
                'trig_L2_calo_phi',
                'trig_L2_calo_e237',
                'trig_L2_calo_e277',
                'trig_L2_calo_fracs1',
                'trig_L2_calo_weta2',
                'trig_L2_calo_ehad1',
                'trig_L2_calo_wstot',
                'trig_L2_calo_e2tsts1',
                'trig_L2_calo_rings',
                'trig_L2_calo_emaxs1',
                'trig_L2_calo_energySample',
                ],
            }

    def __init__(self):
        self._elCand=2
        EDM.__init__(self)


    def initialize(self):
        """
          Link all branches
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            self.link( self.__eventBranches["v1"] )
            return StatusCode.SUCCESS
        else:
            self._logger.warning( "Can not initialize the FastCalo object. Dataframe not available." )
            return StatusCode.FAILURE


    def ringsE(self):
        """
          Retrieve the L2Calo Ringer Rins information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            rings = stdvector_to_list(self._event.trig_L2_calo_rings)
            return np.array(rings, dtype=np.float32)
        else:
            self._logger.warning("Impossible to retrieve the value of L2Calo Ringer Rings. Unknow dataframe")
            return None


    # Check if this object has rings
    def isGoodRinger(self):
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            rings = stdvector_to_list(self._event.trig_L2_calo_rings)
            return True if len(rings)!=0 else False
        else:
            self._logger.warning("Impossible to retrieve the value of ringer rings. Unknow dataframe.")
            return False

    def et(self):
        """
          Retrieve the et information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_et
        else:
            self._logger.warning("Impossible to retrieve the value of et. Unknow dataframe")
            return -999

    def eta(self):
        """
          Retrieve the eta information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_eta
        else:
            self._logger.warning("Impossible to retrieve the value of eta. Unknow dataframe")
            return -999

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_phi
        else:
            self._logger.warning("Impossible to retrieve the value of phi. Unknow dataframe")
            return -999

    def reta(self):
        return self.e237() / float(self.e277())

    def eratio(self):
        eratio = (self.emaxs1() - self.e2tsts1())
        eratio /= (self.emaxs1() + self.e2tsts1())
        return eratio



    def e237(self):
        """
        Retrieve the e237 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_e237
        else:
            self._logger.warning("Impossible to retrieve the value of e237. Unknow dataframe")
            return -999

    def e277(self):
        """
        Retrieve the e277 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_e277
        else:
            self._logger.warning("Impossible to retrieve the value of e277. Unknow dataframe")
            return -999

    def fracs1(self):
        """
          Retrieve the fracs1 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_fracs1
        else:
            self._logger.warning("Impossible to retrieve the value of fracs1. Unknow dataframe")
            return -999

    def emaxs1(self):
        """
          Retrieve the emaxs1 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_emaxs1
        else:
            self._logger.warning("Impossible to retrieve the value of emaxs1. Unknow dataframe")
            return -999

    def weta2(self):
        """
          Retrieve the weta2 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_weta2
        else:
            self._logger.warning("Impossible to retrieve the value of weta2. Unknow dataframe")
            return -999


    def wstot(self):
        """
          Retrieve the wstot information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_wstot
        else:
            self._logger.warning("Impossible to retrieve the value of wstot. Unknow dataframe")
            return -999

    def ehad1(self):
        """
          Retrieve the ehad1 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_ehad1
        else:
            self._logger.warning("Impossible to retrieve the value of ehad1. Unknow dataframe")
            return -999

    def e2tsts1(self):
        """
          Retrieve the e2tsts1 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self._event.trig_L2_calo_e2tsts1
        else:
            self._logger.warning("Impossible to retrieve the value of e2tsts1. Unknow dataframe")
            return -999


    def f1(self):
        """
        Retrieve the f1 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            if ( math.fabs(self.energy()) > 0.00001) :
                F1 = (self.energy(CaloSampling.EMB1)+self.energy(CaloSampling.EME1))/float(self.energy())
                return F1
            else:
                return -1
        else:
            self._logger.warning("Impossible to retrieve the value of f1. Unknow dataframe")
            return -999


    def f3(self):
        """
        Retrieve the f3 information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            # extract F3 (backenergy i EM calorimeter
            e0 = self.energy(CaloSampling.PreSamplerB)  + self.energy(CaloSampling.PreSamplerE)
            e1 = self.energy(CaloSampling.EMB1) 				+ self.energy(CaloSampling.EME1)
            e2 = self.energy(CaloSampling.EMB2) 				+ self.energy(CaloSampling.EME2)
            e3 = self.energy(CaloSampling.EMB3) 				+ self.energy(CaloSampling.EME3)
            eallsamples = float(e0+e1+e2+e3)
            F3= e3/eallsamples if math.fabs(eallsamples)>0. else 0.
            return F3
        else:
            self._logger.warning("Impossible to retrieve the value of f3. Unknow dataframe")
            return -999

    def emTauRoI(self):
        """
          Retrieve the EmTauRoI python object into the Store Event
          For now, this is only available into the PhysVal dataframe.
        """
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return self.getContext().getHandler('HLT__EmTauRoIContainer')
        else:
            self._logger.warning("Impossible to retrieve the EmTauRoI object. Unknow dataframe")
            return None


    def energy( self, idx=None ):
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            if idx:
                return self._event.trig_L2_calo_energySample[idx]
            else:
                return sum(stdvector_to_list(self._event.trig_L2_calo_energySample))
        else:
            self._logger.warning("Impossible to retrieve the value of e2tsts1. Unknow dataframe")
            return -999

    def getAvgmu(self):
        # Retrieve event info to get the pileup information
        eventInfo  = self.getContext().getHandler('EventInfoContainer')
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            return eventInfo.avgmu()
        else:
            self._logger.warning("Impossible to retrieve the value of pileup. Unknow dataframe")
            return -999

    def accept( self,  pidname ):
        if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
            # Dictionary to acess the physval dataframe
            if pidname in self.__eventBranches['v1']:
                # the default selector branches is a vector
                return bool(getattr(self._event, pidname)[self.getPos()])
            elif pidname in self.decorations():
                return bool(self.getDecor(pidname))
            else:
                return False
        else:
            self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")



