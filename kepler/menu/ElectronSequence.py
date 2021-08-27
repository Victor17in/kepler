
__all__ = ['ElectronSequence']

from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi.messenger.macros import *


#
# Chain definition
#
class ElectronSequence( Algorithm ):


  #
  # Constructor
  #
  def __init__(self, name, chain, L1Seed = None):

    Algorithm.__init__(self, name)
    self.__l1Seed = L1Item
    self.__chain = chain



  #
  # Initialize method
  #
  def initialize(self):

    #
    # Include and configure everythong into the emulator tool
    #

    from kepler.menu import TriggerDict
    d = TriggerDict( self.chain , L1Seed = self.__l1seed)

    # Configure the L1Calo hypo step 0
    from kepler.emulator.TrigEgammaL1CaloHypoAlg import configure_from_trigger
    self.__l1calo_key = configure_from_trigger(d)

    # configure the fast electron hypo step 2
    from kepler.emulator.TrigEgammaFastElectronHypoAlg import configure_from_trigger
    self.__fast_electron = configure_from_trigger(d)

    # Configure the HLT hypo step
    from kepler.emulator.TrigEgammaPrecisionElectronHypoAlg import configure_from_trigger
    self.__electron_key = configure_from_trigger(d)


    # configure the HLT isolation additional HLT step
    if d['iso']:
      from kepler.emulator.TrigEgammaPrecisionElectronHypoAlg import configure_iso_from_trigger
      self.__electron_iso_key = configure_iso_from_trigger(d)



    # configure et cuts now
    etthr = d['etthr']
    self.__l2calo_EtCut = (etthr - 3 ) * GeV
    self.__precisioncalo_EtCut = etthr * GeV
    self.__electron_EtCut = etthr * GeV


 
    # Print chain info steps
    MSG_INFO( self, "")
    MSG_INFO( self, "+ Chain with name   : %s", self.name() )
    MSG_INFO( self, "|--> L1Calo       : %s", self.__l1caloItem)
    MSG_INFO( self, "|--> L2Calo EtCut : %d", self.__l2caloEtCut)
    MSG_INFO( self, "|--> L2Calo       : %s", self.__l2caloItem)
    MSG_INFO( self, "|--> L2           : %s", self.__l2Item)
    MSG_INFO( self, "|--> EFCalo EtCut : %d", self.__efcaloEtCut)
    MSG_INFO( self, "|--> HLT EtCut    : %d", self.__hltEtCut)
    MSG_INFO( self, "|--> HLT          : %s", self.__hltItem)
    if self.__applyIsolation:
      MSG_INFO( self, "|--> HLTIso       : %s", self.__hltIsoItem)


    self.init_lock()
    return StatusCode.SUCCESS



  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept( self, context ):

    dec = context.getHandler( "MenuContainer" )
    accept = Accept( self.name(),  [(key, False) for key in ['L1Calo','L2Calo','L2','EFCalo','HLT','Pass'] ])

    passedL1 = bool(dec.accept( self.__l1caloItem ))


    # Is passed by L1?
    if not passedL1:
      return accept

    accept.setCutResult( 'L1Calo' , True )

    # Is passed by L2Calo et cut? AND hypo cut
    em = context.getHandler("HLT__TrigEMClusterContainer")

    if  not ( ( em.et() > self.__l2caloEtCut ) and bool(dec.accept( self.__l2caloItem )) ):
      return accept

    accept.setCutResult( 'L2Calo' , True )



    if self.__trigInfo.signature() == 'electron':
      cont = context.getHandler("HLT__TrigElectronContainer")
    else:
      cont = context.getHandler("HLT__PhotonContainer")

    # Is passed by L2 electron/photon, treat events with container with size equal zero
    passedL2 = bool(dec.accept( self.__l2Item )) if cont.size() > 0 else False

    if not passedL2:
      return accept


    accept.setCutResult( 'L2' , True )

    # Is passed by EF calo et cut
    clCont = context.getHandler( "HLT__CaloClusterContainer" )
    current = clCont.getPos()
    passedEFCalo = False
    for cl in clCont:
      if cl.et() > self.__efcaloEtCut:
        passedEFCalo=True
        break

    if not passedEFCalo:
      return accept


    accept.setCutResult( 'EFCalo' , True )



    # Is passed by HLT electron/photon et cut
    passedHLT_etcut = False

    if self.__signature == 'electron':
      cont = context.getHandler("HLT__ElectronContainer")
      for el in cont:
        if el.et() > self.__hltEtCut:
          passedHLT_etcut = True; break

    elif self.__signature == 'photon':
      cont = context.getHandler("HLT__PhotonContainer")
      for ph in cont:
        if ph.et() > self.__hltEtCut:
          passedHLT_etcut = True; break

    else:
      MSG_FATAL( self, "signature not reconized to emulate the HLT et cut step" )


    if not passedHLT_etcut:
      return accept


    # check the HLT decision
    passedHLT = bool( dec.accept( self.__hltItem ) )

    if passedHLT and self.__applyIsolation:
      # Apply the isolation cut and overwrite the HLT previus decision
      passedHLT = bool( dec.accept( self.__hltIsoItem ) )


    accept.setCutResult( 'HLT', passedHLT )
    accept.setCutResult( 'Pass', passedHLT )

    return accept








