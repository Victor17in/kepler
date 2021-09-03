
__all__ = ["get_chain_dict", "treat_trigger_dict_type"]

from Gaugi import Logger
from Gaugi.messenger.macros import *

from pprint import pprint

class ChainDict(Logger):


    __electronDict = {
                "signature"  : ['e'],
                "extra"      : ['ringer', 'noringer'],
                "pidname"    : [ 'tight','medium','loose','vloose',
                                 'lhtight','lhmedium','lhloose','lhvloose', 'etcut'],
                "iso"        : ['ivarloose', 'ivarmedium', 'ivartight', 'iloose', 
                                'icaloloose', 'icalomedium', 'icalotight' ],
                "lhinfo"     : ['nod0', 'nopix'],
                }

    __photonDict = {
                "signature"  : ['g'],
                "extra"      : [],
                "pidname"    : [ 'tight','medium','loose','vloose'],
                "iso"        : [],
                }



    def __init__(self):
        Logger.__init__(self)


    #
    # Get chain dict
    #
    def __call__(self, trigger, debug=False):

        d = {
            'signature' : '',
            'etthr'     : 0,
            'pidname'   : '',
            'iso'       : '',
            'extra'     : '',
            'L1Seed'    : '',
            'name'      : trigger,
        }


        #
        # HLT_e28_lhtight_nod0_noringer_ivarloose_L1EM22VHI
        #

        parts = trigger.replace('HLT_', '')
        parts = parts.split('_')

        signature = parts[0][0]
        etthr = int(parts[0][1::])

        d['etthr'] = etthr

        if signature == 'e':
            allow_values = self.__electronDict
        elif signatur == 'g':
            allow_values = self.__photonDict
        else:
            MSG_FATAL(self, 'Signature not supported: %s', signature)

        d['signature'] = signature

        pidname = parts[1]
        if pidname in allow_values['pidname']:
            d['pidname'] = pidname
        else:
            MSG_FATAL(self, "Pidname not supported: %s",pidname)
 
        # find isolation
        for key in allow_values['extra']:
            if key in trigger:
                d['iso'] = key
                break

        for key in allow_values['extra']:
            if key in trigger:
                d['extra'] = key
                break

        for key in allow_values['lhinfo']:
            if key in trigger:
                d['info'] = key
                break
        
        if 'L1EM' in trigger:
            l1seed = parts[-1]
            d['L1Seed'] = l1seed

        if debug:
            pprint(d)
        return d


get_chain_dict = ChainDict()



def treat_trigger_dict_type( d ):
    if type(d) is dict:
        return d
    else:
        return get_chain_dict(d)