
__all__ = ["EmulationTool", "Accept", "attach"]


from Gaugi import ToolSvc
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi.messenger.macros import *
import collections


#
# Emulator
#
class EmulationTool( Algorithm ):


  #
  # Constructor
  #
  def __init__(self):
    Algorithm.__init__(self, "Emulator") 
    self.__tools = {}


  #
  # Add a selector to the list
  #
  def __add__( self, tool ):
    self.__tools[tool.name()] = tool
    return self

  #
  # Get the hypo tool
  #
  def retrieve(self, key):
    return self.__tools[key] if self.isValid(key) else None



  #
  # Initialize method
  #
  def initialize(self):

    tools = [ tool for _, tool in self.__tools.items() ]

    for tool in tools:
      MSG_INFO( self, 'Initializing %s tool',tool.name())
      tool.dataframe = self.dataframe
      tool.setContext( self.getContext() )
      tool.level = self.level
      if tool.initialize().isFailure():
        MSG_ERROR( self, 'Can not initialize %s',tool.name())

    return StatusCode.SUCCESS


  #
  # Execute method
  #
  def execute(self, context):
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept( self, context, key ):

    if self.isValid(key):
      return self.__tools[key].accept( context )
    else:
      MSG_FATAL( self, "The key %s is not in the emulation" , key )


  #
  # Finalized method
  #
  def finalize(self):

    for key, tool in self.__tools.items():
      MSG_INFO( self, 'Finalizing %s tool',key)
      if tool.finalize().isFailure():
        MSG_ERROR( self, 'Can not finalizing %s',tool.name)

    return StatusCode.SUCCESS


  #
  # Check if the selector is installed
  #
  def isValid(self, key ):
    return True if key in self.__tools.keys() else False



#
# Add the emulator tool into the tool service by default
#
ToolSvc += EmulationTool()



#
# Helper to avoid to much repetition code into this file
#
def attach( hypos ):
  from Gaugi import ToolSvc
  emulator = ToolSvc.retrieve( "Emulator" )
  names = []
  for hypo in hypos:
    names.append( hypo.name() )
    if not emulator.isValid( hypo.name() ):
      emulator+=hypo
  return names



#
# Accept
#
class Accept( object ):

  #
  # Constructor
  #
  def __init__(self, name, results=[] ):
    self.__name = name
    self.__results = collections.OrderedDict()

    for (key,value) in results:
      self.__results[key] = value

    self.__decoration = {}

  #
  # Get the accept name
  #
  def name(self):
    return self.__name


  #
  # Add new cut
  #
  def addCut( self, key ):
    self.__results[key] = False


  #
  # Set cut result value
  #
  def setCutResult( self, key, value ):
    self.__results[key] = value


  #
  # Get cut result value
  #
  def getCutResult( self, key ):
    try:
      return self.__results[key]
    except KeyError as e:
      print( e )


  #
  # Is passed
  #
  def __bool__(self):
    x = [v for _, v in self.__results.items()]
    return all( [value for _, value in self.__results.items()] )


  #
  # Add decoration
  #
  def setDecor( self, key, value ):
    self.__decoration[key] = value


  #
  # Get decoration
  #
  def getDecor( self, key ):
    return self.__decoration[key]


