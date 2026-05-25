import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="笔记本调研专家", layout="wide")
st.title("💻 笔记本竞品自动调研助手 (诊断修复版)")

# 侧边栏
st.sidebar.header("核心设置")
api_key = st.sidebar.text_input("第一步：输入你的 API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 尝试三个最常用的模型名字
        model_list = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-1.0-pro']
        
        st.info("💡 请全选复制网页内容并粘贴：")
        raw_text = st.text_area("第二步：粘贴网页文本", height=200)

        if st.button("第三步：开始自动调研"):
            if not raw_text:
                st.warning("请先粘贴内容！")
            else:
                any_success = False
                for m_name in model_list:
                    try:
                        with st.spinner(f'正在尝试使用 {m_name}...'):
                            model = genai.GenerativeModel(m_name)
                            # 缩短 Prompt 确保不超限
                            prompt = f"Extract laptop specs as a Markdown table. Text: {raw_text[:5000]}"
                            response = model.generate_content(prompt)
                            
                            st.markdown("### ✅ 调研结果")
                            st.markdown(response.text)
                            st.success(f"成功！模型名称：{m_name}")
                            any_success = True
                            break
                    except Exception as e:
                        # 重点：把具体的错误原因显示出来
                        st.error(f"❌ 模型 {m_name} 失败。具体报错：{str(e)}")
                
                if not any_success:
                    st.divider()
                    st.markdown("### 🔍 故障排查建议：")
                    st.write("1. 如果报错包含 **'User location is not supported'**：说明你的上网环境（加速器节点）不行，请换成**美国或新加坡**。")
                    st.write("2. 如果报错包含 **'API_KEY_INVALID'**：说明你的 Key 复制错了，请去 Google AI Studio 重新生成一个。")
                    st.write("3. 如果报错包含 **'quota'**：说明你用得太频繁，被限流了。")

    except Exception as init_err:
        st.error(f"系统启动失败：{init_err}")
else:
    st.info("🔑 请在左侧输入 API Key。")
