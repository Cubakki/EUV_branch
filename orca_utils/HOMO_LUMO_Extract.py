#用于提取orca计算文件中的信息，得到homo-lumo gap
import os


def extract_homo_lomo_gap(orca_output_file_path : str):
    keyword='ORBITAL ENERGIES'
    keyposition=None
    with open(orca_output_file_path,'r',encoding='utf-8') as f:
        content=f.readlines()
        f.close()
    for i in range(0,len(content)):
        if keyword in content[i]:
            keyposition=i
    for k in range(keyposition,len(content)):
        if 'OCC' in content[k]:
            for t in range(k+1,len(content)):
                splited=content[t].split()
                if float(splited[1])==0:
                    homo=float(content[t-1].split()[3])
                    homo_level=float(content[t-1].split()[1])
                    lumo=float(content[t].split()[3])
                    lumo_level=float(content[t].split()[1])
                    gap=lumo-homo
                    break
            break

    return (gap,homo,lumo)


if __name__=='__main__':
    orca_workdir='./orca_workdir'
    gap_output_file='./HOMO_LUMO_GAP.txt'
    orca_outputfile_keyword='slurm'
    conclusion_list=[['name','gap(eV)','homo(eV)','lumo(eV)']]
    output_count=0
    for crystal_dir in os.listdir(orca_workdir):
        crystal_path=orca_workdir+'/'+crystal_dir
        if os.path.isdir(crystal_path):
            print('进入晶体计算目录:{}'.format(crystal_path))
            for file in os.listdir(crystal_path):
                if orca_outputfile_keyword in file:
                    try:
                        orca_output_file_path=crystal_path+'/'+file
                        print('尝试读取orca输出文件{}的信息'.format(orca_output_file_path))
                        gap_tuple=extract_homo_lomo_gap(orca_output_file_path)
                        conclusion_list.append([crystal_dir,str(gap_tuple[0]),str(gap_tuple[1]),str(gap_tuple[2])])
                        print('提取得到{}的homo:{}eV,lumo:{}eV,gap:{}eV'.format(crystal_dir,gap_tuple[1],gap_tuple[2],gap_tuple[0]))
                        output_count+=1
                    except:
                        print('未能提取{}目录中的homo-lumo信息,可能是文件类型错误或未收敛'.format(crystal_path))
    with open(gap_output_file,'w') as fi:
        fi.write('\n'.join(['{} {} {} {}'.format(x[0],x[1],x[2],x[3]) for x in conclusion_list]))
        fi.close()
    print('成功提取{}组homo-lumo gap并记录于{}中'.format(output_count,gap_output_file))
    #end
