import pdfplumber
import xlwt
# 读取报告2.pdf
with pdfplumber.open('Text/报告2.pdf') as pdf_2:
    # 获取每一页的内容并保存到列表中
    pages = [page.extract_text() for page in pdf_2.pages]
    # 将列表中的内容合并成一个字符串
    novel_2 = ''.join(pages)

import jieba
jieba.setLogLevel(jieba.logging.INFO)

# 每句话作为一条交易记录，每个词作为一个item，每句话分别进行分词，然后将分词结果作为一条交易记录
transactions_ = []
for line in novel_2.split('。'):
    transactions_.append(list(jieba.lcut(line)))

# 加载停用词
stopwords = [line.strip() for line in open('Text/stop.txt', 'r', encoding='UTF-8').readlines()]

transactions = []  # 保存处理后的交易记录
tmp_transaction = []
# 将事务中的停用词和长度为1个字的汉字，逗号，句号，换行符和\u3000等去掉
for transaction in transactions_:
    for word in transaction:
        if word in stopwords or len(word) == 1:
            continue
        else:
            tmp_transaction.append(word)
    transactions_copy = tmp_transaction.copy()
    transactions.append(transactions_copy)
    tmp_transaction.clear()

transactions_.clear()
stopwords.clear()

from efficient_apriori import apriori
# 调用apriori算法，得到频繁项集和关联规则以及支持度和置信度
item_sets, rules = apriori(transactions, min_support=0.03,  min_confidence=0.01)
# 将关联规则按照提升度从大到小排序
rules = sorted(rules, key=lambda x: x.lift, reverse=True)

# 打印频繁项集，按项集中的元素个数分类打印
for key, value in item_sets.items():
    print('频繁项集元素个数：', key)
    for item in value:
        print('  ', item)
print("\n")

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('关联规则', cell_overwrite_ok=True)
col = ('关联规则', '支持度', '置信度', '提升度')
for i in range(0, 4):
    sheet.write(0, i, col[i])

# print('关联规则：', rules)
# 打印置信度和提升度
index = 1
for rule in rules:
    if index > 20:
        break
    print("=============================")
    # print("{0} ==> {1}".format(rule.lhs, rule.rhs))
    print('规则：', rule)
    print('置信度：', rule.confidence)
    print('提升度：', rule.lift)
    print("=============================")
    sheet.write(index, 0, "{0} --> {1}".format(rule.lhs, rule.rhs))
    sheet.write(index, 1, format(rule.support, '.3f'))
    sheet.write(index, 2, format(rule.confidence, '.3f'))
    sheet.write(index, 3, format(rule.lift, '.3f'))
    index += 1

book.save('Text/报告2关联规则挖掘结果.xls')



