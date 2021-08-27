


__all__ = []

from Gaugi import StatusCode, NotSet, retrieve_kw, progressbar
from Gaugi import csvStr2List, expandFolders, save, load
from Gaugi.messenger.macros import *
from Gaugi.messenger  import Logger
from Gaugi.constants import GeV
from Gaugi import EnumStringification
import numpy as np
import pandas as pd


class ReaderPool( Logger ):

  def __init__(self, fList, reader, nFilesPerJob, nthreads):

    Logger.__init__(self)
    from Gaugi import csvStr2List
    from Gaugi import expandFolders
    fList = csvStr2List ( fList )
    self._fList = expandFolders( fList )
    def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
        yield l[i:i + n]
    self._fList = [l for l in chunks(self._fList, nFilesPerJob)]
    self.process_pipe = []
    self._outputs = []
    self._nthreads = nthreads
    self._reader = reader

  def __call__( self ):
    from Gaugi import SafeProcess
    while len(self._fList) > 0:
      if len(self.process_pipe) < self._nthreads:
        job_id = len(self._fList)
        f = self._fList.pop()
        proc = SafeProcess( self._reader , job_id)
        proc(f)
        self.process_pipe.append( (job_id, proc) )

      for proc in self.process_pipe:
        if not proc[1].is_alive():
          MSG_INFO( self,  ('pop process id (%d) from the stack')%(proc[0]) )
          self._outputs.append( proc[1].get( None ))
          self.process_pipe.remove(proc)

    # Check pipe process
    # Protection for the last jobs
    while len(self.process_pipe)>0:
      for proc in self.process_pipe:
        if not proc[1].is_alive():
          MSG_INFO( self,  ('pop process id (%d) from the stack')%(proc[0]) )
          self._outputs.append( proc[1].get( None  ))
          self.process_pipe.remove(proc)

    return self._outputs



class DataReader( Logger ):

  def __init__( self, skip_these_keys,**kw ):
    Logger.__init__(self, kw)
    self._skip_these_keys = skip_these_keys


  def __call__(self, inputFiles  ):
    obj  =None
    for idx, f in progressbar(enumerate(inputFiles), len(inputFiles), 'Reading...: ', 60,  logger = self._logger):
      #d = dict(np.load(f,allow_pickle=True))
      d = dict(load(f))
      obj = self.merge(d,obj,self._skip_these_keys) if obj else d
    return obj


  @classmethod
  def merge( cls, from_dict, to_dict, skip_these_keys ):
    for key in from_dict.keys():
      if cls.skip_key(key, skip_these_keys):  continue
      if to_dict[key] is not None:
        to_dict[key] = np.concatenate( (to_dict[key], from_dict[key]) )
      else:
        to_dict[key] = from_dict[key]
    return to_dict

  @classmethod
  def skip_key( cls, key, skip_these_keys ):
    for skip_this_key in skip_these_keys:
      if skip_this_key in key:
        return True
    return False






class Merger(Logger):

  def __init__( self, nthreads, **kw ):
    Logger.__init__(self, **kw)
    self._nthreads = nthreads
    self._nFilesPerJob = 20
    self._skip_these_keys = ["features", "etBins", "etaBins", "etBinIdx","etaBinIdx"]
    import re
    self._pat = re.compile(r'.+(?P<binID>et(?P<etBinIdx>\d+).eta(?P<etaBinIdx>\d+))\..+$')


  def __call__( self, sgnFileList, bkgFileList, ofile, dump_csv=False):

    # get all keys
    paths = expandFolders(sgnFileList)
    jobIDs = sorted(list(set([self._pat.match(f).group('binID')  for f in paths if self._pat.match(f) is not None])))
    npatterns = {}
    etBins = None; etaBins = None

    debug=False

    for id in jobIDs:

      sgnSubFileList = []
      for f in expandFolders(sgnFileList):
        if id in f:  sgnSubFileList.append(f)

      if debug:
        sgnSubFileList=sgnSubFileList[0:11]

      reader = ReaderPool( sgnSubFileList, DataReader(self._skip_these_keys), self._nFilesPerJob, self._nthreads )
      MSG_INFO( self, "Reading signal files..." )
      outputs = reader()
      sgnDict = outputs.pop()
      if len(outputs)>0:
        for from_dict in progressbar(outputs, len(outputs), 'Mearging signal files: ', 60,  logger = self._logger):
          DataReader.merge( from_dict, sgnDict, self._skip_these_keys )

      bkgSubFileList = []
      for f in expandFolders(bkgFileList):
        if id in f:  bkgSubFileList.append(f)


      if debug:
        bkgSubFileList=bkgSubFileList[0:11]


      reader = ReaderPool( bkgSubFileList, DataReader(self._skip_these_keys), self._nFilesPerJob, self._nthreads )
      MSG_INFO( self, "Reading background files..." )
      outputs = reader()
      bkgDict = outputs.pop()
      if len(outputs)>0:
        for from_dict in progressbar(outputs, len(outputs), 'Mearging background files: ', 60,  logger = self._logger):
          DataReader.merge( from_dict, bkgDict, self._skip_these_keys )


      # Loop over regions
      d = { "features"  : sgnDict["features"],
            "etBins"    : sgnDict["etBins"],
            "etaBins"   : sgnDict["etaBins"],
            "etBinIdx"  : sgnDict["etBinIdx"],
            "etaBinIdx" : sgnDict["etaBinIdx"],
            }

      #if not etBins:  etBins = sgnDict["etBins"]
      etBins = sgnDict["etBins"]
      #if not etaBins:  etaBins = sgnDict["etaBins"]
      etaBins = sgnDict["etaBins"]

      d['data'] = np.concatenate( (sgnDict['pattern_'+id], bkgDict['pattern_'+id]) ).astype('float32')
      d['target'] = np.concatenate( ( np.ones( (sgnDict['pattern_'+id].shape[0],) ),  np.zeros( (bkgDict['pattern_'+id].shape[0],) ) ) ).astype('int16')

      if sgnDict['pattern_'+id] is not None:
        MSG_INFO(self, 'sgnData_%s : (%d, %d)', id, sgnDict['pattern_'+id].shape[0], sgnDict['pattern_'+id].shape[1])
      else:
        MSG_INFO(self, 'sgnData_%s : empty', id)
      if bkgDict['pattern_'+id] is not None:
        MSG_INFO(self, 'bkgData_%s : (%d, %d)', id, bkgDict['pattern_'+id].shape[0], bkgDict['pattern_'+id].shape[1])
      else:
        MSG_INFO(self, 'bkgData_%s : empty', id)
      MSG_INFO( self, "Saving: %s", ofile+'_'+id)

      npatterns['sgnPattern_'+id] = int(sgnDict['pattern_'+id].shape[0])
      npatterns['bkgPattern_'+id] = int(bkgDict['pattern_'+id].shape[0])
      save( d, ofile+'_'+id , protocol = 'savez_compressed')

      if dump_csv:
        # Save as csv for pandas
        dd = {}
        for ikey, key in enumerate(d['features']):
          dd[key] = d['data'][:,ikey]
        dd['target'] = d['target']
        df = pd.DataFrame( dd )
        df.to_csv(ofile+'_'+id+'.csv')


    self.plotNSamples( npatterns, etBins, etaBins )



  @classmethod
  def plotNSamples(cls, npatterns, etBins, etaBins, outname='nPatterns.pdf' ):
    """Plot number of samples per bin"""
    logger = Logger.getModuleLogger("PlotNSamples" )
    from ROOT import TCanvas, gROOT, kTRUE, kFALSE, TH2I, TText
    gROOT.SetBatch(kTRUE)
    c1 = TCanvas("plot_patterns_signal", "a",0,0,800,400); c1.Draw();
    shape = [len(etBins)-1, len(etaBins)-1]
    histo1 = TH2I("text_stats", "#color[4]{Signal}/#color[2]{Background} available statistics", shape[0], 0, shape[0], shape[1], 0, shape[1])
    #histo1 = TH2I("text_stats", "Signal/Background available statistics", shape[0], 0, shape[0], shape[1], 0, shape[1])
    histo1.SetStats(kFALSE)
    histo1.Draw("TEXT")
    histo1.SetXTitle("E_{T}"); histo1.SetYTitle("#eta")
    histo1.GetXaxis().SetTitleSize(0.04); histo1.GetYaxis().SetTitleSize(0.04)
    histo1.GetXaxis().SetLabelSize(0.04); histo1.GetYaxis().SetLabelSize(0.04);
    histo1.GetXaxis().SetTickSize(0); histo1.GetYaxis().SetTickSize(0);
    ttest = TText(); ttest.SetTextAlign(22)
    for etBin in range(shape[0]):
      for etaBin in range(shape[1]):
        key = 'et%d_eta%d'%(etBin,etaBin)
        ttest.SetTextColor(4)
        ttest.DrawText( .5 + etBin, .75 + etaBin, 's: ' + str(npatterns['sgnPattern_'+key]) )

        ttest.SetTextColor(2)
        ttest.DrawText( .5 + etBin, .25 + etaBin, 'b: ' + str(npatterns['bkgPattern_'+key]) )

        try:
          histo1.GetYaxis().SetBinLabel(etaBin+1, '#bf{%d} : %.2f->%.2f' % ( etaBin, etaBins[etaBin], etaBins[etaBin + 1] ) )
        except Exception:
          logger.error("Couldn't retrieve eta bin %d bounderies.", etaBin)
          histo1.GetYaxis().SetBinLabel(etaBin+1, str(etaBin))
        try:
          histo1.GetXaxis().SetBinLabel(etBin+1, '#bf{%d} : %d->%d [GeV]' % ( etBin, etBins[etBin], etBins[etBin + 1] ) )
        except Exception:
          logger.error("Couldn't retrieve et bin %d bounderies.", etBin)
          histo1.GetXaxis().SetBinLabel(etBin+1, str(etaBin))
    c1.SetGrid()
    c1.Update()
    c1.SaveAs(outname)





