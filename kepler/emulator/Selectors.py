
__all__ = ["FastCaloSelectorTool", "FastPhotonSelectorTool", "RingerSelectorTool"]

from Gaugi.messenger.macros import *
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi import ToolSvc

from kepler.menu import treat_trigger_dict_type
from kepler.emulator import Accept

#
# Selector tool
#
class FastPhotonSelectorTool( Algorithm ):

  __property = [ "WPName"]

  #
  # Contructor
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
    self.__hypos = []
    thrs = [0.0, 12.0,17.0,22.0,32.0,44.0]
    for idx, threshold in enumerate(thrs):
      from kepler.emulator.TrigEgammaFastPhotonHypoTool import configure
      hypo = configure( self._name + "_" + str(idx) , threshold, pidname)
      if hypo.initialize().isFailure():
        return StatusCode.FAILURE
      self.__hypos.append(hypo)

    self.init_lock()
    return StatusCode.SUCCESS



   #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):

    fc = context.getHandler( "HLT__TrigEMClusterContainer" )
    et = fc.et()
    passed = False  
    if et < 10*GeV:
      passed = self.__hypos[0].accept(context)
    elif et>=10*GeV and et < 15*GeV:
      passed = self.__hypos[1].accept(context)
    elif et>=15*GeV and et < 20*GeV:
      passed = self.__hypos[2].accept(context)
    elif et>=20*GeV and et < 30*GeV:
      passed = self.__hypos[3].accept(context)
    elif et>=30*GeV and et < 40*GeV:
      passed = self.__hypos[4].accept(context)
    else:
      passed =  self.__hypos[5].accept(context)
    return passed



  #
  # Finalize method
  #
  def finalize(self):
    for hypo in self.__hypos:
      if hypo.finalize().isFailure():
        return StatusCode.FAILURE

    return StatusCode.SUCCESS







#
# Selector tool
#
class FastCaloSelectorTool( Algorithm ):

  __property = [ "WPName"]

  #
  # Contructor
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
    self.__hypos = []
    thrs = [0.0, 15.0, 28] # dummy thrsholds to select the energy range inside of L2CaloCutMaps

    for idx, threshold in enumerate(thrs):
      from kepler.emulator.TrigEgammaFastCaloHypoTool import configure
      hypo = configure( self._name + "_" + str(idx) , threshold, pidname)
      if hypo.initialize().isFailure():
        return StatusCode.FAILURE
      self.__hypos.append(hypo)

    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Generate the decision given the cluster threshold to select the apropriated L2Calo selector
  #
  def accept(self, context):

    fc = context.getHandler( "HLT__TrigEMClusterContainer" )
    et = fc.et()
    passed = False
    if et < 12*GeV:
      passed = self.__hypos[0].accept(context)
    elif et>=12*GeV and et < 22*GeV:
      passed = self.__hypos[1].accept(context)
    else:
      passed =  self.__hypos[2].accept(context)

    return passed


  #
  # Finalize method
  #
  def finalize(self):
    for hypo in self.__hypos:
      if hypo.finalize().isFailure():
        return StatusCode.FAILURE

    return StatusCode.SUCCESS





#
# Hypo tool
#
class RingerSelectorTool(Algorithm):

  __property = [ "ConfigFile" ]

  #
  # Constructor
  #
  def __init__(self, name, generator ,**kw  ):

    Algorithm.__init__(self, name)

    # Set all properties
    for key, value in kw.items():
      if key in self.__property:
        self.declareProperty( key, value )
      else:
        MSG_FATAL( self, "Property with name %s is not allow for %s object", key, self.__class__.__name__)

    self.__models = []
    self.__thresholds = []
    self.__generator = generator


  #
  # Inialize the selector
  #
  def initialize(self):

    #
    # Model inference
    #
    class Model(object):

      def __init__( self, path, etmin, etmax, etamin, etamax):
        self.__etmin=etmin; self.__etmax=etmax; self.__etamin=etamin; self.__etamax=etamax
        from tensorflow.keras.models import model_from_json
        with open(path+'.json', 'r') as json_file:
          self.__model = model_from_json(json_file.read())
          # load weights into new model
          self.__model.load_weights(path+".h5")

      def predict( self, input ):
          #return self.__model.predict(input)[0][0] # too slow
          return self.__model(input)[0][0].numpy() # tensorflow 2.3.1 >

      def etmin(self):
        return self.__etmin
      def etmax(self):
        return self.__etmax
      def etamin(self):
        return self.__etamin
      def etamax(self):
        return self.__etamax

    #
    # Threshold model class
    #
    class Threshold(object):
      def __init__( self, slope, offset, etmin, etmax, etamin, etamax, max_avgmu):
        self.slope=slope; self.offset=offset; self._etmin=etmin; self._etmax=etmax; self._etamin=etamin; self._etamax=etamax
        self.max_avgmu = max_avgmu
      def etmin(self):
        return self._etmin
      def etmax(self):
        return self._etmax
      def etamin(self):
        return self._etamin
      def etamax(self):
        return self._etamax
      def __call__(self, avgmu):
        avgmu = self.max_avgmu if avgmu>self.max_avgmu else avgmu
        return avgmu*self.slope + self.offset


    def treat_float( env, key ):
      return [float(value) for value in  env.GetValue(key, '').split('; ')]

    def treat_string( env, key ):
      return [str(value) for value in  env.GetValue(key, '').split('; ')]

    configPath = self.getProperty( "ConfigFile" )

    MSG_INFO( self, "Reading tuning from: %s", configPath )
    basepath = '/'.join(configPath.split('/')[:-1])


    from ROOT import TEnv
    print(configPath)
    env = TEnv( configPath )
    version = env.GetValue("__version__", '')
    number_of_models = env.GetValue("Model__size", 0)
    etmin_list = treat_float( env, 'Model__etmin' )
    etmax_list = treat_float( env, 'Model__etmax' )
    etamin_list = treat_float( env, 'Model__etamin' )
    etamax_list = treat_float( env, 'Model__etamax' )
    paths = treat_string( env, 'Model__path' )

    for idx, path in enumerate( paths ):
      path = path.replace('.onnx','')
      model = Model( basepath+'/'+path, etmin_list[idx], etmax_list[idx], etamin_list[idx], etamax_list[idx])
      self.__models.append(model)

    number_of_thresholds = env.GetValue("Threshold__size", 0)
    max_avgmu = treat_float( env, "Threshold__MaxAverageMu" )
    etmin_list = treat_float( env, 'Threshold__etmin' )
    etmax_list = treat_float( env, 'Threshold__etmax' )
    etamin_list = treat_float( env, 'Threshold__etamin' )
    etamax_list = treat_float( env, 'Threshold__etamax' )
    slopes = treat_float( env, 'Threshold__slope' )
    offsets = treat_float( env, 'Threshold__offset' )


    for idx, slope in enumerate(slopes):
      threshold = Threshold( slope, offsets[idx], etmin_list[idx], etmax_list[idx], etamin_list[idx],
                             etamax_list[idx], max_avgmu[idx] )
      self.__thresholds.append(threshold)

    MSG_INFO( self, "Tuning version: %s" , version )
    MSG_INFO( self, "Loaded %d models for inference." , number_of_models)
    MSG_INFO( self, "Loaded %d threshold for decision" , number_of_thresholds)


    return StatusCode.SUCCESS



  def accept( self, context):

    accept = Accept(self.name(), ['Pass', False])
    accept.setDecor( "discriminant",-999 )
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    eventInfo = context.getHandler( "EventInfoContainer" )
    avgmu = eventInfo.avgmu()

    eta = abs(fc.eta())
    if eta>2.5: eta=2.5
    et = fc.et()*1e-3 # in GeV

    # get the model for inference
    model = self.__getModel(et,eta)

    # If not fount, return false
    if not model:
      return accept


    # get the threshold
    threshold = self.__getThreshold( et, eta )

    # If not fount, return false
    if not threshold:
      return accept

    # Until here, we have all to run it!
    data = self.__generator( context )
    # compute the output
    if data:
      output = model.predict( data )
    else:
      return accept

    accept.setDecor("discriminant", output)

    # If the output is below of the cut, reprove it
    if output <= threshold(avgmu):
      return accept

    # If arrive until here, so the event was passed by the ringer
    accept.setCutResult( "Pass", True )
    return accept



  #
  # Get the corret model given all the phase spaces
  #
  def __getModel( self, et, eta ):
    model = None
    for obj in self.__models:
      if et > obj.etmin() and et <= obj.etmax():
        if eta > obj.etamin() and eta <= obj.etamax():
          model=obj; break
    return model


  #
  # Get the correct threshold given all phase spaces
  #
  def __getThreshold( self, et, eta ):
    threshold = None
    for obj in self.__thresholds:
      if et > obj.etmin() and et <= obj.etmax():
        if eta > obj.etamin() and eta <= obj.etamax():
          threshold=obj; break
    return threshold




