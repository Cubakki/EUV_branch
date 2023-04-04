import shutil

with open("./Error_Terminated.err","r",encoding="utf-8") as f:
    el=f.readlines()
    f.close()
with open("../worked.log","r",encoding="utf-8")as f:
    wk=f.readlines()
    f.close()
for er in el:
    shutil.rmtree(f"./orca_workdir/{er.strip()}")
wk2=[]
for worked in wk:
    if not worked in el:
        wk2.append(worked)

with open("../worked.log","w",encoding="utf-8")as f:
    f.write("".join(wk2))