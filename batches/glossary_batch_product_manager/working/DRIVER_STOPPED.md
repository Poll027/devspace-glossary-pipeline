# STOPPED glossary_batch_product_manager

command failed (1): /home/azureuser/env/bin/python 00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py transcripts batches/glossary_batch_product_manager 00_GLOSSARY_PIPELINE_CORE/video_bank
[yt_bridge] posted job glossary_batch_product_manager (173 videos); waiting for the Mac worker
[yt_bridge] still waiting for the Mac worker (0 min)
[yt_bridge] still waiting for the Mac worker (5 min)
[yt_bridge] still waiting for the Mac worker (10 min)
[yt_bridge] still waiting for the Mac worker (15 min)
[yt_bridge] still waiting for the Mac worker (20 min)
[yt_bridge] still waiting for the Mac worker (25 min)
[yt_bridge] still waiting for the Mac worker (30 min)
[yt_bridge] still waiting for the Mac worker (35 min)
[yt_bridge] still waiting for the Mac worker (40 min)
[yt_bridge] still waiting for the Mac worker (45 min)
Traceback (most recent call last):
  File "/home/azureuser/roles/product_manager/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 219, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/azureuser/roles/product_manager/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 208, in main
    return vm_transcripts(a[1], a[2])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/azureuser/roles/product_manager/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 128, in vm_transcripts
    data = wait_result(jid)
           ^^^^^^^^^^^^^^^^
  File "/home/azureuser/roles/product_manager/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 103, in wait_result
    sync()
  File "/home/azureuser/roles/product_manager/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 38, in sync
    git("checkout", "-q", "-B", "yt-bridge", "origin/yt-bridge")
  File "/home/azureuser/roles/product_manager/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py", line 28, in git
    raise RuntimeError(f"git {' '.join(a)}: {(r.stdout + r.stderr)[-300:]}")
RuntimeError: git checkout -q -B yt-bridge origin/yt-bridge: x.lock': File exists.

Another git process seems to be running in this repository, e.g.
an editor opened by 'git commit'. Please make sure all processes
are terminated then try again. If it still fails, a git process
may have crashed in this repository earlier:
remove the file manually to continue.



Spend so far $5.01. Fix the cause, then rerun the same command (finished stages are skipped).
