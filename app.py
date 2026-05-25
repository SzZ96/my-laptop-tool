import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="笔记本调研助手", layout="wide")
st.title("💻 笔记本竞品自动调研助手 (终极兼容版)")

# 侧边栏
st.sidebar.header("设置")
api_key = st.sidebar.text_input("第一步：输入你的 API Key", type="password")

if api_key:
    try:
        # 配置 API
        genai.configure(api_key=api_key)
        
        # 定义一个“大脑”列表，如果第一个不行，自动换第二个
        # 很多 404 错误是因为名字不对，我们尝试最常用的几个名字
        model_names = ['gemini-1.5-flash', 'gemini-pro']
        
        st.info("💡 提示：在网页全选 (Ctrl+A) -> 复制 (Ctrl+C) -> 在下方粘贴 (Ctrl+V)。")
        raw_text = st.text_area("第二步：粘贴网页文本内容", height=300)

        if st.button("第三步：开始自动调研"):
            if not raw_text:
                st.warning("请先粘贴内容！")
            else:
                success = False
                for m_name in model_names:
                    try:
                        with st.spinner(f'正在使用模型 {m_name} 尝试分析...'):
                            model = genai.GenerativeModel(m_name)
                            prompt = f"你是一个笔记本专家。请从以下文本中提取参数（Model Name, Screen Size, Screen Type, CPU, GPU, DDR, Hard Drive, Battery, Adapter, Camera, Sound, WiFi, Bluetooth, HDMI port, Fingerprint, Body Material, Backlit keyboard, Weight, Thickness, Pre-installed OS, Size, RRP），并输出Markdown表格。不要说废话。内容：\n\n{raw_text}"
                            response = model.generate_content(prompt)
                            
                            st.markdown("### ✅ 调研结果已生成")
                            st.markdown(response.text)
                            st.success(f"调用成功！(使用的是 {m_name} 模型)")
                            success = True
                            break # 成功了就跳出循环
                    except Exception as e:
                        # 如果这个名字报错 404，就打印出来尝试下一个
                        st.write(f"尝试模型 {m_name} 失败，准备切换下一个...")
                        continue
                
                if not success:
                    st.error("所有模型尝试均失败。请检查：1. API Key是否正确；2. 是否开启了全局网络代理。")

    except Exception as init_err:
        st.error(f"系统启动错误：{init_err}")
else:
    st.info("🔑 请在左侧输入 API Key。")
