
__all__ = ['TrigEgammaFastPhotonHypoTool']


from Gaugi.messenger.macros import *
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi import ToolSvc

from kepler.menu import treat_trigger_dict_type
from kepler.emulator import Accept

#
# L2Calo hypo tool
#
class TrigEgammaFastPhotonHypoTool( Algorithm ):

  __property = [
                "HADETthr",
                "RCoreThr",
                "CARCOREthr",
                "CAERATIOthr",
                "EtaBins",
                "ETthr",
                "ET2thr",
                "HADET2thr",
                "F1thr",
                ]

  #
  # Constructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)

    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)




  #
  # Initialize method
  #
  def initialize(self): 
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept(self, context):

    passed = self.emulate(context)
    return Accept( self.name(), [ ("Pass", passed)] )



  #
  # Emulation method
  #
  def emulate(self, context):

    # get all properties from the local store
    hadeTthr        = self.getProperty('HADETthr'   )
    carcorethr      = self.getProperty('CARCOREthr' )
    caeratiothr     = self.getProperty('CAERATIOthr')
    etabins         = self.getProperty('EtaBins'    )
    eTthr           = self.getProperty('ETthr'      )
    eT2thr          = self.getProperty('ET2thr'     )
    hadeT2thr       = self.getProperty('HADET2thr'  )
    F1thr           = self.getProperty('F1thr'      )


    pClus = context.getHandler( "HLT__TrigEMClusterContainer" )

    # get the equivalent L1 EmTauRoi object in athena
    PassedCuts=0
    # initialise monitoring variables for each event
    eT_T2Calo     = -1.0
    hadET_T2Calo  = -1.0
    rCore         = -1.0
    energyRatio   = -1.0
    F1            = -1.0
    
    absEta = math.fabs( pClus.eta() )
    etaBin = -1
    if absEta > etabins[-1]:
      absEta=etabins[-1]
    # get the corrct eta bin range
    for idx, value in enumerate(etabins):
      if ( absEta > etabins[idx] and absEta < etabins[idx+1] ):
        etaBin = idx

    # Is in crack region?
    inCrack = True if (absEta > 2.37 or (absEta > 1.37 and absEta < 1.52)) else False

    # calculate cluster quantities // definition taken from TrigElectron constructor
    if ( pClus.emaxs1() + pClus.e2tsts1() ) > 0 :
      energyRatio = ( pClus.emaxs1() - pClus.e2tsts1() ) / float( pClus.emaxs1() + pClus.e2tsts1() )

    # (VD) here the definition is a bit different to account for the cut of e277 @ EF
    if ( pClus.e277()!= 0.):
      rCore = pClus.e237() / float(pClus.e277())

    # fraction of energy deposited in 1st sampling
    #if ( math.fabs(pClus.energy()) > 0.00001) :
    #  F1 = (pClus.energy(CaloSampling.EMB1)+pClus.energy(CaloSampling.EME1))/float(pClus.energy())
    F1 = pClus.f1()

    eT_T2Calo  = float(pClus.et())

    if ( eT_T2Calo!=0 and pClus.eta()!=0 ):
      hadET_T2Calo = pClus.ehad1()/math.cosh(math.fabs(pClus.eta()))/eT_T2Calo

    # eta range
    if ( etaBin==-1 ):  # VD
      MSG_DEBUG(self, "Cluster eta: %1.3f  outside eta range ",absEta )
      return False
    else:
      MSG_DEBUG(self, "eta bin used for cuts ")

    PassedCuts+=1 # passed eta cut


   # ET_em
    if ( eT_T2Calo*1e-3 < eTthr[etaBin]): return False
    PassedCuts+=1 # ET_em

    # Rcore
    if ( rCore < carcorethr[etaBin] ):  return False
    PassedCuts+=1 # Rcore

    # Eratio
    if ( inCrack or F1<F1thr[etaBin] ):
      MSG_DEBUG(self, "TrigEMCluster: InCrack= %d F1=%1.3f",inCrack,F1 )
    else:
      if ( energyRatio < caeratiothr[etaBin] ): return False

    PassedCuts+=1 # Eratio
    if(inCrack): energyRatio = -1; # Set default value in crack for monitoring.

    hadET_cut = -1
    # find which ET_had to apply : this depends on the ET_em and the eta bin
    if ( eT_T2Calo >  eT2thr[etaBin] ):
      hadET_cut = hadeT2thr[etaBin]
    else:
      hadET_cut = hadeTthr[etaBin]

    # ET_had
    if ( hadET_T2Calo > hadET_cut ): return False
    PassedCuts+=1 #ET_had
    # F1
    # if ( F1 < m_F1thr[0]) return true;  //(VD) not cutting on this variable, only used to select whether to cut or not on eRatio
    PassedCuts+=1 # F1
    

    # got this far => passed!
    MSG_DEBUG(self, 'T2Calo emulation approved...')
    return True


  #
  # Finalize method
  #
  def finalize(self):
    return StatusCode.SUCCESS






def configure_from_trigger( trigger ):

  d = treat_trigger_dict_type( trigger )
  etthr = d['etthr']
  pidname = d['pidname']
  name = 'Hypo__FastPhoton__' + trigger
  emulator = ToolSvc.retrieve("Emulator")
  if not emulator.isValid(name):
    hypo = configure(name, etthr, pidname)
    emulator+=hypo

  return name


#
# Configure the hypo from trigger name
#
def configure( name, etthr, pidname ):


  def same(value):
    return [value]*9

  from kepler.emulator import L2CaloPhotonCutMaps, TrigEgammaFastPhotonHypoTool
  cuts = L2CaloPhotonCutMaps(etthr)
  hypo  = TrigEgammaFastPhotonHypoTool(name,
                                   EtaBins        = [0.0, 0.6, 0.8, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47],
                                   F1thr          = same(0.005),
                                   ETthr          = same(0),
                                   ET2thr         = same(90.0*GeV),
                                   HADET2thr      = same(999.0),
                                   HADETthr       = cuts.MapsHADETthr[pidname],
                                   CARCOREthr     = cuts.MapsCARCOREthr[pidname],
                                   CAERATIOthr    = cuts.MapsCAERATIOthr[pidname],
                                   )

  return hypo
