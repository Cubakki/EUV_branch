#遍历计算目录，匹配关键词将完整路径（计算目录下的次级路径）备份至/dm_data/wh/zhefengwang
import argparse,os
import copy
import shutil


def travel(pre_path,pre_list:list,bp,fliter_function=None):
    #Deal with Directories
    if os.path.isdir(pre_path):
        pre_list.append((pre_path.split("/")[-1]).split("\\")[-1])
        for secondary_path in os.listdir(pre_path):
            wsp=os.path.join(pre_path,secondary_path)
            travel(wsp,copy.deepcopy(pre_list),bp,fliter_function)
    #Deal with Files
    else:
        wp=pre_path
        fn = os.path.split(wp)[1]
        COPY=True
        if not fliter_function==None:
            COPY=fliter_function(fn)
        if COPY==True:
            wbp = recursion_mkdir(pre_list,bp)
            print("copy {} to {}".format(wp, os.path.join(wbp, fn)))
            shutil.copy(wp,os.path.join(wbp,fn))



def recursion_mkdir(d_list,bp):
    '''
    由于长路径不能用mkdir一次性创建，travel会维护一个路径块列表尝试分次创建
    :param d_list: 路径分块列表
    :return: path_created
    '''
    this_path=bp
    if not os.path.exists(bp):
        print("Cannot find backup path,try to create this path.")
        try:
            os.mkdir(bp)
        except:
            raise ValueError("FAIL TO CREATE BACKUP PATH.PLEASE DO IT MANNULLY.")
    for i in d_list:
        this_path=os.path.join(this_path,i)
        if not os.path.exists(this_path):
            os.mkdir(this_path)
            print("Create directory:{}".format(this_path))
    return this_path

def fliter(fn):
    '''
    筛选函数，配合travel使用 ***目前travel中只回传了fn文件名供处理
    :return:
    '''
    Key_words=["engrad",".inp","opt","property","trj",".xyz"]
    Flag=False
    if "tmp" in fn:
        return False
    for k in Key_words:
        if k in fn:
            print("keyword {} in {},allow to copy".format(k,fn))
            Flag=True
    return Flag


if __name__=="__main__":
    parser=argparse.ArgumentParser()

    parser.add_argument("-cp",default="./")
    parser.add_argument("-bp",default="/dm_data/wh/zhefengwang/backup/2023_7")
    parser.add_argument("--h",default="-cp the calculation path\n-bp the backup path\n")
    args=parser.parse_args()
    print("\nHelp:{}\n".format(args.h))

    Cpath=args.cp
    Bpath=args.bp

    #Travel and Move
    pre_list=[]
    travel(Cpath,pre_list,Bpath,fliter)