

__all__ =  [
              "install_commom_features_for_electron"
           ]



import numpy as np



def install_commom_features_for_electron():

  hypos = []

  # configure L1 items
  from kepler.emulator.TrigEgammaL1CaloHypoAlg import configure
  hypos = [
            configure("L1_EM3"     , "L1EM3"     ),
            configure("L1_EM7"     , "L1EM7"     ),
            configure("L1_EM15VH"  , "L1EM15VH"  ),
            configure("L1_EM15VHI" , "L1EM15VHI" ),
            configure("L1_EM20VH"  , "L1EM20VH"  ),
            configure("L1_EM20VHI" , "L1EM20VHI" ),
            configure("L1_EM22VH"  , "L1EM22VH"  ),
            configure("L1_EM22VHI" , "L1EM22VHI"  ),
            configure("L1_EM24VHI" , "L1EM24VHI"  ),
  ]


  # configure T2Calo for each ET bin used to emulated the HLT only
  from kepler.emulator.TrigEgammaFastCaloHypoAlg import configure
  for pidname in ['lhvloose', 'lhloose','lhmedium', 'lhtight']:

    # T2Calo
    hypos+= [
            configure('L2_%s_et0to12'  , 0  , pidname),
            configure('L2_%s_et0to12'  , 0  , pidname),
            configure('L2_%s_et0to12'  , 0  , pidname),
            configure('L2_%s_et0to12'  , 0  , pidname),
            configure('L2_%s_et12to20' , 12 , pidname),
            configure('L2_%s_et12to20' , 12 , pidname),
            configure('L2_%s_et12to20' , 12 , pidname),
            configure('L2_%s_et12to20' , 12 , pidname),
            configure('L2_%s_et22toInf', 22 , pidname),
            configure('L2_%s_et22toInf', 22 , pidname),
            configure('L2_%s_et22toInf', 22 , pidname),
            configure('L2_%s_et22toInf', 22 , pidname),
    ]

  # configure HLT LH decision
  from kepler.emulator.TrigEgammaPrecisionElectronHypoAlg import configure
  for pidname in ['lhvloose', 'lhloose','lhmedium', 'lhtight']:

    hypos+= [configure('HLT_%s'%pidname,  pidname)]

  # configure L2 electron decisions for each bin
  from kepler.emulator.TrigEgammaFastElectronHypoAlg import configure
  hypos += [
            configure('L2_el_pt0to15'   , 0 ),
            configure('L2_el_pt15to20'  , 15),
            configure('L2_el_pt20to50'  , 20),
            configure('L2_el_pt50toInf' , 50),
          ]

  # Add all hypos into the emulator
  attach(hypos)


  # configure T2Calo per ET (from cluster)
  #install_t2calo_for_electrons()

  # install ringer v6 version
  #install_Zee_ringer_v6()

  # install ringer v8 version
  #install_Zee_ringer_v8()









#
# Install T2Calo algorithm calculated for each event. Here, we select the bin given et from event
# For HLT chain, the t2calo configuration is given by the threshold of chain. Here, is given by et_cluster
#
def install_t2calo_for_electrons():

  from kepler.emulator.selector import TrigEgammaL2CaloSelectorTool
  hypos = [
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloTight"   , WPName ='lhtight'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloMedium"  , WPName ='lhmedium' ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloLoose"   , WPName ='lhloose'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloVLoose"  , WPName ='lhvloose' ) ,
    ]

  return attach(hypos)



def installTrigEgammaL2ElectronSelectors():

  from TrigEgammaEmulationTool import TrigEgammaL2ElectronSelectorTool
  hypos = [
        TrigEgammaL2ElectronSelectorTool("T0HLTElectronL2")
      ]
  return attach(hypos)





###########################################################
################## Official 2017 tuning ###################
###########################################################
def install_Zee_ringer_v6():

  from kepler.emulator.selector import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20170505_v6'

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

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20180125_v8'

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

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  #calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20210811_v9'
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20210306_v9'


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

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  #calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20210811_v10'
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20210306_v10'

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

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  #calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20210811_v11'
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee/TrigL2_20210306_v11'


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
def installElectronL2RingerSelector_v1_el():

  # Using shower shapes + rings here

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee_el/TrigL2_20210306_v1'


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
def installElectronL2RingerSelector_v2_el():

  # Using shower shapes + rings here

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zee_el/TrigL2_20210306_v2'

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



###########################################################
###################  ZRad v1 tuning   #####################
###########################################################
def installPhotonL2CaloRingerSelector_v1():
  '''
  This tuning is the very medium tuning which was adjusted to operate in the knee of the ROC curve given the best balance between PD and FR.
  '''
  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/zrad/TrigL2_20211102_v1'

  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    return [rings]

  hypos = [
              RingerSelectorTool( "T0HLTPhotonRingerTight_v1" ,getPatterns  , ConfigFile = calibpath+'/PhotonRingerTightTriggerConfig.conf' ),
              RingerSelectorTool( "T0HLTPhotonRingerMedium_v1",getPatterns  , ConfigFile = calibpath+'/PhotonRingerMediumTriggerConfig.conf'),
              RingerSelectorTool( "T0HLTPhotonRingerLoose_v1" ,getPatterns  , ConfigFile = calibpath+'/PhotonRingerLooseTriggerConfig.conf' ),
    ]

  return attach(hypos)





###########################################################
################### jpsiee v1 tuning  #####################
###########################################################
def installLowEnergyElectronL2CaloRingerSelector_v1():

  from TrigEgammaEmulationTool import RingerSelectorTool
  import os
  calibpath = os.environ['PRT_PATH'] + '/trigger/data/jpsi/TrigL2_20210227_v1'


  def getPatterns( context ):
    def norm1( data ):
      return (data/abs(sum(data))).reshape((1,100))
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    rings = norm1( fc.ringsE() )
    return [rings]


  hypos = [
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerTight_v1"    ,getPatterns, ConfigFile=calibpath+'/ElectronRingerTightTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerMedium_v1"   ,getPatterns, ConfigFile=calibpath+'/ElectronRingerMediumTriggerConfig.conf'   ),
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerLoose_v1"    ,getPatterns, ConfigFile=calibpath+'/ElectronRingerLooseTriggerConfig.conf'    ),
      RingerSelectorTool( "T0HLTLowEnergyElectronRingerVeryLoose_v1",getPatterns, ConfigFile=calibpath+'/ElectronRingerVeryLooseTriggerConfig.conf'),
    ]

  return attach(hypos)






