import pandas as pd
import jieba
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from db import sqlite3
from nltk.tokenize import word_tokenize  
nltk.download('punkt')

# 读取Excel文件
excel_file = 'static/lego-qa.xlsx'
df = pd.read_excel(excel_file, engine='openpyxl')

# 显示数据框架的前几行，确保正确读取数据
print(df['问题'].head())
print(df['处理结果'].head())

# 将问题和处理结果分别存储在列表中  
questions = df['问题'].tolist()  
results = df['处理结果'].tolist()  


# 对问题和处理结果进行分词处理  
tokenized_questions = [" ".join(jieba.cut(question)) for question in questions]
 
# 创建TaggedDocument对象列表，用于训练Doc2Vec模型  
# 每个TaggedDocument对象包含一个问题和它的标签（这里使用问题的索引作为标签）  
tagged_docs = [TaggedDocument(words=doc, tags=[str(i)]) for i, doc in enumerate(tokenized_questions)]  
  
# 训练Doc2Vec模型  
model = Doc2Vec(vector_size=200, min_count=1, window=5, epochs=40)  
model.build_vocab(tagged_docs)  
model.train(tagged_docs, total_examples=len(tagged_docs) * 2, epochs=model.epochs)  
model.save('qa.model')

# # 创建SQLite处理程序实例
# db_handler = sqlite3.SQLiteHandler("qa_vectors_database.db")
# db_handler.create_table()

# # 存储向量
# for i, words in enumerate(tokenized_texts):
#     text = " ".join(words)
#     vector = model.infer_vector(words)
#     db_handler.insert_vector(i, text, vector)  # 将ID一起存储



def search_and_retrieve_results(query, top_n=5):  
    # 对用户查询进行分词处理  
    tokenized_query = word_tokenize(query)  
    # model = Doc2Vec.load('qa.model')
    # 使用模型为查询生成向量  
    query_vector = model.infer_vector(tokenized_query)  
      
    # 计算查询向量与所有问题向量的相似度  
    similarities = model.dv.most_similar([query_vector], topn=len(model.dv.vectors))  
      
    # 获取最相似问题的索引  
    most_similar_indices = [index for index, _ in similarities]  
      
    # 返回最相似问题的处理结果  
    results_list = [questions[int(index)] for index in most_similar_indices[:top_n]]  
    return results_list  
  
# 示例用户查询  
user_query = "表单项如何在页面或者弹框居中"  
results_list = search_and_retrieve_results(user_query)  
print(f"对于查询 '{user_query}'，最相似问题的处理结果是:")  
for result in results_list:  
    print(result)