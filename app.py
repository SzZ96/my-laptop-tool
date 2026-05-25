import streamlit as st
import google.generativeai as genai
import pandas as pd

# 网页标题
st.set_page_config(page_title="笔记本调研助手", layout="wide")
st.title("💻 笔记本竞品自动调研助手")

# 侧边栏配置
st.sidebar.header("设置")
api_key = st.sidebar.text_input("第一步：输入你的 API Key", type="password")

if api_key:
    # 初始化 AI
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 用户操作区
    st.write("请将 DNS.ru 网页上的所有参数文字‘全选-复制’，然后粘贴在下方：")
    raw_text = st.text_area("第二步：粘贴参数文本", height=300)

    if st.button("第三步：开始自动调研"):
        if raw_text:
            with st.spinner('AI 正在疯狂分析中...'):
                # 固定的调研技能指令
                prompt = f"""
                你是一个笔记本参数专家。请从下面的文本中提取出这22项参数，严格对应：
                Model Name, Screen Size, Screen Type, CPU, GPU, DDR, Hard Drive, Battery, Adapter, Camera, Sound, WiFi, Bluetooth, HDMI port, Fingerprint, Body Material, Backlit keyboard, Weight, Thickness, Pre-installed OS, Size, RRP。
                
                文本内容如下：
                {raw_text}
                
                请直接以 Markdown 表格形式输出结果。
                """
                # 获取 AI 结果
                response = model.generate_content(prompt)
                st.markdown("### ✅ 调研结果已生成")
                st.markdown(response.text)
                st.success("分析完成！你可以直接复制表格到 Excel 中。")
        else:
            st.error("请先粘贴一些文本内容！")
else:
    st.info("💡 请先在左侧输入你在 Google AI Studio 获取的 API Key。")
