import copy
import os.path
from bond_utils.bond_judge import bond_judge
from transform.structure import Molecule,Site


def bond_generate(molecule : Molecule):
    '''
        返回的bond_dict格式--{atom1:[[atomx,atomy,...],{atomx:distance1_x,atomy:distance1_y,...}],atom2...}
        :param molecule:
        :param mode: 1--经典键长,2--原子成键半径
        :return: bond_dict
        **这里的molecule是浅拷贝，虽然我们最后将它返回了，但即使不返回，作为入参的molecule中的site也已经被修改了
        '''
    '''
    1、首先根据CSD半径和一个小的容许误差初步拟定成键情况

    2、选择一个原子为起点遍历其连通的原子群，若这一群不包含整个结构中的全部原子，则剩余原子作为另一个群。逐步放宽允许的成键半径直到两群联通。

    3、重复2中步骤直到整个体系连通   
    '''
    distance_matrix = molecule.distance_matrix
    sites = molecule.sites
    site_name_list=molecule.sites_name_list
    bond_dict = {x:[[],{}] for x in site_name_list}
    judger=bond_judge(2)
    shape=len(distance_matrix)
    bias=0.1
    #初次成键
    while True:
        for site1_id in range(0,len(sites)):
            site1=sites[site1_id]
            if len(site1.bonded_site)==0:
                for site2_id in range(site1_id,molecule.atom_num):
                    if not site2_id==site1_id:
                        site2=sites[site2_id]
                        distance=distance_matrix[site1_id][site2_id]
                        judge_result=judger.judge(site1.specie.name,site2.specie.name,distance,allowed_bias=bias)
                        if judge_result:
                            site1.add_bond(site2_id)
                            site2.add_bond(site1.site_id)
                            bond_dict[site1.site_name][0].append(site2.site_name)
                            bond_dict[site1.site_name][1][site2.site_name] = distance
                            bond_dict[site2.site_name][0].append(site1.site_name)
                            bond_dict[site2.site_name][1][site1.site_name] = distance
        break
    #循环扩大允许误差保证连通
    while True:
        #检验是否连通并分组
        linked_group=Bond_DFS(0,[],molecule)  #这里的linked_group是一个塞满了site_id的列表，因此判断是否全连通可以直接判断列表长度
        if not len(linked_group)==molecule.site_num:
            bias+=0.1
            isolated_group=list(set([i for i in range(0,molecule.site_num)])-set(linked_group))
            for site1_id in linked_group:
                site1 = molecule.get_site(site1_id)
                for site2_id in isolated_group:
                    site2=molecule.get_site(site2_id)
                    distance=distance_matrix[site1_id][site2_id]
                    judge_result = judger.judge(site1.specie.name, site2.specie.name, distance, allowed_bias=bias)
                    if judge_result:
                        site1.add_bond(site2_id)
                        site2.add_bond(site1.site_id)
                        bond_dict[site1.site_name][0].append(site2.site_name)
                        bond_dict[site1.site_name][1][site2.site_name] = distance
                        bond_dict[site2.site_name][0].append(site1.site_name)
                        bond_dict[site2.site_name][1][site1.site_name] = distance
        else:
            break
    return bond_dict


    pass


def Bond_DFS(current_position: int, travelled_atoms: list,molecule : Molecule):
    '''

    :param current_position:  site_id
    :param travelled_atoms: used for recurison
    :param molecule: class Molecule Object
    :return:
    '''
    #site_group是travelled_atoms的浅拷贝，实际上在任意一层递归中都是同一个对象，因而只需在每层中append一次即可
    site_group = travelled_atoms
    site_group.append(current_position)
    for linked_site_id in molecule.get_site(current_position).bonded_site:
        if not linked_site_id in travelled_atoms:
            Bond_DFS(linked_site_id, site_group,molecule)
        else:
            continue
    return site_group

def bond_generate_old(molecule : Molecule):
    '''
    返回的bond_dict格式--{atom1:[[atomx,atomy,...],{atomx:distance1_x,atomy:distance1_y,...}],atom2...}
    :param molecule:
    :param mode: 1--经典键长,2--原子成键半径
    :return: bond_dict
    '''
    bond_dict={}
    distance_matrix=molecule.distance_matrix
    sites=molecule.sites
    used_ele={x:1 for x in molecule.symbol_set}
    for site in sites:
        bond_dict[site.specie.name+str(used_ele[site.specie.name])]=[[],{}]
        used_ele[site.specie.name]+=1
    judger=bond_judge(2)
    shape=len(distance_matrix)
    elements=list(bond_dict.keys())
    for m in range(0,shape):
        for n in range(m,shape):
            site1_element=sites[m].specie.name;site1=elements[m]
            site2_element=sites[n].specie.name;site2=elements[n]
            distance=distance_matrix[(m,n)]
            try:
                judge=judger.judge(site1_element,site2_element,distance,0.5)
                if judge:
                    bond_dict[site1][0].append(site2)
                    bond_dict[site1][1][site2] = distance
                    bond_dict[site2][0].append(site1)
                    bond_dict[site2][1][site1] = distance
            except NotImplementedError:
                print(f"{site1} and {site2} is not in bond_lenth database")
            except:
                print("warning")
    return bond_dict

