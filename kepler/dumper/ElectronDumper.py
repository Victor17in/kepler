
__all__ = ["ElectronDumper"]


from kepler.core import Dataframe as DataframeEnum 
from kepler.events import EgammaParameters
from kepler.utils import get_bin_indexs

from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import save, load
from Gaugi.messenger.macros import *
from Gaugi.constants import GeV

import numpy as np


class ElectronDumper( Algorithm ):


  #
  # constructor
  #
  def __init__(self, name, output, etbins, etabins, dumpRings=True ):
    
    Algorithm.__init__(self, name)
    self.__event = {}
    self.__event_label = []
    self.__save_these_bins = list()
    self.__extra_features = list()
    self.__outputname = output
    self.__etbins = etbins
    self.__etabins = etabins
    self.dumpRings = dumpRings


 
  def __add__( self, key ):
    if type(key) is str:
      key = [key]
    self.__extra_features.extend( key )
    return self


  #
  # Initialize dumper
  #
  def initialize(self):

    Algorithm.initialize(self)

    # build map
    for etBinIdx in range(len(self.__etbins)-1):
      for etaBinIdx in range(len(self.__etabins)-1):
        self.__event[ 'et%d_eta%d' % (etBinIdx,etaBinIdx) ] = None


    #
    # Event info
    #
    self.__event_label.extend( ['RunNumber', 'avgmu'] )

    #
    # Fast calo
    #
    self.__event_label.extend( [
                                'trig_L2_cl_et',
                                'trig_L2_cl_eta',
                                'trig_L2_cl_phi',
                                'trig_L2_cl_reta',
                                'trig_L2_cl_ehad1', 
                                'trig_L2_cl_eratio',
                                'trig_L2_cl_f1', 
                                'trig_L2_cl_f3', 
                                'trig_L2_cl_weta2', 
                                'trig_L2_cl_wstot', 
                                'trig_L2_cl_e2tsts1'] )

    # Add fast calo ringsE
    if self.dumpRings:
      self.__event_label.extend( [ 'trig_L2_cl_ring_%d'%r for r in range(100) ] )


    #
    # Fast electron
    #
    self.__event_label.extend( [
                                'trig_L2_el_hastrack',
                                'trig_L2_el_pt',
                                'trig_L2_el_eta',
                                'trig_L2_el_phi',
                                'trig_L2_el_caloEta',
                                'trig_L2_el_trkClusDeta',
                                'trig_L2_el_trkClusDphi',
                                'trig_L2_el_etOverPt'] )

    #
    # Calo cluster
    #
    self.__event_label.extend( [
                                'trig_EF_cl_et', # this is a list
                                ] )

    #
    # HLT electron
    #
    self.__event_label.extend( [       
                                'trig_EF_el_et', # this is a list
                                'trig_EF_el_lhtight', # this is a list
                                'trig_EF_el_lhmedium', # this is a list
                                'trig_EF_el_lhloose', # this is a list
                                'trig_EF_el_lhvloose', # this is a list
                                ] )


    #
    # Offline variables
    #
    self.__event_label.extend( [
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
                                'DeltaR_TaP',
                                'el_lhtight',
                                'el_lhmedium',
                                'el_lhloose',
                                'el_lhvloose',
                                ] )


  
    self.__event_label.extend( self.__extra_features )

    print(len(self.__event_label))
    return StatusCode.SUCCESS


  #
  # fill current event
  #
  def fill( self, key , event ):

    if self.__event[key]:
      self.__event[key].append( event )
    else:
      self.__event[key] = [event]


  #
  # execute 
  #
  def execute(self, context):





    event_row = list()

    #
    # event info
    #
    eventInfo = context.getHandler( "EventInfoContainer" )
    event_row.append( eventInfo.RunNumber() )
    event_row.append( eventInfo.avgmu() )


    #
    # Fast Calo features
    #
    fc = context.getHandler( "HLT__TrigEMClusterContainer" )



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
    if self.dumpRings:
      event_row.extend( fc.ringsE()   )
   
    #
    # Fast electron features
    #
    fcElCont = context.getHandler("HLT__TrigElectronContainer" )
    hasFcTrack = True if fcElCont.size()>0 else False
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


    #
    # Calo Cluster
    #
    clCont = context.getHandler("HLT__CaloClusterContainer")
    event_row.append( np.array([cl.et() for cl in clCont]))

    
    #
    # HLT electron
    #
    elCont = context.getHandler("HLT__ElectronContainer")
    event_row.append(np.array([el.et() for el in elCont]))
    # Adding PID LH decisions for each WP
    event_row.append(np.array([el.accept("trig_EF_el_lhtight") for el in elCont]))
    event_row.append(np.array([el.accept("trig_EF_el_lhmedium") for el in elCont]))
    event_row.append(np.array([el.accept("trig_EF_el_lhloose") for el in elCont]))
    event_row.append(np.array([el.accept("trig_EF_el_lhvloose") for el in elCont]))

      
    #
    # Offline variables
    #

    elCont   = context.getHandler( "ElectronContainer" )
    trkCont  = elCont.trackParticle()
    hasTrack = True if trkCont.size()>0 else False
   
    # Offline Shower shapes
    event_row.append( elCont.et() )
    event_row.append( elCont.eta() )
    event_row.append( elCont.phi() )
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

    event_row.append( elCont.deltaR() )
    # Adding Offline PID LH decisions
    event_row.append( elCont.accept( "el_lhtight"  ) )
    event_row.append( elCont.accept( "el_lhmedium" ) )
    event_row.append( elCont.accept( "el_lhloose"  ) )
    event_row.append( elCont.accept( "el_lhvloose" ) )
 
    #
    # Decorate with other decisions
    #

    dec = context.getHandler("MenuContainer")

    for feature in self.__extra_features:
      passed = dec.accept(feature).getCutResult('Pass')
      event_row.append( passed )


    etBinIdx, etaBinIdx = get_bin_indexs( fc.et()/1000., abs(fc.eta()), self.__etbins, self.__etabins, logger=self._logger )
    if etBinIdx < 0 or etaBinIdx < 0:
      return StatusCode.SUCCESS

    key = ('et%d_eta%d') % (etBinIdx, etaBinIdx)
    self.fill(key , event_row)
    return StatusCode.SUCCESS


  def finalize( self ):

    from Gaugi import save, mkdir_p
    outputname = self.__outputname

    for etBinIdx in range(len(self.__etbins)-1):
      for etaBinIdx in range(len(self.__etabins)-1):

        key =  'et%d_eta%d' % (etBinIdx,etaBinIdx)
        mkdir_p( outputname )
        if self.__event[key] is None:
          continue

        d = {
            "features"  : self.__event_label,
            "etBins"    : self.__etbins,
            "etaBins"   : self.__etabins,
            "etBinIdx"  : etBinIdx,
            "etaBinIdx" : etaBinIdx
            }

        d[ 'pattern_'+key ] = np.array( self.__event[key] )
        MSG_INFO( self, 'Saving %s with : (%d, %d)', key, d['pattern_'+key].shape[0], d['pattern_'+key].shape[1] )
        save( d, outputname+'/'+outputname+"_"+key , protocol = 'savez_compressed')
    return StatusCode.SUCCESS





