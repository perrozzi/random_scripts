import os, sys

# outputdir = "/eos/cms/store/group/phys_generator/14TEV/PhaseIISummer17"
outputdir = "/eos/cms/store/group/upgrade/PhaseIISummer17/"
evts_per_job = 10000
submit_datasets = [ # prepid                                 total_n_evts
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00021',200000], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00024',1000000], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00026',1000000], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00027',7000000], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00002',5000000], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00025',2000000], # GRIDPACK NON EXISTING
                    ['SMP-PhaseIISummer17wmLHEGENOnly-00004',20000000],
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00005',20000000],
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00007',20000000],
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00008',20000000],
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00009',20000000],
                  ]

for dataset in submit_datasets:
    # create output dir already now to avoid permission issues
    os.system("mkdir "+outputdir+"/"+dataset[0])
    # compute the number of jobs + 5% to account for some efficiency loss
    njobs = int(float(dataset[1])/float(evts_per_job)*1.05)
    print  "submitting "+str(njobs)+" jobs"
    os.system("sleep 2")
    for i in range(1,njobs):
        os.system("bsub -u ciaociao1 -q 1nd submit_jobs.sh "+dataset[0]+" "+str(evts_per_job)+"; sleep 1")
