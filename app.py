import streamlit as st
import google.generativeai as genai
import pandas as pd
import io

st.set_page_config(page_title="笔记本调研助手", layout="wide")
st.title("💻 笔记本竞品自动调研助手 (稳定版)")

# 侧边栏
st.sidebar.header("核心设置")
api_key = st.sidebar.text_input("第一步：在此输入 API Key", type="password")

if api_key:
    try:
        # 初始化
        genai.configure(api_key=api_key)
        # 使用更兼容、更快速的 gemini-1.5-flash 模型
        model = genai.GenerativeModel('gemini-1.5-flash') 

        st.info("💡 建议：打开网页后按 Ctrl+A 全选，Ctrl+C 复制，然后贴到下面。")
        raw_text = st.text_area("第二步：粘贴参数文本", height=300, placeholder="在此粘贴网页内容...")

        if st.button("第三步：开始自动调研"):
            if not raw_text:
                st.warning("请先粘贴文本内容！")
            else:
                with st.spinner('AI 正在提取参数，请稍候...'):
                    # 编写指令，要求返回 Markdown 表格
                    prompt = f"你是一个笔记本参数专家。请从以下文本中提取22项参数（Model Name, Screen Size, Screen Type, CPU, GPU, DDR, Hard Drive, Battery, Adapter, Camera, Sound, WiFi, Bluetooth, HDMI port, Fingerprint, Body Material, Backlit keyboard, Weight, Thickness, Pre-installed OS, Size, RRP）。只返回一个 Markdown 表格，不要说多余的话。文本内容：\n\n{raw_text}"
                    
                    try:
                        response = model.generate_content(prompt)
                        result_text = response.text
                        
                        st.markdown("### ✅ 调研结果")
                        st.markdown(result_text)
                        
                        st.success("分析完成！你可以直接选中上方的表格内容复制到 Excel 中。")
                        
                    except Exception as ai_err:
                        st.error(f"AI 调用失败，具体原因：{str(ai_err)}")
                        if "location" in str(ai_err).lower():
                            st.warning("⚠️ 提示：检测到地区限制。请确保你的网络代理已开启，并切换到美国、日本或新加坡节点，然后刷新页面重试。")

    except Exception as init_err:
        st.error(f"系统初始化失败：{str(init_err)}")
else:
    st.info("🔑 请在左侧输入 API Key 开始使用。")
