import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="笔记本调研助手", layout="wide")
st.title("💻 笔记本竞品自动调研助手 (增强版)")

# 侧边栏
st.sidebar.header("核心设置")
api_key = st.sidebar.text_input("第一步：在此输入 API Key", type="password")

if api_key:
    try:
        # 初始化
        genai.configure(api_key=api_key)
        # 尝试切换更稳定的模型版本
        model = genai.GenerativeModel('gemini-1.5-pro') 

        st.info("💡 建议：打开 DNS.ru 网页，Ctrl+A 全选，Ctrl+C 复制，然后贴到下面。")
        raw_text = st.text_area("第二步：粘贴参数文本", height=300, placeholder="在此粘贴网页内容...")

        if st.button("第三步：开始自动调研"):
            if not raw_text:
                st.warning("请先粘贴文本内容！")
            else:
                with st.spinner('AI 正在分析，请稍候...'):
                    # 编写指令
                    prompt = f"你是一个笔记本参数专家。请从以下文本中提取22项参数（Model Name, Screen Size, Screen Type, CPU, GPU, DDR, Hard Drive, Battery, Adapter, Camera, Sound, WiFi, Bluetooth, HDMI port, Fingerprint, Body Material, Backlit keyboard, Weight, Thickness, Pre-installed OS, Size, RRP），并以Markdown表格输出。文本内容：\n\n{raw_text}"
                    
                    # 尝试调用并捕获错误
                    try:
                        response = model.generate_content(prompt)
                        st.markdown("### ✅ 调研结果")
                        st.markdown(response.text)
                    except Exception as ai_err:
                        # 这里会直接告诉你为什么失败
                        st.error(f"AI 调用失败了，具体原因：{str(ai_err)}")
                        st.info("常见提示：如果是 'User location is not supported'，说明你需要开启代理或更换节点。")

    except Exception as init_err:
        st.error(f"初始化失败：{str(init_err)}")
else:
    st.info("🔑 请在左侧输入 API Key 开始使用。")
