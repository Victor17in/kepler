

__all__ =  [
              "install_commom_features_for_electron_dump",
              "install_Zee_ringer_v6",
              "install_Zee_ringer_v8",
           ]



import numpy as np
from kepler.emulator import attach
import os



def install_commom_features_for_electron_dump():

  hypos = []

  # configure L1 items
  from kepler.emulator.TrigEgammaL1CaloHypoTool import configure
  hypos = [
            configure("L1_EM3"     , "L1_EM3"     ),
            configure("L1_EM7"     , "L1_EM7"     ),
            configure("L1_EM15VH"  , "L1_EM15VH"  ),
            configure("L1_EM15VHI" , "L1_EM15VHI" ),
            configure("L1_EM20VH"  , "L1_EM20VH"  ),
            configure("L1_EM20VHI" , "L1_EM20VHI" ),
            configure("L1_EM22VH"  , "L1_EM22VH"  ),
            configure("L1_EM22VHI" , "L1_EM22VHI"  ),
            configure("L1_EM24VHI" , "L1_EM24VHI"  ),
  ]


  # configure T2Calo for each ET bin used to emulated the HLT only
  from kepler.emulator.TrigEgammaFastCaloHypoTool import configure
  for pidname in ['lhvloose', 'lhloose','lhmedium', 'lhtight']:
    # T2Calo
    hypos+= [
            configure('trig_L2_cl_%s_et0to12'%pidname   , 0  , pidname),
            configure('trig_L2_cl_%s_et12to20'%pidname  , 12 , pidname),
            configure('trig_L2_cl_%s_et22toInf'%pidname , 22 , pidname),
    ]


  # configure L2 electron decisions for each bin
  from kepler.emulator.TrigEgammaFastElectronHypoTool import configure
  hypos += [
            configure('trig_L2_el_cut_pt0to15'   , 0 ),
            configure('trig_L2_el_cut_pt15to20'  , 15),
            configure('trig_L2_el_cut_pt20to50'  , 20),
            configure('trig_L2_el_cut_pt50toInf' , 50),
          ]


  return attach(hypos)










###########################################################
################## Official 2017 tuning ###################
###########################################################
def install_Zee_ringer_v6():

  from kepler.emulator import RingerSelectorTool
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20170505_v6'

  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    return [rings]

  hypos = [
      RingerSelectorTool("T0HLTElectronRingerTight_v6"    ,getPatterns,ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'    ),
      RingerSelectorTool("T0HLTElectronRingerMedium_v6"   ,getPatterns,ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'   ),
      RingerSelectorTool("T0HLTElectronRingerLoose_v6"    ,getPatterns,ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'    ),
      RingerSelectorTool("T0HLTElectronRingerVeryLoose_v6",getPatterns,ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf'),
    ]

  return attach(hypos)





###########################################################
################## Official 2018 tuning ###################
###########################################################
def install_Zee_ringer_v8():

  from kepler.emulator import RingerSelectorTool
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20180125_v8'

  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    return [rings]


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v8"    ,getPatterns, ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerMedium_v8"   ,getPatterns, ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTElectronRingerLoose_v8"    ,getPatterns, ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v8",getPatterns, ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ),
    ]

  return attach(hypos)


###########################################################
################## Testing 2020 tuning  ###################
###########################################################
def install_Zee_ringer_v9():

  # Using shower shapes + rings here

  from kepler.emulator import RingerSelectorTool
  import os
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20210306_v9'


  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    reta = fc.reta()
    eratio = fc.eratio()
    f1 = fc.f1()/0.6
    f3 = fc.f3()/0.04
    weta2 =fc.weta2()/0.02
    wstot = fc.wstot()
    if eratio>10.0:
      eratio = 0.0
    elif eratio>1.0:
      eratio=1.0
    if wstot<-99:
      wstot=0.0

    return [rings, np.array([[reta,eratio,f1,f3,weta2,wstot]])]


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v9"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerMedium_v9"   , getPatterns, ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTElectronRingerLoose_v9"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v9", getPatterns, ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ),
    ]

  return attach(hypos)



###########################################################
################## Testing 2020 tuning  ###################
###########################################################
def install_Zee_ringer_v10():

  from kepler.emulator import RingerSelectorTool
  import os
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20210306_v10'

  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    return [rings]


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v10"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'),
      RingerSelectorTool( "T0HLTElectronRingerMedium_v10"   , getPatterns, ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'),
      RingerSelectorTool( "T0HLTElectronRingerLoose_v10"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'),
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v10", getPatterns, ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf'),
    ]

  return attach(hypos)





###########################################################
################## Testing 2020 tuning  ###################
###########################################################
def install_Zee_ringer_v11():

  # Using shower shapes + rings here

  from kepler.emulator import RingerSelectorTool
  import os
  #calibpath = os.environ['RINGER_CALIBPATH'] + '/trigger/data/zee/TrigL2_20210811_v11'
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20210306_v11'


  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    reta = fc.reta()
    eratio = fc.eratio()
    f1 = fc.f1()/0.6
    f3 = fc.f3()/0.04
    weta2 =fc.weta2()/0.02
    wstot = fc.wstot()
    if eratio>10.0:
      eratio = 0.0
    elif eratio>1.0:
      eratio=1.0
    if wstot<-99:
      wstot=0.0

    return [rings, np.array([[reta,eratio,f1,f3,weta2,wstot]])]


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v11"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerMedium_v11"   , getPatterns, ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTElectronRingerLoose_v11"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v11", getPatterns, ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ),
    ]

  return attach(hypos)


###########################################################
################## Testing 2020 tuning  ###################
###########################################################
def install_Zee_ringer_v1_el():

  # Using shower shapes + rings here

  from kepler.emulator import RingerSelectorTool
  import os
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20210306_v1_el'


  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    reta = fc.reta()
    eratio = fc.eratio()
    f1 = fc.f1()/0.6
    f3 = fc.f3()/0.04
    weta2 =fc.weta2()/0.02
    wstot = fc.wstot()
    if eratio>10.0:
      eratio = 0.0
    elif eratio>1.0:
      eratio=1.0
    if wstot<-99:
      wstot=0.0

    el = context.getHandler("HLT__TrigElectronContainer" )
    # treat cases where we have container but it's empty. In this case, we are not be able to propagate.
    if el.size() == 0:
        return None

    el.setToBeClosestThanCluster()
    deta = el.trkClusDeta()
    dphi = el.trkClusDphi()
    etOverPt = el.etOverPt()

    return [rings, np.array([[reta,eratio,f1,f3,weta2,wstot]]), np.array([[etOverPt, deta, dphi]]) ]


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v1_el"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerMedium_v1_el"   , getPatterns, ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTElectronRingerLoose_v1_el"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v1_el", getPatterns, ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ),
    ]

  return attach(hypos)



###########################################################
################## Testing 2020 tuning  ###################
###########################################################
def install_Zee_ringer_v2_el():

  # Using shower shapes + rings here

  from kepler.emulator import RingerSelectorTool
  import os
  calibpath = os.environ['RINGER_CALIBPATH'] + '/data/electron/Zee/TrigL2_20210306_v2_el'

  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    reta = fc.reta()
    eratio = fc.eratio()
    f1 = fc.f1()/0.6
    f3 = fc.f3()/0.04
    weta2 =fc.weta2()/0.02
    wstot = fc.wstot()
    if eratio>10.0:
      eratio = 0.0
    elif eratio>1.0:
      eratio=1.0
    if wstot<-99:
      wstot=0.0

    el = context.getHandler("HLT__TrigElectronContainer" )

    # treat cases where we have container but it's empty. In this case, we are not be able to propagate.
    if el.size() == 0:
      return None

    el.setToBeClosestThanCluster()
    deta = el.trkClusDeta()
    dphi = el.trkClusDphi()
    etOverPt = el.etOverPt()

    return [rings, np.array([[reta,eratio,f1,f3,weta2,wstot]]), np.array([[etOverPt, deta, dphi]]) ]


  hypos = [
      RingerSelectorTool( "T0HLTElectronRingerTight_v2_el"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerTightTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerMedium_v2_el"   , getPatterns, ConfigFile = calibpath+'/ElectronRingerMediumTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTElectronRingerLoose_v2_el"    , getPatterns, ConfigFile = calibpath+'/ElectronRingerLooseTriggerConfig.conf'     ),
      RingerSelectorTool( "T0HLTElectronRingerVeryLoose_v2_el", getPatterns, ConfigFile = calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf' ),
    ]

  return attach(hypos)








