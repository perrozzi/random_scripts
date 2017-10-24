# example
# sh script         prepid --> ${1}                       nevts --> ${2}
# sh submit_jobs.sh TOP-PhaseIISummer17wmLHEGENOnly-00024 100000

# retrieve test request script with a given number of events (the downloaded script name will be the number of events...)
wget https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/${1}/${2}

# pick up a random seed from bash
rndm=${RANDOM}
echo "USING RANDOM SEED "${rndm}
# manipulate the test request script to add the customized random seed once the job cfg is created
perl -pi -e '$_ .= qq(echo "process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = cms.untracked.uint32('${rndm}')" \>\> '${1}'_1_cfg.py\n) if /cmsDriver/' ${2}

# launch the test request script
sh ${2}

outputdir=/eos/cms/store/group/phys_generator/14TEV/PhaseIISummer17
# create remote directory
mkdir ${outputdir}/${1}

# cp output files adding the random seed in the filename to avoid duplicates
cp ${1}.root ${outputdir}/${1}/${1}-${rndm}.root
cp ${1}_inRAWSIM.root ${outputdir}/${1}/${1}_inRAWSIM-${rndm}.root
