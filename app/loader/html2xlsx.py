from bs4 import BeautifulSoup
import pandas as pd
import os

# HTML文件路径（也可以是一个URL）
html_file_path = 'static/lego-qa.html'

print("Current Working Directory:", os.getcwd())
# 读取HTML内容
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到HTML中的第一个<table>元素
table = soup.find('table')

# 如果找到了表格
if table:
    # 初始化空列表来存储每一行的数据
    rows_data = []
    # 遍历表格中的所有行<tr>
    for row in table.find_all('tr'):
        # 获取当前行的所有单元格数据
        row_data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
        if len(row_data) >= 3 and any(row_data) and row_data[2]:  # 假设 '提问' 列在第三列
          # 将当前行数据添加到列表中
          rows_data.append(row_data)
    # 将数据转换为pandas DataFrame
    df = pd.DataFrame(rows_data[1:], columns=rows_data[0])

    # 将DataFrame保存到Excel文件
    excel_file_path = 'static/lego-qa.xlsx'
    df.to_excel(excel_file_path, index=False)
    
    print(f'Table has been successfully saved to {excel_file_path}')
else:
    print('No tables found')