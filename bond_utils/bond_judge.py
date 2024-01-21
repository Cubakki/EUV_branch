from bond_utils.load_bondlen_data import SRD101,CSD_radius


#对于相当一部分的情况，分子中由于判断键的尺度不易于控制(CSD共价半径方法)，容易出现孤立的原子，整个体系不连通。因此，键的判断应该是
#整体的、弹性的。因此放弃这一方法。
class bond_judge():
    def __init__(self,mode):
        self.bond_dict=SRD101()
        self.radius_dict=CSD_radius()
        self.mode=mode

    def mode(self,mode):
        '''
        更改模式
        :param mode:1--经典键长,2--成键半径
        :return: int (self.mode)
        '''
        self.mode=mode
        return self.mode

    def judge(self,site1,site2,distance,allowed_bias):
        '''
        单位为埃
        :param site1: atom1
        :param site2: atom2
        :param bond_lenth: 几何距离
        :param allowed_bias: 允许的误差倍率。允许x的误差倍率意味着上限提升至(1+x)倍，而下限缩小至1/(1+x)倍
        :return: bool
        '''
        try:
            if self.mode==1:
                typical_lenth=float(self.bond_dict[site1][site2])
                if typical_lenth/(1+allowed_bias) <= distance <= typical_lenth*(1+allowed_bias):
                    return True
            elif self.mode==2:
                radius_sum=float(self.radius_dict[site1])+float(self.radius_dict[site2])
                if radius_sum/(1+allowed_bias) <= distance <= radius_sum*(1+allowed_bias):
                    return True
            else:
                raise Exception
        except:
            raise NotImplementedError(f"the bond between {site1} and {site2} is not in database")
        return False