
__all__ = ['TDT']

from Gaugi import Algorithm 
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi.messenger.macros import *

from kepler.emulator import Accept


#
# Chain definition
#
class TDT( Algorithm ):


  #
  # Constructor
  #
  def __init__(self, name, chain):
    
    Algorithm.__init__(self, name)
    self.__trigger = chain[4::] if chain.startswith('HLT_') else chain


  #
  # Initialize method
  #
  def initialize(self):
    tdt = self.getContext().getHandler("HLT__TDT")    
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
    
    accept = Accept( self.name(), [(key,False) for key in ['L1Calo','L2Calo','L2','EFCalo','HLT']] )

    dec = context.getHandler( "MenuContainer" )
    
    # Get the decision from the TDT metadata
    passedL1Calo = bool(dec.accept( "TDT__L1Calo__"+self.__trigger ))
    passedL2Calo = bool(dec.accept( "TDT__L2Calo__"+self.__trigger ))
    passedL2     = bool(dec.accept( "TDT__L2__"    +self.__trigger ))
    passedEFCalo = bool(dec.accept( "TDT__EFCalo__"+self.__trigger ))
    passedHLT    = bool(dec.accept( "TDT__HLT__"   +self.__trigger ))
    
    accept.setCutResult( 'L1Calo' , passedL1Calo )
    accept.setCutResult( 'L2Calo' , passedL2Calo )
    accept.setCutResult( 'L2'     , passedL2     )
    accept.setCutResult( 'EFCalo' , passedEFCalo )
    accept.setCutResult( 'HLT'    , passedHLT    )
    accept.setCutResult( 'Pass'   , passedHLT    )

    return accept











