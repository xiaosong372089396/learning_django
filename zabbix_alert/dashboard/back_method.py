#-*-coding:utf-8-*-
import psutil


class BackMethod(object):
    def __init__(self,name):
        self.name = name

    def calculateCpu(self):
        interval = 1
        #计算cpu利用率
        cpu_count = psutil.cpu_percent(interval)
        return cpu_count

    def calculateMemory(self):
        #返回内存使用情况
        phymem = psutil.virtual_memory()
        #总共的内存
        total_memory = phymem.total
        #已经使用内存
        used_memory = phymem.used
        return {"total":total_memory,"used":used_memory}



