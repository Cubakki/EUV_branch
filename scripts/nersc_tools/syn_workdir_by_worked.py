import shutil
import os

if __name__=="__main__":
    with open("./worked.log","r") as f:
        worked=[x.strip() for x in f.readlines()]
        f.close()

    for dirs in os.listdir("./orca_workdir"):
        if not dirs in worked:
            shutil.rmtree("./orca_workdir/{}".format(dirs))
            print("{} removed".format(dirs))

    print("program end")