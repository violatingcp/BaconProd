import FWCore.ParameterSet.Config as cms
#from RecoJets.Configuration.GenJetParticles_cff import *
from RecoJets.JetProducers.ak5PFJets_cfi        import ak5PFJets
from RecoJets.JetProducers.ak5PFJetsPruned_cfi  import ak5PFJetsPruned

#for each jet collection run Pruning, subjet b-tagging, quark gluon discrimination,n-subjettiness and subjet quark gluon discrimination
AK5PFJetsCHS = ak5PFJets.clone(
    src      = cms.InputTag('PFBRECO','pfNoElectron'),
    rParam   = cms.double(0.4),
    jetPtMin = cms.double(20)
    )

AK5caPFJetsPrunedCHS = ak5PFJetsPruned.clone(
    src      = cms.InputTag('PFBRECO','pfNoElectron'),
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.4),
    doAreaFastjet = cms.bool(False),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets"),
    jetPtMin = cms.double(20)
    )

from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import ic5JetTracksAssociatorAtVertex
AK5jetTracksAssociatorAtVertexCHS          = ic5JetTracksAssociatorAtVertex.clone()
AK5jetTracksAssociatorAtVertexCHS  .jets   = cms.InputTag('AK5PFJetsCHS')
AK5jetTracksAssociatorAtVertexCHS  .tracks = "generalTracks"

AK5jetTracksAssociatorAtVertexSJCHS        = ic5JetTracksAssociatorAtVertex.clone()
AK5jetTracksAssociatorAtVertexSJCHS.jets   = cms.InputTag('AK5caPFJetsPrunedCHS','SubJets')
AK5jetTracksAssociatorAtVertexSJCHS.tracks = "generalTracks"

from RecoBTag.Configuration.RecoBTag_cff import *
AK5jetImpactParameterTagInfosCHS                      = impactParameterTagInfos.clone()
AK5jetImpactParameterTagInfosCHS.jetTracks            = "AK5jetTracksAssociatorAtVertexCHS"
AK5jetSecondaryVertexTagInfosCHS                      = secondaryVertexTagInfos.clone()
AK5jetSecondaryVertexTagInfosCHS.trackIPTagInfos      = "AK5jetImpactParameterTagInfosCHS"
AK5jetCombinedSecondaryVertexBJetTagsCHS           = combinedSecondaryVertexBJetTags.clone()
AK5jetCombinedSecondaryVertexBJetTagsCHS.tagInfos = cms.VInputTag( cms.InputTag("AK5jetImpactParameterTagInfosCHS"), cms.InputTag("AK5jetSecondaryVertexTagInfosCHS") )

AK5jetImpactParameterTagInfosSJCHS                     = impactParameterTagInfos.clone()
AK5jetImpactParameterTagInfosSJCHS.jetTracks           = "AK5jetTracksAssociatorAtVertexSJCHS"
AK5jetSecondaryVertexTagInfosSJCHS                     = secondaryVertexTagInfos.clone()
AK5jetSecondaryVertexTagInfosSJCHS.trackIPTagInfos     = "AK5jetImpactParameterTagInfosSJCHS"
AK5jetCombinedSecondaryVertexBJetTagsSJCHS          = combinedSecondaryVertexBJetTags.clone()
AK5jetCombinedSecondaryVertexBJetTagsSJCHS.tagInfos = cms.VInputTag( cms.InputTag("AK5jetImpactParameterTagInfosSJCHS"), cms.InputTag("AK5jetSecondaryVertexTagInfosSJCHS") )

from JetTools.AnalyzerToolbox.QGTagger_RecoJets_cff import *
AK5QGTaggerCHS                                       = QGTagger.clone()
AK5QGTaggerCHS.srcJets                               = cms.InputTag('AK5PFJetsCHS')
AK5QGTaggerSubJetsCHS                                = AK5QGTaggerCHS.clone()
AK5QGTaggerSubJetsCHS.srcJets                        = cms.InputTag('AK5caPFJetsPrunedCHS','SubJets')

from JetTools.AnalyzerToolbox.AnalyzerJetToolbox_cff import *
AK5NjettinessCHS                                     = Njettiness.clone()       
AK5NjettinessCHS.src                                 =  cms.InputTag('AK5PFJetsCHS')


AK5jetsequenceCHS = cms.Sequence(
    AK5PFJetsCHS                      *
    AK5caPFJetsPrunedCHS              *
    AK5jetTracksAssociatorAtVertexCHS    *
    AK5jetImpactParameterTagInfosCHS     *
    AK5jetSecondaryVertexTagInfosCHS     *
    AK5jetTracksAssociatorAtVertexSJCHS  *
    AK5jetImpactParameterTagInfosSJCHS   *
    AK5jetSecondaryVertexTagInfosSJCHS   *
    AK5jetCombinedSecondaryVertexBJetTagsCHS * 
    AK5jetCombinedSecondaryVertexBJetTagsSJCHS  *
    AK5QGTaggerCHS                       *
    AK5QGTaggerSubJetsCHS                *                
    AK5NjettinessCHS                     
    )
