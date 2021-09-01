#!/usr/bin/env python

from Gaugi.messenger import LoggingLevel
from Gaugi import ToolSvc

from kepler.core import ElectronLoop
from kepler.core.enumerators import Dataframe as DataframeEnum

import argparse
import sys,os

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

#
# job configuration
#

parser.add_argument('-i','--inputFiles', action='store',
    dest='inputFiles', required = True, nargs='+',
    help = "The input files.")

parser.add_argument('-o','--outputFile', action='store',
    dest='outputFile', required = False, default = None,
    help = "The output name.")

parser.add_argument('-n','--nov', action='store',
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

parser.add_argument('-p','--path', action='store',
    dest='path', required = False, default='*/HLT/Physval/Egamma/probes', type=str,
    help = "Ntuple base path.")

parser.add_argument('-l','--level', action='store',
    dest='level', required = False, type=str, default='INFO',
    help = "VERBOSE/INFO/DEBUG/WARNING/ERROR/FATAL")

parser.add_argument('--mute', action='store_true',
    dest='mute', required = False, 
    help = "Use this for production. quite output")

#
# event selection configuration
#

parser.add_argument('--et_bins', action='store',
    dest='et_bins', required = False, type=str, default='[15.0, 20.0, 30.0, 40.0, 50.0, 100000]',
    help = "et bin ranges")
    
parser.add_argument('--eta_bins', action='store',
    dest='eta_bins', required = False, type=str, default='[0.0, 0.8, 1.37, 1.54, 2.37, 2.50]',
    help = "eta bin ranges")

parser.add_argument('--pidname', action='store',
    dest='pidname', required = False, type=str, default='el_lhvloose',
    help = "Offline pid cut.") 

parser.add_argument('--et_min', action='store',
    dest='et_min', required = False, type=int, default=0,
    help = "Fast calo min et value in GeV.") 

parser.add_argument('--et_max', action='store',
    dest='et_max', required = False, type=int, default=1000,
    help = "Fast calo max et value in GeV") 

#parser.add_argument('--old_path', action='store_true',
#    dest='old_path', required = False, 
#    help = "Use 2017 physval ntuple path") 




if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = ElectronLoop(  "EventATLASLoop",
                     inputFiles = args.inputFiles,
                     treePath   = eval(args.path),
                     dataframe  = DataframeEnum.Electron_v1,
                     outputFile = args.outputFile,
                     level      = getattr(LoggingLevel, args.level),
                     mute_progressbar = args.mute,
                  )



#extra_keys+= install_Zee_ringer_v6()
#extra_keys+= install_Zee_ringer_v8()
from kepler.menu.install import install_commom_features_for_electron_dump
extra_features = install_commom_features_for_electron_dump() 


from kepler.dumper import ElectronDumper
etbins = [15,100]
etabins = [0,2.5]

from kepler.filter import Filter, SelectionType, EtCutType
filter = Filter("ElectronFilter")

filter.setCutValue(SelectionType.SelectionOnlineWithRings)
filter.setCutValue(EtCutType.OfflineAbove, 2) # this is default for now
filter.setCutValue( SelectionType.SelectionPID, eval(args.pidname) )
filter.setCutValue( EtCutType.L2CaloAbove, args.et_min )
filter.setCutValue( EtCutType.L2CaloBelow, args.et_max )

ToolSvc+=filter

output = args.outputFile.replace('.root','')

dumper = ElectronDumper("Dumper", output, eval(args.et_bins), eval(args.eta_bins), dumpRings=True)
dumper += extra_features
ToolSvc+=dumper

acc.run(args.nov)


