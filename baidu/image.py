#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pandas as pd
import time,re
import openpyxl

def reple(id):
    return id != "all"

class files:
    def __init__(self, folder):
        self.folder = folder
        self.lists = []
        self.htlists = []
    def list(self):
        if os.path.isdir(self.folder):
            path = os.path.join(self.folder, "sem")
            lists = os.listdir(path)
            for list in lists:
                item = ''
                type = list[-4:]
                name = list.split("_")
                if type == '.csv':
                    if name[0] == 'jihua':
                        item = 'baidu'
                    elif name[0] == '推广计划':
                        item = 'sogou'
                    else:
                        item = '360'
                    types = [item, list]
                    self.lists.append(types)
                else:
                    return False

    def data(self):
        semdata = []
        for file in self.lists:
            path = os.path.join(self.folder, "sem")
            file_path = os.path.join(path, file[1])

            #print(file_path)
            if  file[0] == "baidu":
                data = self.get_file_data(file_path, nums=7)
                #print(file_path)
                data.reindex()
                nums = data.shape[1]
                if nums != 11:
                    print("%s文件可能下载格式错误"%file_path)
                else:
                    col = ['日期','账户','推广计划','推广计划ID','展现','点击','消费','点击率','平均点击价格','网页转化','商桥转化']
                    data.columns = col
                    data['推广计划'] = data['推广计划'].replace("\[已删除\]","")
                    col = ["日期","账户","推广计划","展现","点击","消费","平均点击价格","点击率"]
                    data = pd.DataFrame(data,columns=col)

            elif file[0] == "360":
                data = self.get_file_data(file_path,nums=1)
                data.reindex()
                nums = data.shape[1]
                if nums != 9:
                    print("%s文件可能下载格式错误"%file_path)
                else:
                    col = ['日期','账户','产品线','推广计划','展现','点击','点击率','消费','平均点击价格']
                    data.columns = col
                    data['推广计划'] = data['推广计划'].replace("\[已删除\]", "")
                    col = ["日期","账户","推广计划","展现","点击","消费","平均点击价格","点击率"]
                    data = pd.DataFrame(data, columns=col)
                # data.set_index(["日期"])
            elif file[0] == "sogou":
                data = self.get_file_data(file_path,nums=1)
                data = data.drop(index = [0])
                data.reindex()
                nums = data.shape[1]
                if nums != 10:
                    print("%s..........(文件可能下载格式错误)"%file_path)
                else:
                    col = ['编号','日期','账户','推广计划','展现','点击数','点击','点击率','平均点击价格','有消耗词量']
                    data.columns = col
                    data['推广计划'] = data['推广计划'].str.replace("\[已删除\]", "")
                    col = ["日期","账户","推广计划","展现","点击","消费","平均点击价格","点击率"]
                    data = pd.DataFrame(data, columns=col)

            else:
                print("error")

            semdata.append(data)
        sdata = pd.concat(semdata,axis=0)
        sdata.columns = ["日期","账户","推广计划","展现","点击","消费","平均点击价格","点击率"]
        sdata['平均点击价格'] = sdata['消费'] / sdata['点击']
        sdata['点击率'] = sdata['点击'] / sdata['展现']
        #print(sdata)
        sdata = sdata[["日期", "账户", "推广计划", "展现", "点击", "点击率", "消费", "平均点击价格"]]
        sdata.drop_duplicates(subset=["日期","账户","推广计划"],inplace=True,keep='first')
        sdata.sort_values(['日期','账户'],inplace=True)
        #print(sdata)
        filename = os.path.join(self.folder, "sem.csv")
        sdata.to_csv(filename, encoding="utf-8", index=False, mode='w+')
        #print(sdata)
    def htlist(self):
        if os.path.isdir(self.folder):
            path = os.path.join(self.folder, "houtai")
            lists = os.listdir(path)
            lists = os.listdir(path)
            for list in lists:
                item = ''
                type = list[-4:]
                if type == '.csv':
                    self.htlists.append(list)
    def houtai(self):
        htdata = []
        path = os.path.join(self.folder, "houtai")
        for file in self.htlists:
            file_path = os.path.join(path, file)
            data = self.get_file_data(file_path, nums=1)
            data.columns = ['日期','渠道','软件ID','软件名称','PV','安全下载','普通下载','按钮3','按钮4','下载点击总数','调起','成功安装','下载/PV','调起/下载','安装成功率','安装整体转化','当天报活率','新装卸载率','次日留存率','七日留存率','新装卸载数','次日留存数','七人留存数','重复安装量','重复安装比例']
            data.reindex()
            #print(data)
            htdata.append(data)
        htdata = pd.concat(htdata, axis=0)
        htdata.columns =  ['日期','渠道','软件ID','软件名称','PV','安全下载','普通下载','按钮3','按钮4','下载点击总数','调起','成功安装','下载/PV','调起/下载','安装成功率','安装整体转化','当天报活率','新装卸载率','次日留存率','七日留存率','新装卸载数','次日留存数','七人留存数','重复安装量','重复安装比例']
        htdata.drop_duplicates(subset=["日期", "渠道", "软件ID"], inplace=True,keep="first")
        htdata.replace('None',0,inplace=True)
        htdata.sort_values(['日期', '渠道'], inplace=True)
        htdata = htdata.loc[htdata['软件ID'].apply(reple)]
        htdata = htdata.drop_duplicates(subset=['日期','渠道','软件ID'],keep="first")
        filename = os.path.join(self.folder, "houtai.csv")
        htdata.to_csv(filename, encoding="utf-8", index=False, mode='w+')

    def get_file_data(self,file_path,nums):
        try:
            data = pd.read_csv(file_path, encoding='gbk', header=None, skiprows=nums)
        except:
            data = pd.read_csv(file_path, encoding='utf-8', header=None, skiprows=nums)
        return data
if __name__ == '__main__':
    infopath = os.getcwd()
    print("生成文件目录为：{}".format(infopath))
    files = files(infopath)
    files.list()
    print("正在合并推广文档。。。。。。。")
    try:
        files.data()
        print("生成SEM文档成功！请查看")
    except Exception as err:
        print("err %s: " % err)
        print("异常错误")
    files.htlist()
    print("正在合并后台文档。。。。。。。")
    try:
        files.houtai()
        print("生成SEM文档成功！请查看")
    except Exception as err:
        print("err %s: " % err)

    os.startfile(infopath)
