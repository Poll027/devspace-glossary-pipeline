# STOPPED glossary_batch_business_analyst

command failed (1): /home/azureuser/env/bin/python 00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py transcripts batches/glossary_batch_business_analyst 00_GLOSSARY_PIPELINE_CORE/video_bank
[yt_bridge] posted job glossary_batch_business_analyst (98 videos); waiting for the Mac worker
[yt_bridge] still waiting for the Mac worker (0 min)
[yt_bridge] still waiting for the Mac worker (5 min)
[yt_bridge] still waiting for the Mac worker (10 min)
[yt_bridge] still waiting for the Mac worker (15 min)
[yt_bridge] still waiting for the Mac worker (20 min)
Traceback (most recent call last):
  File "/home/azureuser/roles/business_analyst/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 219, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/azureuser/roles/business_analyst/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 208, in main
    return vm_transcripts(a[1], a[2])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/azureuser/roles/business_analyst/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 128, in vm_transcripts
    data = wait_result(jid)
           ^^^^^^^^^^^^^^^^
  File "/home/azureuser/roles/business_analyst/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 103, in wait_result
    sync()
  File "/home/azureuser/roles/business_analyst/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 38, in sync
    git("checkout", "-q", "-B", "yt-bridge", "origin/yt-bridge")
  File "/home/azureuser/roles/business_analyst/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 28, in git
    raise RuntimeError(f"git {' '.join(a)}: {(r.stdout + r.stderr)[-300:]}")
RuntimeError: git checkout -q -B yt-bridge origin/yt-bridge: error: could not lock config file .git/config: File exists
error: unable to write upstream branch configuration
hint: 
hint: After fixing the error cause you may try to fix up
hint: the remote tracking information by invoking:
hint:   git branch --set-upstream-to=origin/refs/heads/yt-bridge



Spend so far $4.70. Fix the cause, then rerun the same command (finished stages are skipped).
