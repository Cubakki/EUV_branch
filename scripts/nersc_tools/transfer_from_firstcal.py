import os
import sys
import shutil
import copy

consider_prior = True

if __name__ == "__main__":
    search_workdir = "../first_calculation/orca_workdir/"
    done_log_path = "../first_calculation/done.log"
    prior_log_path = "./prior.log"
    transfered_log_path = "./transfered.log"
    copy_path = "./structures/"
    transfer_num = 0

    if not os.path.exists(copy_path):
        os.makedirs(copy_path)

    with open(done_log_path, 'r') as f:
        done_list = [x.strip() for x in f.readlines()]
        f.close()
    transfer_list = copy.deepcopy(done_list)

    if consider_prior:
        with open(prior_log_path, "r") as f:
            prior_list = [x.strip() for x in f.readlines()]
            f.close()
        transfer_list = list(set(prior_list).intersection(set(done_list)))

    if not os.path.exists(transfered_log_path):
        with open(transfered_log_path, "w") as f:
            f.close()
    with open("./transfered.log",'r') as f:
        transfered = [x.strip() for x in f.readlines()]
        f.close()

    transfer_list = list(set(transfer_list)-set(transfered))

    for st_name in transfer_list:
        ini_path = search_workdir + st_name + "/input.xyz"
        target_path = copy_path + "{}.xyz".format(st_name)
        shutil.copy(ini_path, target_path)
        print("Success transfer {}".format(st_name))
        with open("./transfered.log", "a", encoding="utf-8") as f:
            f.write(st_name + "\n")
            f.close()
        transfer_num += 1

    print("transfer succeed. {} in all.".format(transfer_num))
