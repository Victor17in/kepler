
__all__ = ["TrackCaloMatchType","SummaryType","TrackParticle"]


from Gaugi import EDM
from kepler.core import Dataframe as DataframeEnum
from Gaugi  import StatusCode, EnumStringification
from Gaugi import stdvector_to_list



class TrackCaloMatchType(EnumStringification):

  # brief difference between the cluster eta (presampler) and
  # the eta of the track extrapolated to the presampler
  deltaEta0 = 0
  # brief difference between the cluster eta (first sampling) and the eta of the track extrapolated to the
  # first sampling: |eta_stripscluster -eta_ID|, where eta_stripscluster is computed
  # in the first sampling of the electromagnetic calorimeter, where the granularity is very fine, and eta_ID is the pseudo-rapidity
  # of the track extrapolated to the calorimeter
  deltaEta1 = 1,
  # brief difference between the cluster eta (second sampling) and the eta of the track extrapolated to the second sampling
  deltaEta2 = 2,
  # brief difference between the cluster eta (3rd sampling) and
  # the eta of the track extrapolated to the 3rd sampling
  deltaPhi0 = 4,
  # brief difference between the cluster eta (1st sampling) and
  # the eta of the track extrapolated to the 1st sampling (strips)
  deltaPhi1 = 5,
  # brief difference between the cluster phi (second sampling) and the phi of the track
  # extrapolated to the second sampling : |phi_middlecluster -phi_ID|, where phi_middlecluster
  # is computed in the second compartment of the electromagnetic calorimeter and phi_ID is the
  # azimuth of the track extrapolated to the calorimeter
  deltaPhi2 = 6,
  # brief difference between the cluster phi (presampler) and
  # the eta of the track extrapolated to the presampler  from the perigee with a rescaled
  # momentum.
  deltaPhiRescaled0 = 9,
  # brief difference between the cluster eta (1st sampling) and
  # the eta of the track extrapolated to the 1st sampling (strips) from the perigee with a rescaled
  # momentum.
  deltaPhiRescaled1 = 10,
  # brief difference between the cluster phi (second sampling) and the phi of the track
  # extrapolated to the second sampling from the perigee with a rescaled
  # momentum.
  deltaPhiRescaled2 = 11,



# Enumerates the different types of information stored in Summary.
# Please note that the values have specific types - i.e. some are float # whilst most are uint8_t.
# When adding a new transient information type # please make sure to increase numberOfTrackSummaryTypes.*/
class SummaryType(EnumStringification):

  numberOfBLayerHits                            =  0 #  //!< these are the hits in the first pixel layer, i.e. b-layer [unit8_t].
  numberOfBLayerOutliers                        =  1 #  //!< number of blayer outliers [unit8_t].
  numberOfPixelHits                             =  2 #  //!< these are the pixel hits, including the b-layer [unit8_t].
  numberOfPixelOutliers                         =  3 #  //!< these are the pixel outliers, including the b-layer [unit8_t].
  numberOfPixelDeadSensors                      =  4 #  //!< number of dead pixel sensors crossed [unit8_t].
  numberOfSCTHits                               =  5 #  //!< number of hits in SCT [unit8_t].
  numberOfSCTOutliers                           =  6 #  //!< number of SCT outliers [unit8_t].
  numberOfSCTDeadSensors                        =  7 #  //!< number of dead SCT sensors crossed [unit8_t].
  numberOfTRTHits                               =  8 #  //!< number of TRT hits [unit8_t].
  numberOfTRTOutliers                           =  9 #  //!< number of TRT outliers [unit8_t].
  numberOfTRTHighThresholdHits                  = 10 #  //!< number of TRT hits which pass the high threshold (only xenon counted) [unit8_t].
  numberOfTRTHighThresholdOutliers              = 11 #  //!< number of TRT high threshold outliers (only xenon counted) [unit8_t].
  numberOfTRTXenonHits                          = 12 #  //!< number of TRT hits on track in straws with xenon [unit8_t].
  expectBLayerHit                               = 13 #  //!< Do we expect a b-layer hit for this track? [unit8_t] (should be [bool])
  expectNextToInnermostPixelLayerHit            = 14 #  //!< Do we expect a 1st-layer hit for this track?
  numberOfNextToInnermostPixelLayerHits         = 15 #  //!< these are the hits in the 1st pixel layer
  numberOfNextToInnermostPixelLayerOutliers     = 16 #  //!< number of 1st pixel layer outliers
  #  --- Inner Detector
  numberOfContribPixelLayers                    = 17 #  //!< number of contributing layers of the pixel detector [unit8_t].
  numberOfBLayerSharedHits                      = 18 #  //!< number of Pixel b-layer hits shared by several tracks [unit8_t].
  numberOfBLayerSplitHits                       = 19 #  //!< number of Pixel b-layer hits split by cluster splitting [unit8_t].
  expectInnermostPixelLayerHit                  = 20 #  //!< Do we expect a 0th-layer hit for this track?
  numberOfInnermostPixelLayerHits               = 21 #  //!< these are the hits in the 0th pixel layer?
  numberOfInnermostPixelLayerOutliers           = 22 #  //!< number of 0th layer outliers
  numberOfInnermostPixelLayerSharedHits         = 23 #  //!< number of Pixel 0th layer hits shared by several tracks.
  numberOfInnermostPixelLayerSplitHits          = 24 #  //!< number of Pixel 0th layer hits split by cluster splitting
  numberOfNextToInnermostPixelLayerSharedHits   = 25 #  //!< number of Pixel 1st layer hits shared by several tracks.
  numberOfNextToInnermostPixelLayerSplitHits    = 26 #  //!< number of Pixel 1st layer hits split by cluster splitting
  numberOfDBMHits                               = 27 # //!< these are the number of DBM hits [unit8_t].
  numberOfPixelHoles                            = 28 #  //!< number of pixel layers on track with absence of hits [unit8_t].
  numberOfPixelSharedHits                       = 29 #  //!< number of Pixel all-layer hits shared by several tracks [unit8_t].
  numberOfPixelSplitHits                        = 30 #  //!< number of Pixel all-layer hits split by cluster splitting [unit8_t].
  numberOfGangedPixels                          = 31 #  //!< number of pixels which have a ganged ambiguity [unit8_t].
  numberOfGangedFlaggedFakes                    = 32 #  //!< number of Ganged Pixels flagged as fakes [unit8_t].
  numberOfPixelSpoiltHits                       = 33 #  //!< number of pixel hits with broad errors (width/sqrt(12)) [unit8_t].
  numberOfSCTHoles                              = 34 #  //!< number of SCT holes [unit8_t].
  numberOfSCTDoubleHoles                        = 35 #  //!< number of Holes in both sides of a SCT module [unit8_t].
  numberOfSCTSharedHits                         = 36 #  //!< number of SCT hits shared by several tracks [unit8_t].
  numberOfSCTSpoiltHits                         = 37 #  //!< number of SCT hits with broad errors (width/sqrt(12)) [unit8_t].
  numberOfTRTHoles                              = 38 #  //!< number of TRT holes [unit8_t].
  numberOfTRTHighThresholdHitsTotal             = 39 #  //!< total number of TRT hits which pass the high threshold  [unit8_t].
  numberOfTRTDeadStraws                         = 40 #  //!< number of dead TRT straws crossed [unit8_t].
  numberOfTRTTubeHits                           = 41 #  //!< number of TRT tube hits [unit8_t].
  numberOfTRTSharedHits                         = 42 #  //!< number of TRT hits used by more than one track
  #  --- Muon Spectrometer
  numberOfPrecisionLayers                       = 43 #   //!< layers with at least 3 hits [unit8_t].
  numberOfPrecisionHoleLayers                   = 44 #   //!< layers with holes AND no hits [unit8_t].
  numberOfPhiLayers                             = 45 #   //!< layers with a trigger phi hit [unit8_t].
  numberOfPhiHoleLayers                         = 46 #  //!< layers with trigger phi holes but no hits [unit8_t].
  numberOfTriggerEtaLayers                      = 47 #  //!< layers with trigger eta hits [unit8_t].
  numberOfTriggerEtaHoleLayers                  = 48 #  //!< layers with trigger eta holes but no hits [unit8_t].
  numberOfGoodPrecisionLayers                   = 49 #  //!< layers with at least 3 hits that are not deweighted [uint8_t]
  numberOfOutliersOnTrack                       = 50 #  //!< number of measurements flaged as outliers in TSOS [unit8_t].
  standardDeviationOfChi2OS                     = 51 #  //!< 100 times the standard deviation of the chi2 from the surfaces [unit8_t].
  eProbabilityComb                              = 52 #  //!< Electron probability from combining the below probabilities [float].
  eProbabilityHT                                = 53 #  //!< Electron probability from  High Threshold (HT) information [float].
  pixeldEdx                                     = 54 #  //!< the dE/dx estimate, calculated using the pixel clusters [?]



class TrackParticle(EDM):

  # define all skimmed branches here.
  __eventBranches = {

      "Electron_v1": {'TrackParticle':[
                          'el_trk_pt',
                          'el_trk_eta',
                          'el_trk_charge',
                          'el_trk_sigd0',
                          'el_trk_d0',
                          'el_trk_eProbabilityHT',
                          'el_trk_transformed_eProbabilityHT',
                          'el_trk_d0significance',
                          'el_trk_deltaPOverP',
                          'el_trk_qOverP',
                          'el_trk_summaryValues'
                        ],

                        'HLT__TrackParticle':[
                          'trig_EF_el_trk_pt',
                          'trig_EF_el_trk_eta',
                          'trig_EF_el_trk_charge',
                          'trig_EF_el_trk_sigd0',
                          'trig_EF_el_trk_d0',
                          'trig_EF_el_trk_eProbabilityHT',
                          'trig_EF_el_trk_transformed_eProbabilityHT',
                          'trig_EF_el_trk_d0significance',
                          'trig_EF_el_trk_deltaPOverP',
                          'trig_EF_el_trk_qOverP',
                          'trig_EF_el_trk_summaryValues'

                          ]
                          }
                }

  def __init__(self):
    EDM.__init__(self)


  def initialize(self):
    """
      Link all branches
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      branches = self.__eventBranches["Electron_v1"]["HLT__TrackParticle"] if self._is_hlt else self.__eventBranches["Electron_v1"]["TrackParticle"]
      self.link( branches )
      return StatusCode.SUCCESS
    else:
      self._logger.warning( "Can not initialize the TrackParticle object. Dataframe not available." )
      return StatusCode.FAILURE




  def pt(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_pt[self.getPos()]
      else:
        return self._event.el_trk_pt
    else:
      self._logger.warning("Impossible to retrieve the value of Eta. Unknow dataframe.")
      return -999


  def eta(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_eta[self.getPos()]
      else:
        return self._event.el_trk_eta
    else:
      self._logger.warning("Impossible to retrieve the value of Eta. Unknow dataframe.")
      return -999


  def charge(self):
    """
      Retrieve the charge information from Physval or SkimmedNtuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_charge[self.getPos()]
      else:
        return self._event.el_trk_charge
    else:
      self._logger.warning("Impossible to retrieve the value of charge. Unknow dataframe.")
      return -999


  def d0(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_d0[self.getPos()]
      else:
        return self._event.el_trk_d0
    else:
      self._logger.warning("Impossible to retrieve the value of d0. Unknow dataframe")
      return -999


  def d0significance(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_d0significance[self.getPos()]
      else:
        return self._event.el_trk_d0significance
    else:
      self._logger.warning("Impossible to retrieve the value of d0significance. Unknow dataframe")
      return -999


  def sigd0(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_sigd0[self.getPos()]
      else:
        return self._event.el_trk_sigd0
    else:
      self._logger.warning("Impossible to retrieve the value of sigd0. Unknow dataframe")
      return -999




  def eProbabilityHT(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_eProbabilityHT[self.getPos()]
      else:
        return self._event.el_trk_eProbabilityHT
    else:
      self._logger.warning("Impossible to retrieve the value of eProbabilityHT. Unknow dataframe")
      return -999


  def trans_TRT_PID(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_transformed_eProbabilityHT[self.getPos()]
      else:
        return self._event.el_trk_transformed_eProbabilityHT
    else:
      self._logger.warning("Impossible to retrieve the value of TRT_PID. Unknow dataframe")
      return -999


  def DeltaPOverP(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_deltaPOverP[self.getPos()]
      else:
        return self._event.el_trk_deltaPOverP
    else:
      self._logger.warning("Impossible to retrieve the value of eProbabilityHT. Unknow dataframe")
      return -999


  def qOverP(self):

    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self._event.trig_EF_el_trk_qOverP[self.getPos()]
      else:
        return self._event.el_trk_qOverP
    else:
      self._logger.warning("Impossible to retrieve the value of qOverP. Unknow dataframe")
      return -999


  def summaryValue( self, summaryType ):
    """
      Helper method:
        Retrieve the summary track value from the ntuple
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        offset = ( self._event.trig_EF_el_trk_summaryValues.size()/ float(self.size()) ) * self.getPos()
        if offset+summaryType > self._event.trig_EF_el_trk_summaryValues.size():
          self._logger.error('SummaryType outside of range. Can not retrieve %s from the PhysVal', SummaryType.tostring(summaryType))
          return -999
        else:
          return ord(self._event.trig_EF_el_trk_summaryValues.at(int(offset+summaryType)))
      else:
        if summaryType > self._event.el_trk_summaryValues.size():
          self._logger.error('SummaryType outside of range. Can not retrieve %s from the PhysVal', SummaryType.tostring(summaryType))
          return -999
        else:
          return ord(self._event.el_trk_summaryValues.at(summaryType))
    else:
      self._logger.warning("Impossible to retrieve %s value. Unknow dataframe", SummaryType.tostring(summaryType))
      return -999


  def numberOfBLayerHits(self):
    return self.summaryValue( SummaryType.numberOfBLayerHits )

  def numberOfBLayerOutliers(self):
    return self.summaryValue( SummaryType.numberOfBLayerOutliers )

  def numberOfPixelHits(self):
    return self.summaryValue( SummaryType.numberOfPixelHits )

  def numberOfPixOutliers(self):
    return self.summaryValue( SummaryType.numberOfPixOutliers )

  def numberOfSCTHits(self):
    return self.summaryValue( SummaryType.numberOfSCTHits )

  def numberOfSCTOutliers(self):
    return self.summaryValue( SummaryType.numberOfSCTOutliers )

  def numberOfTRTHits(self):
    return self.summaryValue( SummaryType.numberOfTRTHits )

  def numberOfTRTOutliers(self):
    return self.summaryValue(  SummaryType.numberOfTRTOutliers )

  def numberOfTRTHighThresholdHits(self):
    return self.summaryValue( SummaryType.numberOfTRTHighThresholdHits )

  def numberOfTRTHighThresholdOutliers(self):
    return self.summaryValue( SummaryType.numberOfTRTHighThresholdOutliers )

  def numberOfTRTXenonHits(self):
    return self.summaryValue( SummaryType. numberOfTRTXenonHits )

  def expectBLayerHit(self):
    return self.summaryValue( SummaryType.expectBLayerHit )

  def numberOfSiHits(self):
    return -999

  def numberOfSiDeadSensors(self):
    return -999

  def numberOfPixelDeadSensors(self):
    return self.summaryValue( SummaryType.numberOfPixelDeadSensors )

  def numberOfSCTDeadSensors(self):
    return self.summaryValue( SummaryType.numberOfSCTDeadSensors )

  def expectNextToInnermostPixelLayerHit(self):
    return self.summaryValue( SummaryType.expectNextToInnermostPixelLayerHit )

  def numberOfNextToInnermostPixelLayerHits(self):
    return self.summaryValue( SummaryType.numberOfNextToInnermostPixelLayerHits )

  def numberOfNextToInnermostPixelLayerOutliers(self):
    return self.summaryValue( SummaryType.numberOfNextToInnermostPixelLayerOutliers )

  def size(self):
    """
    	Retrieve the TrackParticle container size
    """
    if self._dataframe is DataframeEnum.Electron_v1:
      if self._is_hlt:
        return self.event.trig_EF_el_trk_eta.size()
      else:
        return 1
    else:
      self._logger.warning("Impossible to retrieve the TrackParticle container size. Unknow dataframe")

  def empty(self):
    return False if self.size()>0 else True


