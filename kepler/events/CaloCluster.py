
__all__ = ["CaloCluster"]


from Gaugi import EDM
from Gaugi import StatusCode
from kepler.core import Dataframe as DataframeEnum


class CaloCluster(EDM):

  # define all skimmed branches here.
  __eventBranches = {
          "Electron_v1"    : {
                  'CaloCluster':[
                              'el_calo_et',
                              'el_calo_eta',
                              'el_calo_phi',
                              'el_calo_etaBE2',
                              'el_calo_e',
                            ],
                   'HLT__CaloCluster':[
                              'trig_EF_el_calo_e',
                              'trig_EF_el_calo_et',
                              'trig_EF_el_calo_eta',
                              'trig_EF_el_calo_phi',
                              'trig_EF_el_calo_etaBE2',
                              'trig_EF_calo_loose',
                              'trig_EF_calo_medium',
                              'trig_EF_calo_tight',
                              'trig_EF_calo_lhvloose',
                              'trig_EF_calo_lhloose',
                              'trig_EF_calo_lhmedium',
                              'trig_EF_calo_lhtight',
                              ]
                            },

          "Photon_v1"      : {
                  'CaloCluster':[
                              'ph_calo_et',
                              'ph_calo_eta',
                              'ph_calo_phi',
                              'ph_calo_etaBE2',
                              'ph_calo_e',
                              ],
                  'HLT__CaloCluster':[
                              'trig_EF_ph_calo_e',
                              'trig_EF_ph_calo_et',
                              'trig_EF_ph_calo_eta',
                              'trig_EF_ph_calo_phi',
                              'trig_EF_ph_calo_etaBE2',
                              'trig_EF_calo_loose',
                              'trig_EF_calo_medium',
                              'trig_EF_calo_tight',
                              'trig_EF_calo_lhvloose',
                              'trig_EF_calo_lhloose',
                              'trig_EF_calo_lhmedium',
                              'trig_EF_calo_lhtight',
                              ]
                              }
                    }



  def __init__(self):
    EDM.__init__(self)


  def initialize(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      self.link( self.__eventBranches["Electron_v1"]['HLT__CaloCluster'] if self._is_hlt else self.__eventBranches["Electron_v1"]["CaloCluster"] )
    elif self._dataframe is DataframeEnum.Photon_v1:
      self.link( self.__eventBranches["Photon_v1"]['HLT__CaloCluster'] if self._is_hlt else self.__eventBranches["Photon_v1"]["CaloCluster"] )
    else:
      self._logger.warning( "CaloCluster object can''t retrieved" )
      return StatusCode.FAILURE

    return StatusCode.SUCCESS


  def et(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_et[self.getPos()]
      else:
        return self._event.el_calo_et
    elif self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_calo_et[self.getPos()]
      else:
        return self._event.ph_calo_et
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Et.")
      return -999


  def eta(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_eta[self.getPos()]
      else:
        return self._event.el_calo_eta
    elif self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_calo_eta[self.getPos()]
      else:
        return self._event.ph_calo_eta
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Eta. Unknow dataframe.")
      return -999


  def phi(self):
    """
      Retrieve the Phi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_phi[self.getPos()]
      else:
        return self._event.el_calo_phi
    elif self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_calo_phi[self.getPos()]
      else:
        return self._event.ph_calo_phi
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Phi. Unknow dataframe.")
      return -999

  def etaBE2(self):
    """
      Retrieve the EtaBE2 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_etaBE2[self.getPos()]
      else:
        return self._event.el_calo_etaBE2
    elif self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_calo_etaBE2[self.getPos()]
      else:
        return self._event.ph_calo_etaBE2
    else:
      self._logger.warning("Impossible to retrieve the value of Calo EtaBE2. Unknow dataframe.")
      return -999

  def energy(self):
    """
      Retrieve the E information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_calo_e[self.getPos()]
      else:
        return self._event.el_calo_e
    elif self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_calo_e[self.getPos()]
      else:
        return self._event.ph_calo_e
    else:
      self._logger.warning("Impossible to retrieve the value of Calo Energy. Unknow dataframe.")
      return -999


  def emCluster(self):
    """
      Retrieve the TrigEmCluster (FastCalo) python object into the Store Event
      For now, this is only available into the PhysVal dataframe.
    """
    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      cluster = self.getContext().getHandler('HLT__TrigEMClusterContainer')
      cluster.setPos(self.getPos())
      return cluster
    else:
      self._logger.warning("Impossible to retrieve the FastCalo object. Unknow dataframe")
      return None



  def size(self):
    """
    	Retrieve the TrackParticle container size
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self.event.trig_EF_el_calo_eta.size()
      else:
        return 1
    elif self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self.event.trig_EF_ph_calo_eta.size()
      else:
        return 1
    else:
      self._logger.warning("Impossible to retrieve the TrackParticle container size. Unknow dataframe")

  def empty(self):
    return False if self.size()>0 else True



