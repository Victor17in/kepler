
__all__ = ['TrigEgammaPrecisionElectronHypoTool',
           'TrigEgammaPrecisionElectronIsolationHypoTool']

from Gaugi.messenger.macros import *
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi import ToolSvc
from kepler.emulator import Accept
from kepler.menu import treat_trigger_dict_type

#
# Hypo tool
#
class TrigEgammaPrecisionElectronHypoTool( Algorithm ):

  __property = [
                "Branch"
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
    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  # 
  def accept(self, context):

    el= context.getHandler("HLT__ElectronContainer")
  
    branch = self.getProperty("Branch")

    if not el.checkBody( branch ):
      MSG_FATAL( self, "The branch %s is not found into the HLT electron body.", branch )


    # helper accessor function
    def getDecision( container, branch ):
      passed=False
      current = container.getPos()
      for it in container:
        if it.accept(branch):  passed=True;  break;
      container.setPos(current) # to avoid location fail
      return passed

    # Decorate the HLT electron with all final decisions
    passed =  getDecision(el, branch)

    return Accept( self.name(), [ ("Pass", passed) ] )


  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS







#
# Hypo tool
#
class TrigEgammaPrecisionElectronIsolationHypoTool( Algorithm ):

  __property = [
                "EtConeCut",
                "PtConeCut",
                "RelEtConeCut",
                "RelPtConeCut",
                "UseClusETforCaloIso",
                "UseClusETforTrackIso",
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

    self.__etConeCut = self.getProperty( "EtConeCut" )
    self.__ptConeCut = self.getProperty( "PtConeCut" )
    self.__relEtConeCut = self.getProperty( "RelEtConeCut" )
    self.__relPtConeCut = self.getProperty( "RelPtConeCut" )
    self.__useClusETforCaloIso = self.getProperty( "UseClusETforCaloIso" )
    self.__useClusETforTrackIso = self.getProperty( "UseClusETforTrackIso" )

    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  # 
  def accept(self, context):

    elCont= context.getHandler("HLT__ElectronContainer")

    current = elCont.getPos()

    passed = False

    for el in elCont:


      etcone20 = el.isolationValue( IsolationType.etcone20 )
      etcone30 = el.isolationValue( IsolationType.etcone30 )
      etcone40 = el.isolationValue( IsolationType.etcone40 )

      ptcone20 = el.isolationValue( IsolationType.ptcone20 )
      ptcone30 = el.isolationValue( IsolationType.ptcone30 )
      ptcone40 = el.isolationValue( IsolationType.ptcone40 )

      ptvarcone20 = el.isolationValue( IsolationType.ptvarcone20 )
      ptvarcone30 = el.isolationValue( IsolationType.ptvarcone30 )
      ptvarcone40 = el.isolationValue( IsolationType.ptvarcone40 )

      etcone = [
                etcone20,
                etcone30,
                etcone40,
               ]

      
      ptcone = [
                ptcone20,
                ptcone30,
                ptcone40,
                ptvarcone20,
                ptvarcone30,
                ptvarcone40
                ]

      el_clus_pt     = el.caloCluster().et()
      el_trk_pt      = el.trackParticle().pt() if el.trackParticle() else -999
      caloIso_ele_pt = el_clus_pt if self.__useClusETforCaloIso else el_trk_pt
      trkIso_ele_pt  = el_clus_pt if self.__useClusETforTrackIso else el_trk_pt



      absEtConeCut_ispassed = True

      # Cut on Absolute Calo Isolation
      for idx, value in enumerate( etcone ):
        if self.__etConeCut[idx] > 0 and value > self.__etConeCut[idx]:
          absEtConeCut_ispassed = False
          break


      if not absEtConeCut_ispassed:
        continue

      
      absPtConeCut_ispassed = True

      # Cut on Absolute Track Isolation
      for idx, value in enumerate( ptcone ):
        if self.__ptConeCut[idx] > 0 and value > self.__ptConeCut[idx]:
          absPtConeCut_ispassed = False
          break


      if not absPtConeCut_ispassed:
        continue



      relEtcone = []

      # Fill rel et cone
      for idx, value in enumerate( etcone ):
        if caloIso_ele_pt > 0.:
          relEtcone.append( value/caloIso_ele_pt )
        else:
          relEtcone.append( 99990. )


      relPtcone = []
      
      # Fill rel pt cone
      for idx, value in enumerate( ptcone ):
        if caloIso_ele_pt > 0.:
          relPtcone.append( value/trkIso_ele_pt )
        else:
          relPtcone.append( 99990. )

      


      relEtConeCut_ispassed = True

      # Cut on Absolute Calo Isolation
      for idx, value in enumerate( relEtcone ):
        if self.__relEtConeCut[idx] > 0 and value > self.__relEtConeCut[idx]:
          relEtConeCut_ispassed = False
          break


      if not relEtConeCut_ispassed:
        continue

      
      relPtConeCut_ispassed = True

      # Cut on Absolute Track Isolation
      for idx, value in enumerate( relPtcone ):
        if self.__ptConeCut[idx] > 0 and value > self.__ptConeCut[idx]:
          relPtConeCut_ispassed = False
          break


      if not relPtConeCut_ispassed:
        continue

      
      passed=True
      if passed:
        break
      

    elCont.setPos( current )

    return Accept( self.name(), [ ("Pass", passed) ] )


  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS







def configure_from_trigger( trigger ):

  d = treat_trigger_dict_type(trigger)
  etthr = d['etthr']
  pidname = d['pidname']
  name = 'Hypo__HLT__' + trigger
  emulator = ToolSvc.retrieve("Emulator")
  if not emulator.isValid(name):
    hypo = configure(name, pidname)
    emulator+=hypo

  return name



def configure_iso_from_trigger( trigger ):

  d = treat_trigger_dict_type(trigger)
  iso = d['iso']
  name = 'Hypo__HLT__' + trigger
  emulator = ToolSvc.retrieve("Emulator")
  if not emulator.isValid(name):
    hypo = configure_iso(name, iso)
    emulator+=hypo

  return name


#
# Configure the hypo tool from trigger name
#
def configure( name, pidname ):

  from kepler.emulator import TrigEgammaPrecisionElectronHypoTool
  hypo  = TrigEgammaPrecisionElectronHypoTool(name, Branch = 'trig_EF_el_'+pidname)
  return hypo



#
# Configure the hypo tool from trigger name
#
def configure_iso( name, iso):

  isolation_dict = {
                    'ivarloose'   : [-1, -1, -1,0.100,-1,-1],
                    'ivarmedium'  : [-1, -1, -1,0.065,-1,-1],
                    'ivartight'   : [-1, -1, -1,0.05,-1,-1],
                    'iloose'      : [0.100, -1, -1,-1,-1,-1],
                   }
  
  caloisolation_dict = {
                        'icaloloose'  : [-1, -1, -1,0.2,-1,-1],
                        'icalomedium' : [-1, -1, -1,0.15,-1,-1],
                        'icalotight'  : [-1, -1, -1,0.1,-1,-1],
                       }

  relEtConeCuts = caloisolation_dict[iso] if 'icalo' in iso else [-1, -1, -1,-1, -1, -1]
  relPtConeCuts = isolation_dict[iso] if not 'icalo' in iso else [-1, -1, -1,-1, -1, -1]

  from kepler.emulator import TrigEgammaPrecisionElectronIsolationHypoTool
  hypo  = TrigEgammaPrecisionlectronIsolationHypoTool(name,
                                                UseClusETforCaloIso   = True,
                                                UseClusETforTrackIso  = True,
                                                PtConeCut             = [-1, -1, -1,-1,-1,-1],
                                                EtConeCut             = [-1, -1, -1,-1, -1, -1],
                                                RelPtConeCut          = relPtConeCuts,
                                                RelEtConeCut          = relEtConeCuts,
                                                )

  return hypo

