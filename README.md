# gpa-calculator
本项目提供了一个基于 Web 的 GPA 计算器，使用 Streamlit 构建。它允许用户上传他们的课程成绩（Excel 格式），直接在网页界面编辑数据，并根据不同的课程类型计算 GPA。

## 功能

- **上传 Excel 文件**：上传你的课程成绩的 Excel 文件。
- **数据可视化**：通过条形图可视化平均分数和 GPA。
- **数据编辑**：在网页界面直接修改你的课程数据。
- **手动添加成绩**：手动输入课程详情以计算 GPA。
- **全面的 GPA 分析**：计算整体及必修课的 GPA 和分数。

## 安装

运行此项目前，你需要在系统上安装 Python。该项目使用了 Streamlit、Pandas 和 Matplotlib 等库。
1. 克隆此仓库：
   ```bash
   git clone https://github.com/yourusername/gpa-calculator.git #需要修改
   cd gpa-calculator #需要修改
2. 安装所需的包：
    pip install -r requirements.txt
3. 运行应用程序：
    streamlit run app.py

启动应用程序后，在你的网页浏览器中访问 http://localhost:8501。系统会提示你上传一个包含课程成绩的 Excel 文件。应用程序提供查看数据、编辑行、手动添加课程和可视化 GPA 统计的功能。

所需环境
Python 3.x
Streamlit
Pandas
Matplotlib
Openpyxl
具体版本请见 requirements.txt。