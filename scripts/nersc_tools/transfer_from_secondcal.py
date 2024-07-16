import os
import sys
import shutil
import copy

consider_prior = True

def extract_energy_from_orca_outputfile(fp):
    with open(fp, 'r') as f:
        lines = f.readlines()
        f.close()
    for li in lines:
        if "FINAL SINGLE POINT ENERGY" in li:
            Energy = float(li.split()[-1]) * 27.2113863
            return Energy
    return False



if __name__ == "__main__":
    first_workdir = "../first_calculation/orca_workdir/"
    second_workdir = "../second_calculation/orca_workdir/"
    done_log_path = "../second_calculation/done.log"
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
        ini_nu_path = second_workdir + st_name + "/" + st_name +".xyz"
        if not os.path.exists(copy_path + f"{st_name}"):
            os.makedirs(copy_path + f"{st_name}" )
        target_path_nu = copy_path + f"{st_name}/"+"nu.xyz"
        target_path_ps = copy_path + f"{st_name}/" + "ps.xyz"
        target_path_ng = copy_path + f"{st_name}/" + "ng.xyz"
        print("Succeed in checking {}'s file to be transfered, now prepare to extract and write energy data".format(st_name))
        #energy data extract
        outfile_path_nu = first_workdir + st_name + "/" + "output.log"
        outfile_path_ps = second_workdir + st_name + "/" + "ps" + "/" + "output.log"
        outfile_path_ng = second_workdir + st_name + "/" + "ng" + "/" + "output.log"

        nu_energy = extract_energy_from_orca_outputfile(outfile_path_nu)
        ps_energy = extract_energy_from_orca_outputfile(outfile_path_ps)
        ng_energy = extract_energy_from_orca_outputfile(outfile_path_ng)

        ionization = ps_energy - nu_energy
        attachment = ng_energy - nu_energy

        #write energy data
        with open(copy_path + f"{st_name}" + "/" + "SP.inf", 'w') as f:
            f.write("nu_sp_energy:"+str(nu_energy)+"\n")
            f.write("ps_sp_energy:"+str(ps_energy)+"\n")
            f.write("ng_sp_energy:"+str(ng_energy)+"\n")
            f.write("ionization_energy:"+str(ionization)+"\n")
            f.write("Attachment_energy:"+str(attachment)+"\n")
            f.close()

        print("{}'s energy information written to {}".format(st_name, copy_path + f"{st_name}" + "/" + "SP.inf"))

        shutil.copy(ini_nu_path, target_path_nu)
        shutil.copy(ini_nu_path, target_path_ps)
        shutil.copy(ini_nu_path, target_path_ng)

        print("Transfer structure files done : {}".format(st_name))

        with open("./transfered.log", "a", encoding="utf-8") as f:
            f.write(st_name + "\n")
            f.close()
        transfer_num += 1

    print("transfer succeed. {} in all.".format(transfer_num))
