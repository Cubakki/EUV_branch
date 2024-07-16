from transform.read import structure_reader
from transform.openmx_input_writer import OpenMXInputWriter
import os
from mpi4py import MPI
from filelock import FileLock

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

structure_path = "./structures"
work_path = "./openmx_workdir"
openmx_path = "/public/spst/home/wanghan3_6/softwares/openmx3.9/work/openmx"

if __name__ == '__main__':

    while True:
        lock = FileLock(f"worklist.lock")

        with lock:
            with open("worklist", "r") as f:
                worklist = [x.strip() for x in f.readlines()]
                f.close()
            try:
                work = worklist[0]
            except :
                lock.release()
                raise ValueError("No work in worklist.")
            with open("worklist","w") as f:
                f.write("\n".join(worklist[1:]))
                f.close()

        with open("./worked.log","a") as f:
            f.write(work+"\n")
            f.close()

        print("now rank {} start work with {}".format(rank,work))
        struct_work_path = work_path + "/" + work + "/" + "openmx_in.dat"
        os.chdir(structure_path)
        os.system("mpirun -np 16 {} openmx_in.dat > openmx.std".format(openmx_path))
        os.system("cat openmx.out >> openmx.scfout")
        with open("./done.log","a") as f:
            f.write(work+"\n")
            f.close()