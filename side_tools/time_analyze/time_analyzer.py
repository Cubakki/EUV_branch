import json
import os
import numpy as np
from numpy import polyfit
import time
import matplotlib.pyplot as plt

'''
用于分析ORCA计算地耗时，主要分为两个模块

1、读取模块

2、分析与可视化模块
'''

class Exploiter:
    def __init__(self):
        self.work_path=[]
        self.__data={}  #格式: {str(计算种类,OPT或SP):{str(方法与基组):[ [int(原子数),int(所用核时)] ],...},...}
        pass

    def add_exploit_path(self,paths):
        '''
        添加搜索(成对的输入文件input.inp和日志slurm.xxx的)目录
        :param paths:
        :return:
        '''
        for path in paths:
            self.work_path.append(path)
        pass

    def __write_self_data(self,result_list):
        '''

        :param result_list: [int(原子数),int(所用核时),str(计算种类,OPT或SP),str(方法与基组)]
        :return: True, False
        '''
        cal_type=result_list[2]
        cal_method=result_list[3]
        size=result_list[0]
        time=result_list[1]
        if not cal_type in self.__data.keys():
            self.__data[cal_type]={}
        if not cal_method in self.__data[cal_type].keys():
            self.__data[cal_type][cal_method]=[]
        self.__data[cal_type][cal_method].append([size,time])
        return True
    def __extract_file_pair(self,input_file_path,calculation_file_path):
        '''
        尝试提取输入文件和计算文件对中的信息（体系大小和使用核时）
        :param input_file_path:
        :param calculation_file_path:
        :return: True/False,直接判断结果，放弃或写入至self.data中
        '''
        with open(input_file_path,'r') as ifp:
            ifl=ifp.readlines()
            cal_type=ifl[0].split()[-1]
            cal_method=" ".join(ifl[0].split()[:1])[1:]
            core_num=int(ifl[1].split()[-2])
            atom_num=len(ifl)-5
        with open(calculation_file_path,'r') as cfp:
            cfl=cfp.readlines()
            if not "ORCA TERMINATED NORMALLY" in cfl[-2]:
                return False
            time_seq=cfl[-1].split()
            run_time=int(time_seq[3])*24+int(time_seq[5])+int(time_seq[7])/60+int(time_seq[9])/3600
            core_time=run_time*core_num

        self.__write_self_data([atom_num,core_time,cal_type,cal_method])
        return True
    def __exploit_recursion(self,nodes : list):
        '''
        递归遍历搜索目录下的所有叶节点，返回叶节点列表
        :return:
        '''
        for node in nodes:
            children=[node+"/"+child_name for child_name in os.listdir(node)]
            child_dir=[]
            #检查是否存在子目录与计算文件
            input_flag=False
            input_file_path=''
            cal_flag=False
            cal_file_path=''
            for child in children:
                if os.path.isdir(child):
                    child_dir.append(child)
                if "input.inp" in child:
                    input_flag=True
                    input_file_path=child
                if "slurm-" in child:
                    cal_flag=True
                    cal_file_path=child
            self.__exploit_recursion(child_dir)
            if (input_flag==True and cal_flag==True):
                print("Legal analyze file pair:{},{}".format(input_file_path,cal_file_path))
                self.__extract_file_pair(input_file_path,cal_file_path)
            #检查目录下是否存在输入文件与计算日志，若有则尝试读取
        pass

    def exploit(self):
        self.__exploit_recursion(self.work_path)
        self.__auto_save()

    def export_data_as_dict(self):
        return self.__data

    def __auto_save(self):
        with open("./exploit_data.json",'w',encoding='utf-8') as f:
            json.dump(self.__data,f)
            f.close()

class Analyzer_and_ploter:
    def __init__(self):
        self.data={}
        self.analyze_dict={}
        self.log=""
        pass

    def accept_data(self,data : dict):
        self.data=data

    def load_data_from_json(self,js_path):
        with open(js_path,'r',encoding='utf-8') as f:
            self.data=json.load(f)
            f.close()

    def analyze(self):
        self.__add_log("分析开始\n\n")
        for cal_type in self.data.keys():
            if not cal_type in self.analyze_dict.keys():
                self.analyze_dict[cal_type]={}
            for cal_method in self.data[cal_type].keys():
                #数据准备
                self.__add_log("-----------------------------------------------------------------")
                self.__add_log("计算类型:{},计算方法与模组:{}".format(cal_type,cal_method))

                if not cal_method in self.analyze_dict[cal_type].keys():
                    self.analyze_dict[cal_type][cal_method]=[]
                dataset=self.data[cal_type][cal_method] # dataset-- [ [int(原子数),int(核时)],...  ]
                size=np.array([x[0] for x in dataset])
                core_time=np.array([x[1] for x in dataset])

                #自动拟合
                self.__add_log("自动拟合开始,在1至5次多项式拟合中选择最优拟合\n")

                best_fit=self.__auto_polyfit(size,core_time)

                self.__add_log("自动拟合完成。")
                self.__add_log("最佳多项式次数为{}，对应最小均方差为{}".format(best_fit["bestFitTime"],best_fit["MAE"]))

                func_str="y = " + self.__gen_func(best_fit["coefficient"])

                self.__add_log("拟合多项式:{}   ,其中y为消耗核时,x为体系大小(原子数)".format(func_str))

                #绘图并保存

                self.__add_log("绘制图像并保存")

                plt.scatter(np.array([x[0] for x in dataset]),np.array([x[1] for x in dataset])) #绘制原始数据点图
                new_x=np.linspace(min(size),max(size),1000)  #生成横坐标(原子数使绘制曲线平滑)
                poly=np.poly1d(best_fit["coefficient"])
                plt.plot(new_x,poly(new_x),color='red') #绘制拟合曲线
                plt.savefig("./analyze_plot_{}_{}.png".format(cal_type,cal_method))
                plt.clf()

                self.__add_log("图像保存完成")
                self.__add_log("-----------------------------------------------------------------")
        self.__write_and_renew_log()

    def __auto_polyfit(self,data_x,data_y):
        corres_coefficient = polyfit(data_x, data_y, 1)  # 使用polyfit进行fit_time次拟合
        min_loss = self.__cal_loss(data_x, data_y, corres_coefficient)
        bestFitTime = 1
        for i in range(4):
            coefficient = polyfit(data_x, data_y, i + 2)
            loss = self.__cal_loss(data_x, data_y, coefficient)
            if loss < min_loss:
                min_loss = loss
                bestFitTime = i + 2
                corres_coefficient = coefficient

        return {'MAE': min_loss, 'bestFitTime': bestFitTime, 'coefficient': corres_coefficient}

    def __cal_loss(self,data_x,data_y,coefficient):
        xline = np.linspace(min(data_x), max(data_x), len(data_x) * 8)
        func = ""
        for i in range(len(coefficient)):
            func += str(coefficient[i]) + " * pow(x , " + str(len(coefficient) - i - 1) + ") + "

        func += "0"
        y = []
        for x in xline:
            p = eval(func)
            y.append(p)

        loss = 0
        for i in range(len(data_x)):
            x = data_x[i]
            p = pow(eval(func) - data_y[i], 2)
            loss += p
        loss = loss / len(data_x)
        return loss

    def __gen_func(self,coefficient):
        func = ""
        for i in range(len(coefficient)):
            func += str(coefficient[i]) + " * x^ " + str(len(coefficient) - i - 1) + " + "
        func=func[:-3]
        return func

    def __add_log(self,sentence):
        self.log += sentence
        self.log += '\n'
        return True

    def __write_and_renew_log(self):
        with open("./analyze_log_{}.txt".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),'w',encoding='utf-8') as f:
            f.write(self.log)
            f.close()
        self.log=""

if __name__=="__main__":
    paths=["/dm_data/wh/jingbin/SnHO/first_cal/orca_workdir/","/dm_data/wh/jingbin/SnHO/second_cal_svpopt/orca_workdir",
           "/dm_data/wh/jingbin/SnHO/third_cal/workdir"]

    exploiter=Exploiter()
    exploiter.add_exploit_path(paths)
    exploiter.exploit()
    exp_data=exploiter.export_data_as_dict()

    analyzer=Analyzer_and_ploter()
    analyzer.accept_data(exp_data)
    analyzer.analyze()
