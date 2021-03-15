from snownlp import SnowNLP

"""
    输入指令文字
    输出指令类别
    项目移植需要修改snownlp/sentiments/__init__.py中的path
"""


def classify(word):
    predict = SnowNLP(word).sentiments
    if predict > 0.6:
        result = '合法指令'
    else:
        result = '非法指令'
    return result


# 测试代码
#word_result = classify("你好")
#print(word_result)