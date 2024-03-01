import pandas as pd
from transformers import BertTokenizer, BertModel
import torch

# 加载预训练模型及其分词器
model_name = 'bert-base-multilingual-cased'  # 这个模型对多种语言都有良好支持，包括中文
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# 读取数据
excel_file = 'static/lego-qa.xlsx'
df = pd.read_excel(excel_file, engine='openpyxl')

# 数据预处理
questions = df['问题'].tolist()
results = df['处理结果'].tolist()

# 将文本转换为向量
def text_to_vector(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    outputs = model(**inputs)
    return outputs.pooler_output[0].detach()

# 存储问题的向量表示
question_vectors = torch.stack([text_to_vector(q) for q in questions])

# 搜索与查询最相似的问题
def search_and_retrieve_results(query, top_n=5):
    query_vector = text_to_vector(query)
    cos = torch.nn.CosineSimilarity(dim=0)
    similarities = torch.tensor([cos(query_vector, q_vec) for q_vec in question_vectors])
    most_similar_indices = similarities.argsort(descending=True)[:top_n]
    return [questions[i] for i in most_similar_indices], [results[i] for i in most_similar_indices]

# 示例查询
user_query = "图片上传"
similar_questions, similar_results = search_and_retrieve_results(user_query)
print(f"对于查询 '{user_query}'，最相似的问题及其处理结果是:")
for question, result in zip(similar_questions, similar_results):
    print(f"问题: {question}\n处理结果: {result}\n")
