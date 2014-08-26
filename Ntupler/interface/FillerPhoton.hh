#ifndef BACONPROD_NTUPLER_FILLERPHOTON_HH
#define BACONPROD_NTUPLER_FILLERPHOTON_HH

#include "BaconProd/Utils/interface/TriggerTools.hh"
#include <vector>
#include <string>

// forward class declarations
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
class TClonesArray;
class EcalClusterLazyTools;
namespace trigger {
  class TriggerEvent;
}


namespace baconhep
{
  class FillerPhoton
  {
    public:
      FillerPhoton(const edm::ParameterSet &iConfig);
      ~FillerPhoton();
      
      void fill(TClonesArray			            *array,	      // output array to be filled
                const edm::Event		            &iEvent,	      // event info
	        const edm::EventSetup		            &iSetup,	      // event setup info
                const reco::Vertex                          &pv,              // event primary vertex
		const std::vector<const reco::PFCandidate*> &pfNoPU,          // PFNoPU candidates
	        const std::vector<const reco::PFCandidate*> &pfPU,	      // PFPU candidates
	        const std::vector<TriggerRecord>            &triggerRecords,  // list of trigger names and objects
	        const trigger::TriggerEvent	            *triggerEvent);   // event trigger objects
            
      void computeIso(const reco::Photon &photon, const std::vector<const reco::PFCandidate*> &pfNoPU,
                      float &out_chHadIso, float &out_gammaIso, float &out_neuHadIso) const;
      
      float computeIsoForFSR(const reco::PFCandidate *photon,
                             const std::vector<const reco::PFCandidate*> &pfNoPU,
		             const std::vector<const reco::PFCandidate*> &pfPU) const;

      
      // Photon cuts
      double fMinPt;
      
      // EDM object collection names
      std::string fPhotonName;
      edm::InputTag fPFCandName;
      std::string fEleName;
      std::string fConvName;
      std::string fEBSCName;
      std::string fEESCName;
      std::string fEBRecHitName;
      std::string fEERecHitName;
  };
}
#endif
