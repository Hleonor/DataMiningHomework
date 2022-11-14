import pdfplumber

# 读取报告1.pdf
with pdfplumber.open('Text/报告1.pdf') as pdf_1:
    # 获取每一页的内容并保存到列表中
    pages = [page.extract_text() for page in pdf_1.pages]
    # 将列表中的内容合并成一个字符串
    novel_1 = ''.join(pages)

# 读取报告2.pdf
with pdfplumber.open('Text/报告2.pdf') as pdf_2:
    pages = [page.extract_text() for page in pdf_2.pages]
    novel_2 = ''.join(pages)

# 读取报告3.pdf
with pdfplumber.open('Text/报告3.pdf') as pdf_3:
    pages = [page.extract_text() for page in pdf_3.pages]
    novel_3 = ''.join(pages)

# 将三份报告的内容合并为一个字符串
novel_combine = novel_1 + novel_2 + novel_3

import jieba
jieba.setLogLevel(jieba.logging.INFO)

novelList_1 = list(jieba.lcut(novel_1))
novelList_2 = list(jieba.lcut(novel_2))
novelList_3 = list(jieba.lcut(novel_3))
#合并三个报告的分词结果
novelList_combine = list(jieba.lcut(novel_combine))

stopwords = [line.strip() for line in open('Text/stop.txt', 'r', encoding='UTF-8').readlines()]

novelDict_1 = {}
novelDict_2 = {}
novelDict_3 = {}
novelDict_combine = {}

for word in novelList_1:
    if word not in stopwords:
        if len(word) == 1:  # 长度为1，不进行统计
            continue
        else:
            novelDict_1[word] = novelDict_1.get(word, 0) + 1  # 和之前的setDefault操作类似

for word in novelList_2:
    if word not in stopwords:
        if len(word) == 1:
            continue
        else:
            novelDict_2[word] = novelDict_2.get(word, 0) + 1

for word in novelList_3:
    if word not in stopwords:
        if len(word) == 1:
            continue
        else:
            novelDict_3[word] = novelDict_3.get(word, 0) + 1

for word in novelList_combine:
    if word not in stopwords:
        if len(word) == 1:
            continue
        else:
            novelDict_combine[word] = novelDict_combine.get(word, 0) + 1

novelListSorted_1 = list(novelDict_1.items())  # 通过items()方法将字典转换为元组列表
novelListSorted_2 = list(novelDict_2.items())
novelListSorted_3 = list(novelDict_3.items())
novelListSorted_combine = list(novelDict_combine.items())

'''
    通过lambda函数，将元组列表的第二个元素作为排序的关键字
    reverse=True表示降序排列
'''
novelListSorted_1.sort(key=lambda e: e[1], reverse=True)
novelListSorted_2.sort(key=lambda e: e[1], reverse=True)
novelListSorted_3.sort(key=lambda e: e[1], reverse=True)
novelListSorted_combine.sort(key=lambda e: e[1], reverse=True)

print("报告1的词频统计结果：")
for topWordUp in novelListSorted_1[:10]:  # 统计词频最高的前10个词
    print(topWordUp)
print("===========================")

print("报告2的词频统计结果：")
for topWordUp in novelListSorted_2[:10]:
    print(topWordUp)
print("===========================")

print("报告3的词频统计结果：")
for topWordUp in novelListSorted_3[:10]:
    print(topWordUp)
print("===========================")

print("三个报告的词频统计结果：")
for topWordUp in novelListSorted_combine[:10]:
    print(topWordUp)
print("===========================")






