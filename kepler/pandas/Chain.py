
class Chain(Logger):

    def __init__(self, name, trigger, L1Seed = None ):

    
    def configure(self):

        d = get_chain_dict(self.trigger)





    def apply(self, df, col_name)


        df['L1Calo_'+col_name ] = False
        df['L2Calo_'+col_name ] = False
        df['L2_'+col_name ]     = False
        df['EFCalo_'+col_name ] = False
        df['HLT_'+col_name ]    = False

        # Filter by L1
        df_temp = df.loc[df[self.L1Item_column] == True]
        # store decisions
        df.at[df_temp.index, 'L1Calo_' + col_name] = True
        # drop reproved events
        df_temp = df_temp.loc[df_temp['L1Calo_'+col_name]==True]


        # Filter by L2Calo
        df_temp = df_temp.loc[ (df_temp['trig_L2_cl_et'] > self.l2calo_ethr * GeV) & (df_temp[self.l2calo_column] == True)]
        # store decisions
        df.at[df_temp.index, 'L2Calo_' + col_name] = True
        # drop reproved events
        df_temp = df_temp.loc[df_temp['L2Calo_'+col_name]==True]



