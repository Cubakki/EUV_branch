import os

if __name__=="__main__":
    worked = [dir_name for dir_name in os.listdir("./orca_workdir")]

    with open("./worked.log","w") as f:
        f.write("\n".join(worked))
        f.close()

    print("worked.log written")