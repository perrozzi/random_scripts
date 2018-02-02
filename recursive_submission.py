import os, sys, ROOT, glob

GenOnly = True

# just_check_entries = True
just_check_entries = False
string_to_filter_files = "" # for example "inRAWSIM"

queue = "1nd"

# outputdir = "/eos/cms/store/group/phys_generator/14TEV/PhaseIISummer17"
# outputdir = "/eos/cms/store/group/phys_generator/perrozzi/MinBiasCentralDiffraction"
# outputdir = "/eos/cms/store/group/upgrade/PhaseIISummer17/"
# outputdir = "/tmp/perrozzi"
outputdir = "/eos/cms/store/group/phys_generator/perrozzi/"

evts_per_job = 50000
submit_datasets = [ # prepid                           total_n_evts, matching*filter efficiency
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00021',200000,1], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00024',1000000,1], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00026',1000000,1], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00027',7000000,1], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00002',5000000], # DONE
                    # ['TOP-PhaseIISummer17wmLHEGENOnly-00025',2000000,1], # GRIDPACK NON EXISTING
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00004',20000000,0.27], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00005',20000000,0.129], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00007',20000000,0.693], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00008',20000000,0.272], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00009',20000000,0.109], # DONE
                    # ['SMP-PhaseIISummer17wmLHEGENOnly-00011',5000000,0.32], # DONE
                    # ['PPD-RunIIFall17GS-00005',10000000,1],
                    # ['PPD-RunIIFall17GS-00007',5000000,1],
                    # ['B2G-RunIISummer17wmLHEGS-00002',50000,1],
                    # ['HIG-RunIIFall17wmLHEGS-00597',1000000,(0.2*0.01)],
                    # ['HIG-RunIIFall17wmLHEGS-00598',1000000,(0.3*0.3688)],
                    ['HIG-RunIIFall17wmLHEGS-00599',1000000,(0.3*0.6117)],
                    # ['HIG-RunIIFall17wmLHEGS-00600',1000000,(0.2*0.004)],
                  ]

for dataset in submit_datasets:
    print "analyzing dataset",str(dataset)
    # create output dir already now to avoid permission issues
    if not os.path.isdir(outputdir+"/"+dataset[0]):
        os.system("mkdir "+outputdir+"/"+dataset[0])
    print "output dir: "+outputdir+"/"+dataset[0]
    # check for existing files
    files = glob.glob(outputdir+"/"+dataset[0]+"/"+dataset[0]+"*"+string_to_filter_files+"*")
    print"found",len(files),"files"
    sys.stdout.flush()
    if just_check_entries:
        chain = ROOT.TChain("Events")
        for file in files:
            chain.Add(file)
        produced_events = chain.GetEntries()
        print "produced events:",str(produced_events),"/",str(dataset[1]),"i.e.",str(float(produced_events)/float(dataset[1])*100),"%"
        sys.stdout.flush()
    else:
        produced_events = 0
        # compute the number of jobs + 5% to account for some efficiency loss
        n_events = float(float(dataset[1])-float(produced_events))
        effective_evts_per_job = float(evts_per_job*float(dataset[2]))
        print "matching*filter efficiency:",dataset[2],"effective number of events per job:",str(effective_evts_per_job)
        njobs = int(n_events/float(effective_evts_per_job)*1.05)-int(len(files))
        print  "submitting "+str(njobs)+" jobs to produce",n_events,"events"
        os.system("sleep 2")
        for i in range(0,njobs):
            print("bsub -u ciaociao1 -C 0 -q "+queue+" submit_jobs.sh "+dataset[0]+" "+str(evts_per_job)+" "+outputdir+" "+int(GenOnly))
            os.system("bsub -u ciaociao1 -C 0 -q "+queue+" submit_jobs.sh "+dataset[0]+" "+str(evts_per_job)+" "+outputdir+" "+int(GenOnly)+"; sleep 5; rm -rf LSFJOB_* core.*")
            # os.system("sh submit_jobs.sh "+dataset[0]+" "+str(evts_per_job)+" "+outputdir)
            if i % 100 == 0:
                  os.system("echo 'submitted "+str(i)+" jobs, sleeping 3 minutes'; sleep 200")
    sys.stdout.flush()

os.system("echo 'submission complete'")

while True:
    os.system("rm -rf LSFJOB_* core.*; sleep 30")
