
__all__ = ["Photon_v1"]

def Photon_v1():

  code = """
	namespace edm{

	struct Photon_v1{

	    /* Branch variables */
	    uint32_t            RunNumber{};
	    unsigned long long  EventNumber{};
	    float               avgmu{};
	    float               LumiBlock{};

	    /* Egamma */

	    bool                ph_hasCalo   ;
	    bool                ph_hasTrack  ;
	    float               ph_e;
	    float               ph_et;
	    float               ph_eta;
	    float               ph_phi;
	    float               ph_ethad1;
	    float               ph_ehad1;
	    float               ph_f1;
	    float               ph_f3;
	    float               ph_f1core;
	    float               ph_f3core;
	    float               ph_weta1;
	    float               ph_weta2;
	    float               ph_wtots1;
	    float               ph_fracs1;
	    float               ph_Reta;
	    float               ph_Rphi;
	    float               ph_Eratio;
	    float               ph_Rhad;
	    float               ph_Rhad1;
	    float               ph_deta1;
	    float               ph_deta2;
	    float               ph_dphi2;
	    float               ph_dphiresc;
	    float               ph_deltaPhiRescaled2;
	    float               ph_deltaEta1;
	    float               ph_deltaE;
	    float               ph_e277;
	    std::vector<float> *ph_etCone;
	    std::vector<float> *ph_ptCone;
	    
	    bool                ph_loose{};
	    bool                ph_medium{};
	    bool                ph_tight{};
	    bool                ph_lhvloose{};
	    bool                ph_lhloose{};
	    bool                ph_lhmedium{};
	    bool                ph_lhtight{};
	    bool                ph_multiLepton{};
	    std::vector<float> *ph_ringsE;
	    int                 ph_nGoodVtx{};
	    int                 ph_nPileupPrimaryVtx{};
	    ///Egamma Calo
	    float               ph_calo_et{};
	    float               ph_calo_eta{};
	    float               ph_calo_phi{};
	    float               ph_calo_etaBE2{};
	    float               ph_calo_e{};
	    // Level 1
	    float               trig_L1_eta{};
	    float               trig_L1_phi{};
	    float               trig_L1_emClus{};
	    float               trig_L1_tauClus{};
	    float               trig_L1_emIsol{};
	    float               trig_L1_hadIsol{};
	    float               trig_L1_hadCore{};

	    // Level 2 Calo
	    float               trig_L2_calo_et{};
	    float               trig_L2_calo_eta{};
	    float               trig_L2_calo_phi{};
	    float               trig_L2_calo_e237{}; 
	    float               trig_L2_calo_e277{}; 
	    float               trig_L2_calo_fracs1{}; 
	    float               trig_L2_calo_weta2{}; 
	    float               trig_L2_calo_ehad1{}; 
	    float               trig_L2_calo_emaxs1{};
	    float               trig_L2_calo_e2tsts1{};
	    float               trig_L2_calo_wstot{}; 
	    std::vector<float> *trig_L2_calo_energySample; 
	    std::vector<float> *trig_L2_calo_rings;
	    std::vector<float> *trig_L2_calo_rnnOutput;
	    // level 2 id
	    std::vector<float> *trig_L2_ph_pt;
	    std::vector<float> *trig_L2_ph_caloEta;
	    std::vector<float> *trig_L2_ph_eta;
	    std::vector<float> *trig_L2_ph_phi;
	    std::vector<float> *trig_L2_ph_nTRTHits;
	    std::vector<float> *trig_L2_ph_nTRTHiThresholdHits;

	    // EFCalo and HLT steps

	    std::vector<float>               *trig_EF_calo_e;
	    std::vector<float>               *trig_EF_calo_et;
	    std::vector<float>               *trig_EF_calo_eta;
	    std::vector<float>               *trig_EF_calo_phi;
	    std::vector<float>               *trig_EF_calo_etaBE2;

	    std::vector<float>               *trig_EF_ph_calo_e;
	    std::vector<float>               *trig_EF_ph_calo_et;
	    std::vector<float>               *trig_EF_ph_calo_eta;
	    std::vector<float>               *trig_EF_ph_calo_phi;
	    std::vector<float>               *trig_EF_ph_calo_etaBE2;

	    std::vector<float>               *trig_EF_ph_e;
	    std::vector<float>               *trig_EF_ph_et;
	    std::vector<float>               *trig_EF_ph_eta;
	    std::vector<float>               *trig_EF_ph_phi;
	    std::vector<float>               *trig_EF_ph_ethad1;
	    std::vector<float>               *trig_EF_ph_ehad1;
	    std::vector<float>               *trig_EF_ph_f1;
	    std::vector<float>               *trig_EF_ph_f3;
	    std::vector<float>               *trig_EF_ph_f1core;
	    std::vector<float>               *trig_EF_ph_f3core;
	    std::vector<float>               *trig_EF_ph_weta1;
	    std::vector<float>               *trig_EF_ph_weta2;
	    std::vector<float>               *trig_EF_ph_wtots1;
	    std::vector<float>               *trig_EF_ph_fracs1;
	    std::vector<float>               *trig_EF_ph_Reta;
	    std::vector<float>               *trig_EF_ph_Rphi;
	    std::vector<float>               *trig_EF_ph_Eratio;
	    std::vector<float>               *trig_EF_ph_Rhad;
	    std::vector<float>               *trig_EF_ph_Rhad1;
	    std::vector<float>               *trig_EF_ph_deta2;
	    std::vector<float>               *trig_EF_ph_dphi2;
	    std::vector<float>               *trig_EF_ph_dphiresc;
	    std::vector<float>               *trig_EF_ph_e277;
	    std::vector<float>               *trig_EF_ph_deltaPhiRescaled2;
	    std::vector<float>               *trig_EF_ph_deltaEta1;
	    std::vector<float>               *trig_EF_ph_deltaE;
	    std::vector<float>               *trig_EF_ph_etCone;
	    std::vector<float>               *trig_EF_ph_ptCone;


	    std::vector<bool>                *trig_EF_ph_hasCalo   ;
	    std::vector<bool>                *trig_EF_ph_hasTrack  ;



	    std::vector<bool>                *trig_EF_ph_loose;
	    std::vector<bool>                *trig_EF_ph_medium;
	    std::vector<bool>                *trig_EF_ph_tight;
	    std::vector<bool>                *trig_EF_ph_lhvloose;
	    std::vector<bool>                *trig_EF_ph_lhloose;
	    std::vector<bool>                *trig_EF_ph_lhmedium;
	    std::vector<bool>                *trig_EF_ph_lhtight;
	    std::vector<bool>                *trig_EF_calo_loose;
	    std::vector<bool>                *trig_EF_calo_medium;
	    std::vector<bool>                *trig_EF_calo_tight;
	    std::vector<bool>                *trig_EF_calo_lhvloose;
	    std::vector<bool>                *trig_EF_calo_lhloose;
	    std::vector<bool>                *trig_EF_calo_lhmedium;
	    std::vector<bool>                *trig_EF_calo_lhtight;

	    std::vector<int>                 *trig_tdt_L1_calo_accept;
	    std::vector<int>                 *trig_tdt_L2_calo_accept;
	    std::vector<int>                 *trig_tdt_L2_ph_accept  ;
	    std::vector<int>                 *trig_tdt_EF_calo_accept;
	    std::vector<int>                 *trig_tdt_EF_ph_accept  ;
	    std::vector<int>                 *trig_tdt_emu_L1_calo_accept;
	    std::vector<int>                 *trig_tdt_emu_L2_calo_accept;
	    std::vector<int>                 *trig_tdt_emu_L2_ph_accept  ;
	    std::vector<int>                 *trig_tdt_emu_EF_calo_accept;
	    std::vector<int>                 *trig_tdt_emu_EF_ph_accept  ;



	    // Monte Carlo
	    bool                mc_hasMC{}     ;
	    float               mc_pt{}        ;
	    float               mc_eta{}       ;
	    float               mc_phi{}       ;
	    bool                mc_isTop{}     ;
	    bool                mc_isParton{}  ;
	    bool                mc_isMeson{}   ;
	    bool                mc_isQuark{}   ;
	    bool                mc_isTau{}     ;
	    bool                mc_isMuon{}    ;
	    bool                mc_isPhoton{}  ;
	    bool                mc_isElectron{};

	    int                 mc_type{};
	    int                 mc_origin{};
	    bool                mc_isTruthElectronFromZ{};
	    bool                mc_isTruthElectronFromW{};
	    bool                mc_isTruthElectronFromJpsi{};
	    bool                mc_isTruthElectronAny{};
	    bool                mc_isTruthJetFromAny{};
	    bool                mc_isTruthPhotonFromAny{};


	};
	}
	"""

  import ROOT
  ROOT.gInterpreter.ProcessLine(code)

  from ROOT import edm
  return edm.Photon_v1()

