import pandas as pd  
from llama2 import Index, Document, Field, TextType, Searcher, QueryParser  
  
# 读取数据  
excel_file = 'static/lego-qa.xlsx'  
df = pd.read_excel(excel_file, engine='openpyxl')  
  
# 提取问题和处理结果列的数据  
questions = df['问题'].tolist()  
results = df['处理结果'].tolist()  
  
# 创建索引  
index = Index("lego_qa_index", store_directory="./store")  
  
# 将问题和处理结果添加到索引中  
for question, result in zip(questions, results):  
    # 创建文档对象  
    doc = Document()  
      
    # 添加问题字段  
    doc.add_field(Field("question", question, TextType()))  
      
    # 添加处理结果字段  
    doc.add_field(Field("result", result, TextType()))  
      
    # 将文档添加到索引中  
    index.add_document(doc)  
  
# 提交更改到索引  
index.commit()  
  
# 关闭索引以释放资源  
index.close()  
  
# 在此之后，你可以使用 Searcher 类来查询索引  
# ...

# 打开索引以进行搜索  
index = Index("lego_qa_index", store_directory="./store")  
  
# 创建查询器  
query_parser = QueryParser()  
  
# 执行查询  
query = "你的查询关键字"  
searcher = Searcher(index)  
results = searcher.search(query_parser.parse("question:" + query), limit=10)  
  
# 打印查询结果  
for result in results:  
    print(f"Score: {result.score}, Question: {result.document['question']}, Result: {result.document['result']}")  
  
# 关闭索引  
index.close()