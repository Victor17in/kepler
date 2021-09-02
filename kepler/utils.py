

__all__ = ['get_bin_indexs', 'load_ringer_models']

import numpy as np
from tensorflow.keras.models import model_from_json


def get_bin_indexs(et,eta,etbins,etabins, logger=None):

  # Fix eta value if > 2.5
  if eta > etabins[-1]:  eta = etabins[-1]
  if et > etbins[-1]:  et = etbins[-1]
  ### Loop over binnings
  for etBinIdx in range(len(etbins)-1):
    if et >= etbins[etBinIdx] and  et < etbins[etBinIdx+1]:
      for etaBinIdx in range(len(etabins)-1):
        if eta >= etabins[etaBinIdx] and eta < etabins[etaBinIdx+1]:
          return etBinIdx, etaBinIdx
  return -1, -1#





#
# Load all ringer models from athena format
#
def load_ringer_models( configPath ):
    

    basepath = '/'.join(configPath.split('/')[:-1])
    from ROOT import TEnv
    env = TEnv( configPath )
    version = env.GetValue("__version__", '')

    def treat_float( env, key ):
      return [float(value) for value in  env.GetValue(key, '').split('; ')]

    def treat_string( env, key ):
      return [str(value) for value in  env.GetValue(key, '').split('; ')]

    #
    # Reading all models
    #
    number_of_models = env.GetValue("Model__size", 0)
    etmin_list = treat_float( env, 'Model__etmin' )
    etmax_list = treat_float( env, 'Model__etmax' )
    etamin_list = treat_float( env, 'Model__etamin' )
    etamax_list = treat_float( env, 'Model__etamax' )
    paths = treat_string( env, 'Model__path' )
    
    #
    # deserialize list to matrix
    #
    etbins = np.unique(etmin_list).tolist()
    etbins.append(etmax_list[-1])
    etabins = np.unique(etamin_list).tolist()
    etabins.append(etamax_list[-1])

    d = {
            'models' : [ [None for _ in range(len(etabins)-1)] for __ in range(len(etbins)-1) ],
            'model_etBins' : etbins, 
            'model_etaBins': etabins, 
        }

    etBinIdx=0
    etaBinIdx=0
    for idx, path in enumerate( paths ):
      if etaBinIdx > len(etabins)-2:
        etBinIdx +=1
        etaBinIdx = 0 
      path = basepath+'/'+path.replace('.onnx','')
      with open(path+'.json', 'r') as json_file:
          model = model_from_json(json_file.read())
          # load weights into new model
          model.load_weights(path+".h5")
          d['models'][etBinIdx][etaBinIdx] = model
      etaBinIdx+=1

    #
    # Reading all thresholds
    #  
   
    number_of_thresholds = env.GetValue("Threshold__size", 0)
    max_avgmu = treat_float( env, "Threshold__MaxAverageMu" )
    etmin_list = treat_float( env, 'Threshold__etmin' )
    etmax_list = treat_float( env, 'Threshold__etmax' )
    etamin_list = treat_float( env, 'Threshold__etamin' )
    etamax_list = treat_float( env, 'Threshold__etamax' )
    slopes = treat_float( env, 'Threshold__slope' )
    offsets = treat_float( env, 'Threshold__offset' )

    #
    # deserialize list to matrix
    #

    etbins = np.unique(etmin_list).tolist()
    etbins.append(etmax_list[-1])
    etabins = np.unique(etamin_list).tolist()
    etabins.append(etamax_list[-1])
    
    d['thresholds'] = [ [None for _ in range(len(etabins)-1)] for __ in range(len(etbins)-1) ]
    d['threshold_etBins'] = etbins
    d['threshold_etaBins'] = etabins
    
    etBinIdx=0
    etaBinIdx=0
    for idx, slope in enumerate(slopes):
      if etaBinIdx > len(etabins)-2:
        etBinIdx +=1
        etaBinIdx = 0 
      d['thresholds'][etBinIdx][etaBinIdx] = {'slope':slope, 'offset':offsets[idx] }
      etaBinIdx+=1

    return d, version
