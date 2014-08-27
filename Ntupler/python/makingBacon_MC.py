import FWCore.ParameterSet.Config as cms

process = cms.Process('MakingBacon')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/GeometryDB_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load('TrackingTools/TransientTrack/TransientTrackBuilder_cfi')

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.GlobalTag.globaltag = 'START53_V7G::All'

process.load('CommonTools/ParticleFlow/PFBRECO_cff')
process.load('Dummy/Puppi/Puppi_cff')
process.load("RecoTauTag/Configuration/RecoPFTauTag_cff")

# import custom configurations
process.load('BaconProd/Ntupler/myJetExtras04_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras05_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras06_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras07_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras08_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras09_cff')    # include gen jets and b-tagging

process.load('BaconProd/Ntupler/myJetExtras04CHS_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras05CHS_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras06CHS_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras07CHS_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras08CHS_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras09CHS_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras12CHS_cff')    # include gen jets and b-tagging

process.load('BaconProd/Ntupler/myJetExtras04Puppi_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras05Puppi_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras06Puppi_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras07Puppi_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras08Puppi_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras09Puppi_cff')    # include gen jets and b-tagging
#process.load('BaconProd/Ntupler/myJetExtras12Puppi_cff')    # include gen jets and b-tagging

#process.load('BaconProd/Ntupler/myMETFilters_cff')        # apply MET filters set to tagging mode
#process.load('BaconProd/Ntupler/myMVAMet_cff')            # MVA MET
#process.load("BaconProd/Ntupler/myPFMETCorrections_cff")  # PF MET corrections
#process.pfJetMETcorr.jetCorrLabel = cms.string("ak5PFL1FastL2L3")

process.load('JetTools/AnalyzerToolbox/AnalyzerJetToolbox_cff')
from RecoMET.METProducers.PFMET_cfi import pfMet

# trigger filter
import os
cmssw_base = os.environ['CMSSW_BASE']
hlt_filename = "BaconAna/DataFormats/data/HLTFile_v0"
process.load('HLTrigger/HLTfilters/hltHighLevel_cfi')
process.hltHighLevel.throw = cms.bool(False)
process.hltHighLevel.HLTPaths = cms.vstring()
hlt_file = open(cmssw_base + "/src/" + hlt_filename, "r")
for line in hlt_file.readlines():
  line = line.strip()              # strip preceding and trailing whitespaces
  if (line[0:3] == 'HLT'):         # assumes typical lines begin with HLT path name (e.g. HLT_Mu15_v1)
    hlt_path = line.split()[0]
    process.hltHighLevel.HLTPaths.extend(cms.untracked.vstring(hlt_path))


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.source = cms.Source("PoolSource",
  fileNames  = cms.untracked.vstring('/store/results/b_tagging/StoreResults/QCD_Pt-300to470_Tune4C_13TeV_pythia8/USER/Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v1/00000/0044DCD0-BC1B-E411-9F97-003048FFCBFC.root')
)
process.source.inputCommands = cms.untracked.vstring("keep *",
                                                     "drop *_MEtoEDMConverter_*_*")

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True),
  Rethrow     = cms.untracked.vstring('ProductNotFound'),
  fileMode    = cms.untracked.string('NOMERGE')
)

is_data_flag = False
do_hlt_filter = False

process.pfMetPuppi = pfMet.clone();
process.pfMetPuppi.src = cms.InputTag('puppi','Puppi')
process.pfMetPuppi.calculateSignificance = False # this can't be easily implemented on packed PF candidates at the moment

# change jet inputs
# Select candidates that would pass CHS requirements
process.chs = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))
process.AK4GenJets.src = cms.InputTag('packedGenParticles')
process.AK4PFJets.src = cms.InputTag('packedPFCandidates')
process.AK4PFJetsCHS.src = cms.InputTag('chs')
process.AK4PFJetsPuppi.src = cms.InputTag('puppi','Puppi')
# process.AK8GenJets.src = cms.InputTag('packedGenCandidates')
# process.AK8PFJets.src = cms.InputTag('chs')
# process.AK8PFJetsCHS.src = cms.InputTag('chs')
# process.AK8PFJetsPuppi.src = cms.InputTag('puppi','Puppi');

process.ntupler = cms.EDAnalyzer('NtuplerMod',
  skipOnHLTFail = cms.untracked.bool(do_hlt_filter),
  outputName    = cms.untracked.string('baconTest.root'),
  TriggerFile   = cms.untracked.string(hlt_filename),
  edmPVName     = cms.untracked.string('offlineSlimmedPrimaryVertices'),
  edmPFCandName = cms.untracked.string('packedPFCandidates'),
  
  Info = cms.untracked.PSet(
    isActive             = cms.untracked.bool(True),
    edmPFCandName        = cms.untracked.string('packedPFCandidates'),
    edmPileupInfoName    = cms.untracked.string('addPileupInfo'),
    edmBeamspotName      = cms.untracked.string('offlineBeamSpot'),
    edmPFMETName         = cms.untracked.string('slimmedMETs'),
    edmPFMETCorrName     = cms.untracked.string('pfType0p1CorrectedMet'),
    edmMVAMETName        = cms.untracked.string('pfMEtMVA'),
    edmMVAMETUnityName   = cms.untracked.string('pfMEtMVAUnity'),
    edmMVAMETNoSmearName = cms.untracked.string('pfMEtMVANoSmear'),
    edmPuppETName        = cms.untracked.string('pfMetPuppi'),
    edmRhoForIsoName     = cms.untracked.string('fixedGridRhoAll'),
    edmRhoForJetEnergy   = cms.untracked.string('fixedGridRhoAll'),
    doFillMET            = cms.untracked.bool(True),
    doFillMETFilters     = cms.untracked.bool(False)
  ),
  
  GenInfo = cms.untracked.PSet(
    isActive            = ( cms.untracked.bool(False) if is_data_flag else cms.untracked.bool(True) ),
    edmGenEventInfoName = cms.untracked.string('generator'),
    edmGenParticlesName = cms.untracked.string('prunedGenParticles'),
    fillAllGen          = cms.untracked.bool(False)
  ),
  
  PV = cms.untracked.PSet(
    isActive      = cms.untracked.bool(True),   
    edmName       = cms.untracked.string('offlineSlimmedPrimaryVertices'),
    minNTracksFit = cms.untracked.uint32(0),
    minNdof       = cms.untracked.double(4),
    maxAbsZ       = cms.untracked.double(24),
    maxRho        = cms.untracked.double(2)
  ),
  
  Electron = cms.untracked.PSet(
    isActive                  = cms.untracked.bool(False)
  ),
  
  Muon = cms.untracked.PSet(
    isActive      = cms.untracked.bool(False)
  ),
  
  Photon = cms.untracked.PSet(
    isActive              = cms.untracked.bool(False),
    minPt                 = cms.untracked.double(0),
    edmName               = cms.untracked.string('photons'),
    edmPFCandName         = cms.untracked.string('particleFlow'),
    edmElectronName       = cms.untracked.string('gsfElectrons'),
    edmConversionName     = cms.untracked.string('allConversions'),
    edmEBSuperClusterName = cms.untracked.string('correctedHybridSuperClusters'),
    edmEESuperClusterName = cms.untracked.string('correctedMulti5x5SuperClustersWithPreshower'),
    edmEBRecHitName       = cms.untracked.string('reducedEcalRecHitsEB'),
    edmEERecHitName       = cms.untracked.string('reducedEcalRecHitsEE'),
    edmRhoForEnergyRegression = cms.untracked.string('kt6PFJets'),
    edmPVName                 = cms.untracked.string('offlinePrimaryVertices')
  ),
  
  Tau = cms.untracked.PSet(
    isActive = cms.untracked.bool(False),
    minPt    = cms.untracked.double(15),
    edmName  = cms.untracked.string('hpsPFTauProducer'),
    ringIsoFile      = cms.untracked.string('BaconProd/Utils/data/gbrfTauIso_apr29a.root'),
    ringIso2File     = cms.untracked.string('BaconProd/Utils/data/gbrfTauIso_v2.root'),
    edmRhoForRingIso = cms.untracked.string('kt6PFJets')
  ),
  
  Jet = cms.untracked.PSet(
    isActive             = cms.untracked.bool(True),
    minPt                = cms.untracked.double(20),
    doComputeFullJetInfo = cms.untracked.bool(True),
    doGenJet             = ( cms.untracked.bool(False) if is_data_flag else cms.untracked.bool(True) ),
    
    coneSizes = cms.untracked.vdouble(0.4),#,0.8,1.2),
    postFix   = cms.untracked.vstring("","CHS","Puppi"),
    
    edmPVName = cms.untracked.string('offlineSlimmedPrimaryVertices'),
    
    # ORDERED lists of jet energy correction input files
    jecFiles = ( cms.untracked.vstring('BaconProd/Utils/data/Summer13_V1_DATA_L1FastJet_AK5PF.txt',
                                       'BaconProd/Utils/data/Summer13_V1_DATA_L2Relative_AK5PF.txt',
				       'BaconProd/Utils/data/Summer13_V1_DATA_L3Absolute_AK5PF.txt',
				       'BaconProd/Utils/data/Summer13_V1_DATA_L2L3Residual_AK5PF.txt')
                 if is_data_flag else 
                 cms.untracked.vstring('BaconProd/Utils/data/Summer13_V1_MC_L1FastJet_AK5PF.txt',
                                       'BaconProd/Utils/data/Summer13_V1_MC_L2Relative_AK5PF.txt',
				       'BaconProd/Utils/data/Summer13_V1_MC_L3Absolute_AK5PF.txt')
	       ),
    jecUncFiles = ( cms.untracked.vstring('BaconProd/Utils/data/Summer13_V1_DATA_Uncertainty_AK5PF.txt')
                    if is_data_flag else
                    cms.untracked.vstring('BaconProd/Utils/data/Summer13_V1_MC_Uncertainty_AK5PF.txt')
                  ),
    jecFilesForID = ( cms.untracked.vstring('BaconProd/Utils/data/FT_53_V21_AN3_L1FastJet_AK5PF.txt',
                                            'BaconProd/Utils/data/FT_53_V21_AN3_L2Relative_AK5PF.txt',
				            'BaconProd/Utils/data/FT_53_V21_AN3_L3Absolute_AK5PF.txt',
					    'BaconProd/Utils/data/FT_53_V21_AN3_L2L3Residual_AK5PF.txt')
                      if is_data_flag else
                      cms.untracked.vstring('BaconProd/Utils/data/START53_V15_L1FastJet_AK5PF.txt',
                                            'BaconProd/Utils/data/START53_V15_L2Relative_AK5PF.txt',
				            'BaconProd/Utils/data/START53_V15_L3Absolute_AK5PF.txt')
		    ),
    edmRhoName = cms.untracked.string('fixedGridRhoAll'),
    
    # ORDERD list of pileup jet ID input files
    jetPUIDFiles = cms.untracked.vstring('',
                                         'BaconProd/Utils/data/TMVAClassificationCategory_JetID_53X_Dec2012.weights.xml'),
    
    # names of various jet-related collections WITHOUT prefix (e.g. 'PFJets' instead of 'AK5PFJets')
    # prefix string will be determined by ntupler module based on cone size
    jetName            = cms.untracked.string('PFJets'),
    genJetName         = cms.untracked.string('GenJets'),
    jetFlavorName      = cms.untracked.string('byValAlgo'),
    jetFlavorPhysName  = cms.untracked.string('byValPhys'),
    pruneJetName       = cms.untracked.string('caPFJetsPruned'),
    subJetName         = cms.untracked.string('caPFJetsPruned'),
    csvBTagName        = cms.untracked.string('jetCombinedSecondaryVertexBJetTags'),
    csvBTagSubJetName  = cms.untracked.string('jetCombinedSecondaryVertexBJetTagsSJ'),
    jettiness          = cms.untracked.string('Njettiness'),
    qgLikelihood       = cms.untracked.string('QGTagger'),
    qgLikelihoodSubjet = cms.untracked.string('QGTaggerSubJets')
  ),
  
  PFCand = cms.untracked.PSet(
    isActive       = cms.untracked.bool(False),
    edmName        = cms.untracked.string('particleFlow'),
    edmPVName      = cms.untracked.string('offlinePrimaryVertices'),
    doAddDepthTime = cms.untracked.bool(False)
  )
)

process.baconSequence = cms.Sequence(#process.PFBRECO*
                                     process.chs*
                                     process.puppi*
                                     #process.metFilters*
                                     #process.producePFMETCorrections*
                                     #process.recojetsequence*
                                     #process.genjetsequence*
                                     process.AK4genjetsequence*
                                     process.AK4jetsequence*
                                     process.AK4jetsequenceCHS*
                                     process.AK4jetsequencePuppi*
                                     #process.recoTau*   ### must come after antiktGenJets otherwise conflict on RecoJets/JetProducers/plugins
				     #process.MVAMetSeq*
             process.pfMetPuppi*
				     process.ntupler)
				     
if do_hlt_filter:
  process.p = cms.Path(process.hltHighLevel*process.baconSequence)
else:
  process.p = cms.Path(process.baconSequence)

#process.output = cms.OutputModule("PoolOutputModule",                                                                                                                                                     
#                                  outputCommands = cms.untracked.vstring('keep *'),                                                                                                                      
#                                  fileName       = cms.untracked.string ("BBB")                                                                                                                    
#)

# schedule definition                                                                                                       
#process.outpath  = cms.EndPath(process.output)                                                                                                                                                

#
# simple checks to catch some mistakes...
#
if is_data_flag:
  assert process.ntupler.GenInfo.isActive == cms.untracked.bool(False)
  # assert process.ntupler.Electron.isData == cms.untracked.bool(True)
  # assert process.ntupler.Muon.isData == cms.untracked.bool(True)
  assert process.ntupler.Jet.doGenJet == cms.untracked.bool(False)
# else:
#   assert process.ntupler.Electron.isData == cms.untracked.bool(False)
#   assert process.ntupler.Muon.isData == cms.untracked.bool(False)
