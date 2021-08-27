
__all__ = ['MonteCarlo']

from Gaugi import EDM
from Gaugi import StatusCode
from kepler.core import Dataframe as DataframeEnum


class MonteCarlo(EDM):

  __eventBranches = {
                    'v1':[ # For electron and photon
                      'mc_hasMC',
                      'mc_isTruthElectronAny',
                      'mc_isTruthElectronFromZ',
                      'mc_isTruthElectronFromW',
                      'mc_isTruthElectronFromJpsi',
                      'mc_isTruthJetFromAny',
                      'mc_isTruthPhotonFromAny',
                      'mc_type',
                      'mc_origin',
                      ],
                    }


  def __init__(self):
    EDM.__init__(self)



  def initialize(self):
    """
    Initialize all branches
    """
    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      self.link( self.__eventBranches["v1"] )
      return StatusCode.SUCCESS
    else:
      self._logger.warning( "Can not initialize the MonteCarlo object. Dataframe not available." )
      return StatusCode.FAILURE




  def isTruthElectronFromZ(self):

    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromZ
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromW(self):

    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromW
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromJpsi(self):

    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromJpsi
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthElectronFromAny(self):

    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthElectronFromAny
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthJetFromAny(self):

    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthJetFromAny
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def isTruthPhotonFromAny(self):

    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_isTruthPhotonFromAny
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")
  
  def isMC(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return bool(self._event.mc_hasMC)
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")

  def type(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_type
    else:
      self._logger.warning("Impossible to retrieve the type value.")

  def origin(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1 or DataframeEnum.Photon_v1:
      return self._event.mc_origin
    else:
      self._logger.warning("Impossible to retrieve the type value.")



