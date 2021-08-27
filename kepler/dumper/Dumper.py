
__all__ = ["Collector"]


from kepler.core import Dataframe as DataframeEnum
from Gaugi import StatusCode, progressbar
from Gaugi import csvStr2List, expandFolders, save, load
from Gaugi.messenger.macros import *
from Gaugi.messenger  import Logger
from Gaugi.constants import GeV
from Gaugi import EnumStringification
from Gaugi import Algorithm
import numpy as np


class Dumper( Algorithm ):

  def __init__(self, name, **kw):
    
    Algorithm.__init__(self, name)
    self._event = {}
    self._event_label = []
    self._save_these_bins = list()
    self._extra_features = list()
    
    self.declareProperty( "OutputFile", 'sample.pic', "The output file name"       )


    for key, value in kw.items():
      self.setProperty(key, value)


  def setEtBinningValues( self, etbins ):
    self._etbins = etbins


  def setEtaBinningValues( self, etabins ):
    self._etabins = etabins


  def AddFeature( self, key ):
    self._extra_features.append( key )


  def initialize(self):
    Algorithm.initialize(self)
    for etBinIdx in range(len(self._etbins)-1):
      for etaBinIdx in range(len(self._etabins)-1):
        self._event[ 'et%d_eta%d' % (etBinIdx,etaBinIdx) ] = None


    self._event_label.append( 'avgmu' )

    # Add fast calo ringsE
    self._event_label.extend( [ 'L2Calo_ring_%d'%r for r in range(100) ] )

    self._event_label.extend( [ 'L2Calo_et',
                                'L2Calo_eta',
                                'L2Calo_phi',
                                'L2Calo_reta',
                                'L2Calo_ehad1', # new
                                'L2Calo_eratio',
                                'L2Calo_f1', # new
                                'L2Calo_f3', # new
                                'L2Calo_weta2', # new
                                'L2Calo_wstot', # new
                                'L2Calo_e2tsts1', # new
                                'L2Electron_hastrack',
                                'L2Electron_pt',
                                'L2Electron_eta',
                                'L2Electron_phi',
                                'L2Electron_caloEta',
                                'L2Electron_trkClusDeta',
                                'L2Electron_trkClusDphi',
                                'L2Electron_etOverPt',

                                ] )

 


    self._event_label.extend( [
                                # Offline variables
                                'et',
                                'eta',
                                'phi',
                                # offline shower shapers
                                'rhad1',
                                'rhad',
                                'f3',
                                'weta2',
                                'rphi',
                                'reta',
                                'wtots1',
                                'eratio',
                                'f1',
                                # offline track
                                'hastrack',
                                'numberOfBLayerHits',
                                'numberOfPixelHits',
                                'numberOfTRTHits',
                                'd0',
                                'd0significance',
                                'eProbabilityHT',
                                'trans_TRT_PID',
                                'deltaEta1',
                                'deltaPhi2',
                                'deltaPhi2Rescaled',
                                'DeltaPOverP',

                                ] )


    
    if self._dataframe is DataframeEnum.Electron_v1:
      self._event_label.extend( [
                                # Offline variables
                                'el_lhtight',
                                'el_lhmedium',
                                'el_lhloose',
                                'el_lhvloose',
                                ] )
    elif self._dataframe is DataframeEnum.Photon_v1:
      self._event_label.extend( [
                                # Offline variables
                                'ph_tight',
                                'ph_medium',
                                'ph_loose',
                                ] )
    else:
      self._event_label.extend( [
                                # Offline variables
                                'el_lhtight',
                                'el_lhmedium',
                                'el_lhloose',
                                'el_lhvloose',
                                ] )


    self._event_label.extend( self._extra_features )

    return StatusCode.SUCCESS


  def fill( self, key , event ):

    if self._event[key]:
      self._event[key].append( event )
    else:
      self._event[key] = [event]


  #
  # execute 
  #
  def execute(self, context):


    if self._dataframe is DataframeEnum.Electron_v1:
      elCont    = context.getHandler( "ElectronContainer" )
      trkCont   = elCont.trackParticle()
      hasTrack = True if trkCont.size()>0 else False
   
      fcElCont = context.getHandler("HLT__TrigElectronContainer" )
      hasFcTrack = True if fcElCont.size()>0 else False

    elif self._dataframe is DataframeEnum.Photon_v1:
      elCont    = context.getHandler( "PhotonContainer" )
      trkCont   = None
      hasTrack  = False
      hasFcTrack = False

    eventInfo = context.getHandler( "EventInfoContainer" )
    fc        = context.getHandler( "HLT__TrigEMClusterContainer" )
    



    from EventSelectionTool import RetrieveBinningIdx
    etBinIdx, etaBinIdx = RetrieveBinningIdx( fc.et()/1000., abs(fc.eta()), self._etbins, self._etabins, logger=self._logger )
    if etBinIdx < 0 or etaBinIdx < 0:
      return StatusCode.SUCCESS


    key = ('et%d_eta%d') % (etBinIdx, etaBinIdx)

    event_row = list()
    # event info
    event_row.append( eventInfo.avgmu() )

    # fast calo features
    event_row.extend( fc.ringsE()   )
    event_row.append( fc.et()       )
    event_row.append( fc.eta()      )
    event_row.append( fc.phi()      )
    event_row.append( fc.reta()     )
    event_row.append( fc.ehad1()    )
    event_row.append( fc.eratio()   )
    event_row.append( fc.f1()       )
    event_row.append( fc.f3()       )
    event_row.append( fc.weta2()    )
    event_row.append( fc.wstot()    )
    event_row.append( fc.e2tsts1()  )



    
    if hasFcTrack:
      fcElCont.setToBeClosestThanCluster()
      event_row.append( True )
      event_row.append( fcElCont.pt() )
      event_row.append( fcElCont.eta() )
      event_row.append( fcElCont.phi() )
      event_row.append( fcElCont.caloEta() )
      event_row.append( fcElCont.trkClusDeta() )  
      event_row.append( fcElCont.trkClusDphi() )
      event_row.append( fcElCont.etOverPt() )
    else:
      event_row.extend( [False, -1, -1, -1, -1, -1, -1, -1] )



      
    # Offline Shower shapes
    event_row.append( elCont.et() )
    event_row.append( elCont.eta() )
    event_row.append( elCont.phi() )
    
    
    from EventAtlas import EgammaParameters
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rhad1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rhad ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.f3 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.weta2 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rphi ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Reta ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.wtots1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Eratio ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.f1 ) )


    # Offline track variables
    if hasTrack:
      event_row.append( hasTrack)
      event_row.append( trkCont.numberOfBLayerHits() )
      event_row.append( trkCont.numberOfPixelHits() )
      event_row.append( trkCont.numberOfTRTHits() )
      event_row.append( trkCont.d0() )
      event_row.append( trkCont.d0significance() )
      event_row.append( trkCont.eProbabilityHT() )
      event_row.append( trkCont.trans_TRT_PID() )
      event_row.append( elCont.deta1() )
      event_row.append( elCont.dphi2() )
      event_row.append( elCont.deltaPhiRescaled2() )
      event_row.append( trkCont.DeltaPOverP() )

    else:
      event_row.extend( [False, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1] )

    


    if self._dataframe is DataframeEnum.Electron_v1:
      event_row.append( elCont.accept( "el_lhtight"  ) )
      event_row.append( elCont.accept( "el_lhmedium" ) )
      event_row.append( elCont.accept( "el_lhloose"  ) )
      event_row.append( elCont.accept( "el_lhvloose" ) )
 


    elif self._dataframe is DataframeEnum.Photon_v1:
      event_row.append( elCont.accept( "ph_tight"  ) )
      event_row.append( elCont.accept( "ph_medium" ) )
      event_row.append( elCont.accept( "ph_loose"  ) )
      
    dec = context.getHandler("MenuContainer")

    for feature in self._extra_features:
      passed = dec.accept(feature).getCutResult('Pass')
      event_row.append( passed )


    self.fill(key , event_row)


    return StatusCode.SUCCESS


  def finalize( self ):

    from Gaugi import save, mkdir_p

    outputname = self.getProperty("OutputFile")

    for etBinIdx in range(len(self._etbins)-1):
      for etaBinIdx in range(len(self._etabins)-1):

        key =  'et%d_eta%d' % (etBinIdx,etaBinIdx)
        mkdir_p( outputname )
        if self._event[key] is None:
          continue

        d = {
            "features"  : self._event_label,
            "etBins"    : self._etbins,
            "etaBins"   : self._etabins,
            "etBinIdx"  : etBinIdx,
            "etaBinIdx" : etaBinIdx
            }

        d[ 'pattern_'+key ] = np.array( self._event[key] )
        MSG_INFO( self, 'Saving %s with : (%d, %d)', key, d['pattern_'+key].shape[0], d['pattern_'+key].shape[1] )
        save( d, outputname+'/'+outputname+"_"+key , protocol = 'savez_compressed')
    return StatusCode.SUCCESS





