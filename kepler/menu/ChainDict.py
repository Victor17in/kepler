
__all__ = ["get_chain_dict", "treat_trigger_dict_type"]

from Gaugi import Logger
from Gaugi.messenger.macros import *


class ChainDict(Logger):


    __electronDict = {
                "signature"  : ['e'],
                "extra"      : ['ringer', 'noringer'],
                "pidname"    : [ 'tight','medium','loose','vloose',
                                 'lhtight','lhmedium','lhloose','lhvloose', 'etcut'],
                "iso"        : ['ivarloose', 'ivarmedium', 'ivartight', 'iloose', 
                                'icaloloose', 'icalomedium', 'icalotight' ],
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
    def __call__(self, trigger):

        d = {
            'signature' : '',
            'pidname'   : '',
            'iso'       : '',
            'extra'     : '',
            'L1Seed'    : '',
            'name'      : trigger,
        }


        #
        # HLT_e28_lhtight_nod0_noringer_ivarloose_L1EM22VHI
        #
        parts = self.__trigger.split('_')

        signature = parts[1][0]
        etthr = int(parts[1][0::])

        if signature == 'e':
            allow_values = self.__electronDict
        elif signatur == 'g':
            allow_values = self.__photonDict
        else:
            MSG_FATAL(self, 'Signature not supported: %s', signature)

        d['signature'] = signature

        pidname = parts[2]
        if pidname in allow_values['pidname']:
            d['pidname'] = pidname
        else:
            MSG_FATAL(self, "Pidname not supported: %s",pidname)
 
        # find isolation
        for key in allow_values['extra']:
            if key in self.__trigger:
                d['iso'] = key
                break

        for key in allow_values['extra']:
            if key in self.__trigger:
                d['extra'] = key
                break

        for key in allow_values['lhinfo']:
            if key in self.__trigger:
                d['info'] = key
                break
        
        l1seed = parts[-1]
        d['L1Seed'] = l1seed

        return d


get_chain_dict = ChainDict()



def treat_trigger_dict_type( d ):
    if type(d) is dict:
        return d
    else:
        return get_chain_dict(d)