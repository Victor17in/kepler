
__all__ = ['ElectronLoop', 'PhotonLoop']


from Gaugi.messenger import Logger, LoggingLevel
from Gaugi.messenger.macros import *
from Gaugi import StatusCode, StatusTool
from Gaugi.TEventLoop import TEventLoop

from kepler.core.enumerators import Dataframe as DataframeEnum

#
# Electron loop
#
class ElectronLoop( TEventLoop ):

  def __init__(self, name , **kw):
    # Retrieve all information needed
    TEventLoop.__init__(self, name, **kw)


  #
  # Initialize all services
  #
  def initialize( self ):

    MSG_INFO( self, 'Initializing Event...')
    if super(ElectronLoop,self).initialize().isFailure():
      MSG_FATAL( self, "Impossible to initialize the TEventLoop services.")

    if self._dataframe is DataframeEnum.Electron_v1:
      from kepler.dataframe import Electron_v1
      self._event = Electron_v1()
    else:
      return StatusCode.FATAL


    MSG_INFO( self, "Creating containers...")
    # Allocating containers
    from kepler.events import Electron
    from kepler.events import TrigEMCluster
    from kepler.events import TrigElectron
    from kepler.events import CaloCluster
    from kepler.events import TrackParticle
    from kepler.events import EmTauRoI
    from kepler.events import EventInfo
    from kepler.events import MonteCarlo
    from kepler.events import TDT
    from kepler.events import Menu


    # Initialize the base of this container.
    # Do not change this key names!
    self._containersSvc  = {
                            # event dataframe containers
                            'EventInfoContainer'         : EventInfo(),
                            'MonteCarloContainer'        : MonteCarlo(),
                            'CaloClusterContainer'       : CaloCluster(),
                            'MenuContainer'              : Menu(),
                           }

    self._containersSvc.update({
                            'HLT__TrigEMClusterContainer': TrigEMCluster(),
                            'HLT__CaloClusterContainer'  : CaloCluster(),
                            'HLT__EmTauRoIContainer'     : EmTauRoI(),
                            })

    self._containersSvc.update({  'ElectronContainer'           : Electron(),
                                    'TrackParticleContainer'      : TrackParticle(),
                                    'HLT__TrigElectronContainer'  : TrigElectron(),
                                    'HLT__ElectronContainer'      : Electron(),
                                    'HLT__TrackParticleContainer' : TrackParticle(),
                                })
  

    # append TDT container
    if self._dataframe is DataframeEnum.Electron_v1:
      self._containersSvc.update({
                            # metadata containers
                            'HLT__TDT'                   : TDT(),
                            })


    # force the event id number for this event looper
    #self._containersSvc['EventInfoContainer'].setId( self.id() )
    # Add decoration for  event information
    self._containersSvc['EventInfoContainer'].setDecor( "is_fakes", True if 'fakes' in self._treePath else False)



    # configure all EDMs needed
    for key, edm  in self._containersSvc.items():
      self.getContext().setHandler(key,edm)
      # add properties
      edm.dataframe = self._dataframe
      edm.tree  = self._t
      edm.level = self._level
      edm.event = self._event
      edm.setContext(self.getContext())

      # enable hlt property by the container key name
      if 'HLT' in key:
        edm.is_hlt = True

      # set basepath into the root file
      if edm.useMetadataParams():
        edm.setMetadataParams( {'basepath':self._metadataInputFile[1].rsplit('/',1)[0],
                                 'file':self._metadataInputFile[0]} ) # remove the last name after '/' (tree name)
      # If initializations is failed, we must remove this from the container
      # service
      MSG_INFO( self, "Initialize the dataframe with name: %s" , key )
      if(edm.initialize().isFailure()):
        MSG_WARNING( self, 'Impossible to create the EDM: %s',key)

    self.getContext().initialize()

    MSG_INFO( self, 'Initializing all tools...')
    from Gaugi import ToolSvc as toolSvc
    self._alg_tools = toolSvc.getTools()
    for alg in self._alg_tools:
      if alg.status is StatusTool.DISABLE:
        continue
      # Retrieve all services
      alg.level = self._level
      alg.setContext( self.getContext() )
      alg.setStoreGateSvc( self.getStoreGateSvc() )
      alg.dataframe = self._dataframe
      if alg.isInitialized():
        continue
      if alg.initialize().isFailure():
        MSG_FATAL( self, "Impossible to initialize the tool name: %s",alg.name)

    return StatusCode.SUCCESS




class PhotonLoop( TEventLoop ):

  def __init__(self, name , **kw):
    # Retrieve all information needed
    TEventLoop.__init__(self, name, **kw)


  #
  # Initialize all services
  #
  def initialize( self ):

    MSG_INFO( self, 'Initializing Event...')
    if super(Event,self).initialize().isFailure():
      MSG_FATAL( self, "Impossible to initialize the TEventLoop services.")

    if self._dataframe is DataframeEnum.Photon_v1:
      from kepler.events import Photon_v1
      self._event = Photon_v1()
    else:
      return StatusCode.FATAL


    MSG_INFO( self, "Creating containers...")
    # Allocating containers
    from kepler.events import Photon
    from kepler.events import TrigEMCluster
    from kepler.events import CaloCluster
    from kepler.events import EmTauRoI
    from kepler.events import EventInfo
    from kepler.events import MonteCarlo
    from kepler.events import TDT
    from kepler.events import Menu


    # Initialize the base of this container.
    # Do not change this key names!
    self._containersSvc  = {
                            # event dataframe containers
                            'EventInfoContainer'         : EventInfo(),
                            'MonteCarloContainer'        : MonteCarlo(),
                            'CaloClusterContainer'       : CaloCluster(),
                            'MenuContainer'              : Menu(),
                           }

    self._containersSvc.update({
                            'HLT__TrigEMClusterContainer': TrigEMCluster(),
                            'HLT__CaloClusterContainer'  : CaloCluster(),
                            'HLT__EmTauRoIContainer'     : EmTauRoI(),
                            })

    self._containersSvc.update({  'PhotonContainer'             : Photon(),
                                    'HLT__PhotonContainer'        : Photon(),
                                })

    # append TDT container
    if self._dataframe is DataframeEnum.Photon_v1:
      self._containersSvc.update({
                            # metadata containers
                            'HLT__TDT'                   : TDT(),
                            })


    # force the event id number for this event looper
    #self._containersSvc['EventInfoContainer'].setId( self.id() )
    # Add decoration for  event information
    self._containersSvc['EventInfoContainer'].setDecor( "is_fakes", True if 'fakes' in self._treePath else False)



    # configure all EDMs needed
    for key, edm  in self._containersSvc.items():
      self.getContext().setHandler(key,edm)
      # add properties
      edm.dataframe = self._dataframe
      edm.tree  = self._t
      edm.level = self._level
      edm.event = self._event
      edm.setContext(self.getContext())

      # enable hlt property by the container key name
      if 'HLT' in key:
        edm.is_hlt = True

      # set basepath into the root file
      if edm.useMetadataParams():
        edm.setMetadataParams( {'basepath':self._metadataInputFile[1].rsplit('/',1)[0],
                                 'file':self._metadataInputFile[0]} ) # remove the last name after '/' (tree name)
      # If initializations is failed, we must remove this from the container
      # service
      MSG_INFO( self, "Initialize the dataframe with name: %s" , key )
      if(edm.initialize().isFailure()):
        MSG_WARNING( self, 'Impossible to create the EDM: %s',key)

    self.getContext().initialize()

    MSG_INFO( self, 'Initializing all tools...')
    from Gaugi import ToolSvc as toolSvc
    self._alg_tools = toolSvc.getTools()
    for alg in self._alg_tools:
      if alg.status is StatusTool.DISABLE:
        continue
      # Retrieve all services
      alg.level = self._level
      alg.setContext( self.getContext() )
      alg.setStoreGateSvc( self.getStoreGateSvc() )
      alg.dataframe = self._dataframe
      if alg.isInitialized():
        continue
      if alg.initialize().isFailure():
        MSG_FATAL( self, "Impossible to initialize the tool name: %s",alg.name)

    return StatusCode.SUCCESS



