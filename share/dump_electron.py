


from Gaugi.messenger import LoggingLevel, Logger
from Gaugi import ToolSvc, ToolMgr

from kepler.core import ElectronLoop
from kepler.core.enumerators import Dataframe as DataframeEnum

import argparse
import sys,os

mainLogger = Logger.getModuleLogger("job")
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
    dest='path', required = False, type=str, default='*/HLT/Egamma/Egamma/probes',
    help = "Ntuple base path.")

parser.add_argument('-l','--level', action='store',
    dest='level', required = False, type=str, default='INFO',
    help = "VERBOSE/INFO/DEBUG/WARNING/ERROR/FATAL")

#
# event selection configuration
#


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

# electron loop
acc = ElectronLoop(  "EventATLASLoop",
                     inputFiles = args.inputFiles,
                     treePath   = args.path,
                     dataframe  = DataframeEnum.Electron_v1,
                     outputFile = args.outputFile,
                     level      = getattr(LoggingLevel, args.level),
                  )

acc.run(args.nov)


