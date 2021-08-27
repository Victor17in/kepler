
__all__ = ['Photon', 'EgammaParameters', 'PhotonPid']


from Gaugi import EDM
from Gaugi import StatusCode, EnumStringification
from Gaugi import stdvector_to_list
from kepler.core import Dataframe as DataframeEnum
import math

class PhotonPid(EnumStringification):

      Tight    = 0
      Medium   = 1
      Loose    = 2

class EgammaParameters(EnumStringification):

      # brief uncalibrated energy (sum of cells) in presampler in a 1x1 window in cells in eta X phi
      e011 = 0
      # brief uncalibrated energy (sum of cells) in presampler in a 3x3 window in cells in eta X phi
      e033 = 1
      # brief uncalibrated energy (sum of cells) in strips in a 3x2 window in cells in eta X phi
      e132 = 2
      # brief uncalibrated energy (sum of cells) in strips in a 15x2 window in cells in eta X phi
      e1152 = 3
      # brief transverse energy in the first sampling of the hadronic calorimeters behind the cluster calculated from ehad1
      ethad1 = 4
      # brief ET leakage into hadronic calorimeter with exclusion of energy in CaloSampling::TileGap3
      ethad = 5
      # brief E leakage into 1st sampling of had calo (CaloSampling::HEC0 + CaloSampling::TileBar0 + CaloSampling::TileExt0)
      ehad1 = 6
      # brief E1/E = fraction of energy reconstructed in the first sampling, where E1 is energy in all strips belonging to the
      # cluster and E is the total energy reconstructed in the electromagnetic calorimeter cluster
      f1 = 7
      # brief fraction of energy reconstructed in 3rd sampling
      f3 = 8
      # brief E1(3x1)/E = fraction of the energy reconstructed in the first longitudinal compartment of the electromagnetic
      # calorimeter, where E1(3x1) the energy reconstructed in +/-3 strips in eta, centered around the maximum energy strip and
      # E is the energy reconstructed in the electromagnetic calorimeter
      f1core = 9
      # brief E3(3x3)/E fraction of the energy reconstructed in the third compartment of the electromagnetic calorimeter,
      # where E3(3x3), energy in the back sampling, is the sum of the energy contained in a 3x3 window around the maximum energy cell
      f3core = 10
      # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 3x3 (in cell units eta X phi)
      e233 = 11
      # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 3x5
      e235 = 12
      # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 5x5
      e255 = 13
      # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 3x7
      e237 = 14
      # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 7x7
      e277 = 15
      # brief uncalibrated energy (sum of cells) of the third sampling in a rectangle of size 3x3
      e333 = 16
      # brief uncalibrated energy (sum of cells) of the third sampling in a rectangle of size 3x5
      e335 = 17
      # brief uncalibrated energy (sum of cells) of the third sampling in a rectangle of size 3x7
      e337 = 18
      # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 7x7
      e377 = 19
      # brief shower width using +/-3 strips around the one with the maximal energy deposit:
      # w3 strips = sqrt{sum(Ei)x(i-imax)^2/sum(Ei)}, where i is the number of the strip and imax the strip number of the most energetic one
      weta1 = 20
      # brief the lateral width is calculated with a window of 3x5 cells using the energy weighted  sum over all cells,
      # which depends on the particle impact point inside the cell: weta2 =
      # sqrt(sum Ei x eta^2)/(sum Ei) -((sum Ei x eta)/(sum Ei))^2, where Ei is the energy of the i-th cell
      weta2 = 21
      # brief 2nd max in strips calc by summing 3 strips
      e2ts1 = 22
      # brief energy of the cell corresponding to second energy maximum in the first sampling
      e2tsts1 = 23
      # brief shower shape in the shower core : [E(+/-3)-E(+/-1)]/E(+/-1), where E(+/-n) is
      # the energy in +- n strips around the strip with highest energy
      fracs1 = 24
      # brief same as egammaParameters::weta1 but without corrections  on particle impact point inside the cell
      widths1 = 25
      # brief same as egammaParameters::weta2 but without corrections on particle impact point inside the cell
      widths2 = 26
      # brief relative position in eta within cell in 1st sampling
      poscs1 = 27
      # brief relative position in eta within cell in 2nd sampling
      poscs2= 28
      # brief uncorr asymmetry in 3 strips in the 1st sampling
      asy1 = 29
      # brief difference between shower cell and predicted track in +/- 1 cells
      pos = 30
      # brief Difference between the track and the shower positions:
      # sum_{i=i_m-7}^{i=i_m+7}E_i x (i-i_m) / sum_{i=i_m-7}^{i=i_m+7}E_i,
      # The difference between the track and the shower positions measured
      # in units of distance between the strips, where i_m is the impact cell
      # for the track reconstructed in the inner detector and E_i is the energy
      # reconstructed in the i-th cell in the eta direction for constant phi given by the track parameters
      pos7 = 31
      # brief  barycentre in sampling 1 calculated in 3 strips
      barys1 =32
      # brief shower width is determined in a window detaxdphi = 0,0625x~0,2, corresponding typically to 20 strips in
      # eta : wtot1=sqrt{sum Ei x ( i-imax)^2 / sum Ei}, where i is the strip number and imax the strip number of the first local maximum
      wtots1 = 33
      # brief energy reconstructed in the strip with the minimal value between the first and second maximum
      emins1 = 34
      # brief energy of strip with maximal energy deposit
      emaxs1 = 35
      # brief  1-ratio of energy in 3x3 over 3x7 cells;
      #        E(3x3) = E0(1x1) + E1(3x1) + E2(3x3) + E3(3x3); E(3x7) = E0(3x3) + E1(15x3) + E2(3x7) + E3(3x7)
      r33over37allcalo = 36
      # brief core energy in em calo  E(core) = E0(3x3) + E1(15x2) + E2(5x5) + E3(3x5)
      ecore = 37
      # brief  e237/e277
      Reta = 38
      # brief  e233/e237
      Rphi = 39
      # brief (emaxs1-e2tsts1)/(emaxs1+e2tsts1)
      Eratio = 40
      # brief ethad/et
      Rhad = 41
      # brief ethad1/et
      Rhad1 = 42
      # brief e2tsts1-emins1
      DeltaE =43



class Photon(EDM):

  __eventBranches = {
        'Photon_v1':{'Photon':[ 'ph_hasCalo',
                              'ph_hasTrack',
                              'ph_e',
                              'ph_et',
                              'ph_eta',
                              'ph_phi',
                              'ph_ethad1',
                              'ph_ehad1',
                              'ph_f1',
                              'ph_f3',
                              'ph_f1core',
                              'ph_f3core',
                              'ph_weta2',
                              'ph_wtots1',
                              'ph_fracs1',
                              'ph_Reta',
                              'ph_Rphi',
                              'ph_Eratio',
                              'ph_Rhad',
                              'ph_Rhad1',
                              'ph_deta2',
                              'ph_dphi2',
                              'ph_dphiresc',
                              'ph_deltaPhiRescaled2',
                              'ph_e277',
                              'ph_deltaE',
                              'ph_deltaEta1',
                              'ph_etCone',
                              'ph_ptCone',
                              'ph_calo_e',
                              'ph_calo_et',
                              'ph_calo_eta',
                              'ph_calo_etaBE2',
                              'ph_calo_phi',
                              'ph_nGoodVtx',
                              'ph_ringsE',
                              'ph_nPileupPrimaryVtx',
                              'ph_loose',
                              'ph_medium',
                              'ph_tight',
                              'ph_multiLepton',
                              'mc_isPhoton'],
                    'HLT__Photon':[ 'trig_EF_calo_et',
                                    'trig_EF_calo_eta',
                                    'trig_EF_calo_phi',
                                    'trig_EF_calo_etaBE2',
                                    'trig_EF_calo_e',
                                    'trig_EF_ph_calo_e',
                                    'trig_EF_ph_calo_et',
                                    'trig_EF_ph_calo_eta',
                                    'trig_EF_ph_calo_phi',
                                    'trig_EF_ph_calo_etaBE2',
                                    'trig_EF_ph_hasCalo',
                                    'trig_EF_ph_hasTrack',
                                    'trig_EF_ph_et',
                                    'trig_EF_ph_eta',
                                    'trig_EF_ph_phi',
                                    'trig_EF_ph_e',
                                    'trig_EF_ph_ethad1',
                                    'trig_EF_ph_ehad1',
                                    'trig_EF_ph_f1',
                                    'trig_EF_ph_f3',
                                    'trig_EF_ph_f1core',
                                    'trig_EF_ph_f3core',
                                    'trig_EF_ph_weta1',
                                    'trig_EF_ph_weta2',
                                    'trig_EF_ph_wtots1',
                                    'trig_EF_ph_fracs1',
                                    'trig_EF_ph_Reta',
                                    'trig_EF_ph_Rphi',
                                    'trig_EF_ph_Eratio',
                                    'trig_EF_ph_Rhad',
                                    'trig_EF_ph_Rhad1',
                                    'trig_EF_ph_deta2',
                                    'trig_EF_ph_dphi2',
                                    'trig_EF_ph_e277',
                                    'trig_EF_ph_deltaE',
                                    'trig_EF_ph_dphiresc',
                                    'trig_EF_ph_deltaPhiRescaled2',
                                    'trig_EF_ph_deltaEta1',
                                    'trig_EF_ph_etCone',
                                    'trig_EF_ph_ptCone',
                                    'trig_EF_calo_tight',
                                    'trig_EF_calo_medium',
                                    'trig_EF_calo_loose',
                                    'trig_EF_calo_lhtight',
                                    'trig_EF_calo_lhmedium',
                                    'trig_EF_calo_lhloose',
                                    'trig_EF_calo_lhvloose',
                                    'trig_EF_ph_tight',
                                    'trig_EF_ph_medium',
                                    'trig_EF_ph_loose',
                                    'mc_isPhoton',
                                    ]
                                    }
                  }

  def __init__(self):
    EDM.__init__(self)


  def initialize(self):
    """
      Initalize all branches
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      self.link( self.__eventBranches["Photon_v1"]["HLT__Photon"] if self._is_hlt else self.__eventBranches["Photon_v1"]["Photon"] )
      return StatusCode.SUCCESS
    else:
      self._logger.warning( "Can not initialize the Photon object. Dataframe not available." )
      return StatusCode.FAILURE


  def et(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      eta = self.caloCluster().etaBE2()
      return (self.caloCluster().energy()/math.cosh(eta))
    else:
      self._logger.warning("Impossible to retrieve the value of Et.")
      return -999

  def eta(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_eta[self.getPos()]
      else:
        return self._event.ph_eta
    else:
      self._logger.warning("Impossible to retrieve the value of Eta. Unknow dataframe.")
      return -999

  def phi(self):
    """
      Retrieve the Phi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_phi[self.getPos()]
      else:
        return self._event.ph_phi
    else:
      self._logger.warning("Impossible to retrieve the value of Phi. Unknow dataframe.")
      return -999

  def reta(self):
    """
      Retrieve the Reta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_Reta[self.getPos()]
      else:
        return self._event.ph_Reta
    else:
      self._logger.warning("Impossible to retrieve the value of Reta. Unknow dataframe")
      return -999

  # shower shape
  def eratio(self):
    """
      Retrieve the eratio information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_Eratio[self.getPos()]
      else:
        return self._event.ph_Eratio
    else:
      self._logger.warning("Impossible to retrieve the value of eratio. Unknow dataframe")
      return -999


  # shower shape
  def weta1(self):
    """
      Retrieve the weta1 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_weta1[self.getPos()]
      else:
        return self._event.ph_weta1
    else:
      self._logger.warning("Impossible to retrieve the value of weta1. Unknow dataframe")
      return -999

  # shower shape
  def weta2(self):
    """
      Retrieve the weta2 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_weta2[self.getPos()]
      else:
        return self._event.ph_weta2
    else:
      self._logger.warning("Impossible to retrieve the value of weta2. Unknow dataframe")
      return -999



  # shower shape
  def rhad(self):
    """
      Retrieve the rhad information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_Rhad[self.getPos()]
      else:
        return self._event.ph_Rhad
    else:
      self._logger.warning("Impossible to retrieve the value of rhad. Unknow dataframe")
      return -999

  # shower shape
  def rhad1(self):
    """
      Retrieve the rhad1 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_Rhad1[self.getPos()]
      else:
        return self._event.ph_Rhad1
    else:
      self._logger.warning("Impossible to retrieve the value of rhad1. Unknow dataframe")
      return -999



  # shower shape
  def rphi(self):
    """
      Retrieve the rphi information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_Rphi[self.getPos()]
      else:
        return self._event.ph_Rphi
    else:
      self._logger.warning("Impossible to retrieve the value of rphi. Unknow dataframe")
      return -999

  # shower shape
  def f1(self):
    """
      Retrieve the f1 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_f1[self.getPos()]
      else:
        return self._event.ph_f1
    else:
      self._logger.warning("Impossible to retrieve the value of f1. Unknow dataframe")
      return -999

  # shower shape
  def f3(self):
    """
      Retrieve the f3 information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_f3[self.getPos()]
      else:
        return self._event.ph_f3
    else:
      self._logger.warning("Impossible to retrieve the value of f3. Unknow dataframe")
      return -999

  # shower shape
  def wtots1(self):
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_wtots1[self.getPos()]
      else:
        return self._event.ph_wtots1
    else:
      self._logger.warning("Impossible to retrieve the value of wstot. Unknow dataframe")
      return -999

  # shower shape
  def e277(self):
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_e277[self.getPos()]
      else:
        return self._event.ph_e277
    else:
      self._logger.warning("Impossible to retrieve the value of e277. Unknow dataframe")
      return -999

  # shower shape
  def deltaE(self):
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self._event.trig_EF_ph_deltaE[self.getPos()]
      else:
        return self._event.ph_deltaE
    else:
      self._logger.warning("Impossible to retrieve the value of deltaE. Unknow dataframe")
      return -999


  def showerShapeValue( self, showerShapeType ):

    # brief (emaxs1-e2tsts1)/(emaxs1+e2tsts1)
    if showerShapeType is EgammaParameters.Eratio:
        return self.eratio()
    # brief  e237/e277
    elif showerShapeType is EgammaParameters.Reta:
        return self.reta()
    # brief  e233/e237
    elif showerShapeType is EgammaParameters.Rphi:
        return self.rphi()
    # brief E1/E = fraction of energy reconstructed in the first sampling, where E1 is energy in all strips belonging to the
    # cluster and E is the total energy reconstructed in the electromagnetic calorimeter cluster
    elif showerShapeType is EgammaParameters.f1:
        return self.f1()
    # brief fraction of energy reconstructed in 3rd sampling
    elif showerShapeType is EgammaParameters.f3:
        return self.f3()
    # brief shower width is determined in a window detaxdphi = 0,0625x~0,2, corresponding typically to 20 strips in
    # eta : wtot1=sqrt{sum Ei x ( i-imax)^2 / sum Ei}, where i is the strip number and imax the strip number of the first local maximum
    elif showerShapeType is EgammaParameters.wtots1:
        return self.wtots1()
    # brief shower width using +/-3 strips around the one with the maximal energy deposit:
    # w3 strips = sqrt{sum(Ei)x(i-imax)^2/sum(Ei)}, where i is the number of the strip and imax the strip number of the most energetic one
    elif showerShapeType is EgammaParameters.weta1:
        return self.weta1()
    # brief shower width using +/-3 strips around the one with the maximal energy deposit:
      # w3 strips = sqrt{sum(Ei)x(i-imax)^2/sum(Ei)}, where i is the number of the strip and imax the strip number of the most energetic one
    elif showerShapeType is EgammaParameters.weta2:
        return self.weta2()
    # brief uncalibrated energy (sum of cells) of the middle sampling in a rectangle of size 7x7
    elif showerShapeType is EgammaParameters.e277:
        return self.e277()
    # brief e2tsts1-emins1
    elif showerShapeType is EgammaParameters.DeltaE:
        return self.deltaE()
    # brief ethad1/et
    elif showerShapeType is EgammaParameters.Rhad1:
        return self.rhad1()
    # brief ethad/et
    elif showerShapeType is EgammaParameters.Rhad:
        return self.rhad()
    else:
        self._logger.warning('Unknow ShowerShape type. %s', EgammaParameters.tostring(showerShapeType))
        return -999



  def getAvgmu(self):
    """
      Retrieve the rphi information from Physval or SkimmedNtuple
    """
    # Retrieve event info to get the pileup information
    eventInfo  = self.retrieve('EventInfoContainer')
    if self._dataframe is DataframeEnum.Photon_v1:
      return eventInfo.avgmu()
    else:
      self._logger.warning("Impossible to retrieve the value of pileup. Unknow dataframe")
      return -999


  def ringsE(self):
    """
      Retrieve the Ringer Rings information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        self._logger.warning("Ringer rings information not available in HLT Photon object.")
        return -999
      else:
        return self._event.ph_ringsE
    else:
      self._logger.warning("Impossible to retrieve the value of ringer rings. Unknow dataframe.")
      return -999


  # Check if this object has rings
  def isGoodRinger(self):
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        self._logger.warning("Ringer rings information not available in HLT Electron object.")
        return False
      else:
        rings = stdvector_to_list(self._event.ph_ringsE)
        return True if len(rings)!=0 else False
    else:
      self._logger.warning("Impossible to retrieve the value of ringer rings. Unknow dataframe.")
      return False


  def size(self):
    """
      Retrieve the electro container size
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      if self._is_hlt:
        return self.event.trig_EF_ph_et.size()
      else:
        return 1
    else:
      self._logger.warning("Impossible to retrieve the electron container size. Unknow dataframe")
      return 0


  def empty(self):
    return False if self.size()>0 else True

  def __iter__(self):
    self.setPos(-1) # force to be -1
    if self.size()>0:
      while (self.getPos()+1) < self.size():
        self.setPos(self.getPos()+1)
        yield self


  def caloCluster(self):
    """
      Retrieve the CaloCluster python object into the Store Event
      For now, this is only available into the PhysVal dataframe.
    """
    if self._dataframe is DataframeEnum.Photon_v1:
      # The electron object is empty
      if self.empty():
        return None
      elif self._is_hlt:
        if self._event.trig_EF_ph_hasCalo[self.getPos()]:
          cluster = self.getContext().getHandler('HLT__CaloClusterContainer')
          cluster.setPos(self.getPos())
          return cluster
        else:
          return None
      else:
        if self._event.ph_hasCalo:
          return self.getContext().getHandler('CaloClusterContainer')
        else:
          return None
    else:
      self._logger.warning("Impossible to retrieve the caloCluster object. Unknow dataframe")
      return None


  def accept( self,  pidname ):

    if self._dataframe is DataframeEnum.Photon_v1:
      # Dictionary to acess the physval dataframe
      if pidname in self.__eventBranches['Photon_v1']['HLT__Photon'] and self._is_hlt:
        # the default selector branches is a vector
        return bool(getattr(self._event, pidname)[self.getPos()]) if getattr(self._event, pidname).size()>0 else False

      elif pidname in self.__eventBranches['Photon_v1']['Photon'] and not self._is_hlt:
        return bool(getattr(self._event, pidname))
      elif pidname in self.decorations():
        return bool(self.getDecor(pidname))
      else:
        return False
    else:
      self._logger.warning("Impossible to retrieve the pidname. Unknow dataframe")

  def isMCPhoton(self):
    if self._dataframe is DataframeEnum.Photon_v1:
        return self._event.mc_isPhoton
    else:
      self._logger.warning("Impossible to retrieve the value of deltaE. Unknow dataframe")
      return False

