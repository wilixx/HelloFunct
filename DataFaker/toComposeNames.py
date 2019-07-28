#!/usr/bin/env python
# coding=utf-8
# author: Allen Guo
import exrex
'''
# 本方法用于构造中文姓名
'''
def ChineseNameComposer(PersonTempDict):
    name = exrex.getone(PersonTempDict["familyName"])+exrex.getone(PersonTempDict["composedName"])
    return name
if __name__ == "__main__":
    # 工作流如下
    # 创建姓名模板
    PersonTempDict = dict(
                         familyName=r"(郭)",# r"(赵|钱|孙|李|周|吴|郑|王|国|马|张|刘|胡|沈)",
                         composedName=r'(星|空|金|少|邵|益|何|美|华|盛|友|小|雨)'+
                                      r'(安|居|乐|业|国|泰|民|安|宝|玉|太|平|丽|平|涛|意|亮|广|旋|利|民|瑞|雪)',
                         )
    for i in range(50):
        print(ChineseNameComposer(PersonTempDict))
