import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import tempfile
import os

# 启用中文字符显示支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

def main():
    st.title("成绩数据分析")

    # 上传文件功能，允许用户上传Excel格式的成绩数据
    uploaded_file = st.file_uploader("上传您的成绩数据（Excel格式）", type=["xls", "xlsx"])
    if uploaded_file is not None:
        # 使用临时文件保存上传的文件，确保在多用户环境下的文件隔离
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            tmp.write(uploaded_file.getvalue())
            uploaded_file_path = tmp.name
        
        df = pd.read_excel(uploaded_file_path, skiprows=3)

        st.write("原始数据预览：")
        st.dataframe(df)  # 显示所有数据

        # 数据编辑功能：允许用户输入行号进行编辑
        st.subheader("编辑成绩数据")
        row_number = st.number_input("输入要编辑的行号（从0开始）", min_value=0, max_value=len(df)-1, step=1, format="%d")
        
        if st.button("加载行数据"):
            # 加载选定行的数据到表单
            row_data = df.iloc[row_number]
            edit_form(row_data, row_number, uploaded_file_path, df)

        # 手动添加成绩的功能
        add_grades_manually(df, uploaded_file_path)

        # 分析和显示数据
        analyze_and_display_data(df)

def add_grades_manually(df, file_path):
    """手动添加成绩"""
    st.subheader("手动批量添加成绩")
    num_courses = st.number_input("您要添加几门课程的成绩？", min_value=0, max_value=10, step=1)

    new_data = []
    for i in range(num_courses):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                course_name = st.text_input(f"课程名称{i+1}", key=f"name{i+1}")
            with col2:
                score = st.number_input(f"成绩{i+1}", min_value=0.0, max_value=100.0, step=0.1, key=f"score{i+1}")
            with col3:
                credit = st.number_input(f"学分{i+1}", min_value=0.0, step=0.1, key=f"credit{i+1}")
            with col4:
                gpa = st.number_input(f"绩点{i+1}", min_value=0.0, max_value=5.0, step=0.1, key=f"gpa{i+1}")
            with col5:
                course_type = st.selectbox(f"课程属性{i+1}", ["必修", "任选"], key=f"type{i+1}")
            new_data.append([course_name, score, credit, gpa, course_type])

    if st.button("添加成绩"):
        new_df = pd.DataFrame(new_data, columns=["课程名称", "成绩", "学分", "绩点", "课程属性"])
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_excel(file_path, index=False)  # 保存到原始文件
        st.success("成绩已添加并保存到文件。")
        st.dataframe(updated_df)  # 显示更新后的所有数据

def edit_form(row_data, row_number, file_path, df):
    """显示编辑表单并处理数据保存"""
    with st.form(key="edit_row"):
        course_name = st.text_input("课程名称", value=row_data['课程名称'])
        score = st.number_input("成绩", value=float(row_data['成绩']))
        credit = st.number_input("学分", value=float(row_data['学分']))
        gpa = st.number_input("绩点", value=float(row_data['绩点']))
        course_type = st.selectbox("课程属性", ["必修", "任选"], index=["必修", "任选"].index(row_data['课程属性']))

        submit_button = st.form_submit_button(label="保存更改")
        if submit_button:
            # 更新DataFrame
            df.loc[row_number, '课程名称'] = course_name
            df.loc[row_number, '成绩'] = score
            df.loc[row_number, '学分'] = credit
            df.loc[row_number, '绩点'] = gpa
            df.loc[row_number, '课程属性'] = course_type
            # 保存到文件
            df.to_excel(file_path, index=False)
            st.success(f"行{row_number}的数据已更新。")
            st.dataframe(df)  # 显示更新后的数据

def analyze_and_display_data(df):
    """进行数据分析并显示结果"""
    # 确保所有必要的列都存在
    if '绩点' not in df.columns:
        st.error("错误：数据中缺少'绩点'列。")
        return

    # 数据处理，排除学分为0或成绩为“通过”的记录
    df = df[(df['学分'] != 0) & (df['成绩'] != '通过')]
    df['成绩'] = df['成绩'].replace('免修', '90').astype(float)  # 将“免修”转换为90分
    required_courses = df[df['课程属性'] == '必修']

    # 计算平均学分绩点和平均成绩
    total_credits = sum(df['学分'])
    if total_credits > 0:
        total_gpa = sum(df['学分'] * df['绩点'])
        average_gpa = total_gpa / total_credits
        average_score = sum(df['成绩'] * df['学分']) / total_credits
    else:
        average_gpa = float('nan')
        average_score = float('nan')

    # 对必修课程进行相同的处理
    total_credits_required = sum(required_courses['学分'])
    if total_credits_required > 0:
        total_gpa_required = sum(required_courses['学分'] * required_courses['绩点'])
        average_gpa_required = total_gpa_required / total_credits_required
        average_score_required = sum(required_courses['成绩'] * required_courses['学分']) / total_credits_required
    else:
        average_gpa_required = float('nan')
        average_score_required = float('nan')
    
    # 显示计算结果
    st.write(f"整体的百分制加权平均分为: {average_score:.2f}")
    st.write(f"必修课的百分制加权平均分为: {average_score_required:.2f}")
    st.write(f"整体平均学分绩点为: {average_gpa:.2f}")
    st.write(f"必修课的平均学分绩点为: {average_gpa_required:.2f}")
    st.write(f"保研中必修课的得分为（满分80): {average_score_required * 0.8:.2f}")
    
    # 数据可视化
    fig, ax = plt.subplots()
    df.groupby('课程属性')['成绩'].mean().plot(kind='bar', ax=ax)
    ax.set_title("不同课程属性的平均成绩")
    ax.set_ylabel("平均成绩")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
