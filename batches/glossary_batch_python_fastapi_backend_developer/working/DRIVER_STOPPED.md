# STOPPED glossary_batch_python_fastapi_backend_developer

command failed (1): /home/azureuser/env/bin/python /home/azureuser/roles/python_fastapi_backend_developer/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py '/home/azureuser/roles/python_fastapi_backend_developer/glossary/batches/glossary_batch_python_fastapi_backend_developer' 'c1'
JeznW_7DlB0: 1 proposals, 0 rejected
xY__sjI5yVU: 0 proposals, 1 rejected
-aKFBoZpiqA: 1 proposals, 0 rejected
14z_Tf3p2Mw: 0 proposals, 1 rejected
oAkLSJNr5zY: 0 proposals, 1 rejected
Qb9s3UiMSTA: 0 proposals, 1 rejected
FsAPt_9Bf3U: 0 proposals, 1 rejected
6McU94UMY9M: 1 proposals, 0 rejected
Y21OR1OPC9A: 1 proposals, 0 rejected
Kg1Yvry_Ydk: 0 proposals, 1 rejected
Traceback (most recent call last):
  File "/home/azureuser/roles/python_fastapi_backend_developer/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py", line 189, in <module>
    main()
  File "/home/azureuser/roles/python_fastapi_backend_developer/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py", line 153, in main
    prompt = video_prompt(B, vid, pairs, C, briefs, pa, names, header)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/azureuser/roles/python_fastapi_backend_developer/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py", line 37, in video_prompt
    cat = load(BANK / "catalogue" / f"{vid}.json")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/azureuser/roles/python_fastapi_backend_developer/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py", line 24, in load
    return json.loads(Path(p).read_text())
                      ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/pathlib.py", line 1029, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/pathlib.py", line 1015, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/home/azureuser/roles/python_fastapi_backend_developer/glossary/00_GLOSSARY_PIPELINE_CORE/video_bank/catalogue/CeQJepmYkjQ.json'


Spend so far $7.71. Fix the cause, then rerun the same command (finished stages are skipped).
