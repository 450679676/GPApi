"""
读取ini文件配置信息
"""
import configparser


def read(path,selector,option):
    conf = configparser.ConfigParser()#实例化对象

    conf.read(path) #读取文件内容
    return conf.get(selector,option) # GET返回配置文件中的DEFAULT下的URL

#print(read('./inter_conf.ini','DEFAULT',"URL"))