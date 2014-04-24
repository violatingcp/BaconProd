#!/bin/bash

if test -z $CMSSW_VERSION; then
  echo "[BaconProd] Need CMSSW project area setup!";
  echo
  return 0;
fi

CURRDIR=$PWD
PATCHDIR=$CMSSW_BASE/src/BaconProd/patch
cd $CMSSW_BASE/src


### MuScleFit corrections for muons
echo
echo "[BaconProd] Checking out MuScleFit package..."
cp -r /afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_5_3_13/src/MuScleFit $CMSSW_BASE/src/

### Electron MVA ID
echo
echo "[BaconProd] Checking out Electron MVA ID package..."
cp -r /afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_5_3_13/src/EGamma $CMSSW_BASE/src/

### MET filters
echo
echo "[BaconProd] Checking out packages for MET filters..."
#cvs co -r V00-00-13-01 RecoMET/METFilters
#cvs co -r V00-00-08    RecoMET/METAnalyzers
cp -r /afs/cern.ch/work/p/pharris/pharris/public/bacon/prod/CMSSW_6_2_7_patch2/src/RecoMET/            $CMSSW_BASE/src/

### Jet/MET packages
echo
echo "[BaconProd] Checking out jet/MET packages..."
git clone https://github.com/nhanvtran/JetTools.git
cp $PATCHDIR/JetTools/AnalyzerToolbox/python/njettinessadder_cfi.py JetTools/AnalyzerToolbox/python/

cp -r /afs/cern.ch/work/p/pharris/public/tmp/CMSSW_5_3_13/src/DataFormats 
cp -r /afs/cern.ch/work/p/pharris/pharris/public/bacon/prod/CMSSW_6_2_7_patch2/src/DataFormats $CMSSW_BASE/src
cp -r /afs/cern.ch/work/p/pharris/public/tmp/CMSSW_5_3_13/src/RecoJets                         $CMSSW_BASE/src
cp -r /afs/cern.ch/work/p/pharris/public/tmp/CMSSW_5_3_13/src/CondFormats                      $CMSSW_BASE/src

git clone https://github.com/violatingcp/Jets_Short.git
mv Jets_Short/RecoJets/JetProducers/data/*.xml RecoJets/JetProducers/data/
rm -rf Jets_Short

cp $PATCHDIR/RecoMET/METPUSubtraction/python/mvaPFMET_leptons_cff.py RecoMET/METPUSubtraction/python/
cp $PATCHDIR/RecoMET/METPUSubtraction/data/*Sep*.root                RecoMET/METPUSubtraction/data/

### clean up large unncessary files to fit into CRAB input sandbox (100MB)
rm -f RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_53X_chs_Dec2012.weights.xml.~1.1.~
rm -f JetTools/AnalyzerToolbox/data/TMVAClassification*.xml

### remove any compiled python scrips from copied directories...
rm -f */*/python/*.pyc

echo
echo "[BaconProd] Setup complete!"

cd $CURRDIR

return 1;
