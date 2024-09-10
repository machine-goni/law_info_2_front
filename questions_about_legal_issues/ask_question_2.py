# 법률 조언 front-end

import streamlit as st
import streamlit.components.v1 as components
import json
import requests
#import pyperclip    # 클립보드 복사
import markdown2
from bs4 import BeautifulSoup


if st.session_state.init_backend == 200 and st.session_state.build != "advice":
    inputs = {"workflow_type": "advice"}
    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
    if result.status_code == 200:
        st.session_state.build = "advice"
    
elif st.session_state.init_backend != 200 and st.session_state.build != "advice":
    init_result = requests.post(url=f"{st.session_state.backend_url}init")
    st.session_state.init_backend = init_result.status_code
    
    if st.session_state.init_backend == 200:
        inputs = {"workflow_type": "advice"}
        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
        if result.status_code == 200:
            st.session_state.build = "advice"


# 사이드바
with st.sidebar:
    st.header('국가법령정보센터')
    st.page_link(f"https://www.law.go.kr/lsSc.do?menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060114", label="법령 찾기", icon=":material/link:")
    st.page_link(f"https://www.law.go.kr/lsTrmSc.do?menuId=13&subMenuId=65", label="법령용어찾기", icon=":material/link:")
    
    st.divider()
    st.caption("[출처] 여기서 보여지는 통계자료는 'e-나라지표' 에서 제공되었습니다.")
    
    
if "disable_advice" not in st.session_state:
    st.session_state.disable_advice = 0      # 0: 답변받은적 없음, 1: 첫답변 받음, 2: 최종 답변
        
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
if "result_answer_post" not in st.session_state:
    st.session_state.result_answer_post = ""
    
if "input_info_dict" not in st.session_state:
    st.session_state.input_info_dict = {}
    

new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">현재 상황에 대한 법률 조언을 제공합니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.caption('현재의 상황과 질문을 입력하시면 AI가 답변합니다.')
st.caption('예) 고소를 당한 상황, 소송을 당한 상황, 법적 조치를 취하려는 상황 등')
st.text("")


# 입력 사항
if st.session_state.disable_advice == 0:
    st.text_area(label='질문의 배경이 되는 현재의 상황을 상세히 설명해 주세요.', max_chars=1500, key='user_input_status', placeholder="예) 상대방과 금전거래를 한 적이 없는데 상대방이 법원에 물품 대금 10,000,000원에 대한 지급명령신청을 하였습니다.")
    st.text_area(label='현재의 상황에서 궁금하거나 하려고 하는 부분을 입력하세요.', max_chars=500, key='user_input_question', placeholder="예) 어떻게 대응해야 할까요?")
    
else:
    input_info_title_1 = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 14px;">입력정보</p>'
    st.markdown(input_info_title_1, unsafe_allow_html=True)
    st.text(f"상황: {st.session_state.input_info_dict.get('status')}")
    st.text(f"질문: {st.session_state.input_info_dict.get('question')}")
    

content_input_limit = 4
def click_write_paper():
    if st.session_state.disable_advice == 0:
        if (len(st.session_state.user_input_status) == 0) or (len(st.session_state.user_input_question) == 0):
            st.session_state.result_answer = "모든 입력란에 내용을 입력 하세요."
        
        elif (len(st.session_state.user_input_status) < content_input_limit) or (len(st.session_state.user_input_question) < content_input_limit):
            st.session_state.result_answer = "내용이 너무 짧습니다."
            
        else:
            st.session_state.disable_advice = 1
            st.session_state.hide_main_side = True
                
            user_inputs = {"is_post_conversation": False, \
            "status": st.session_state.user_input_status, "question": st.session_state.user_input_question, \
            "add_info": "없음"}
            
            # 입력정보 저장
            st.session_state.input_info_dict = user_inputs
            
            # when the user clicks on button it will fetch the API
            result = requests.post(url=f"{st.session_state.backend_url}advice", data=json.dumps(user_inputs))
            rslt = json.loads(json.loads(result.text))
            st.session_state.result_answer = rslt.get('answer')
            
    elif st.session_state.disable_advice == 1:
        st.session_state.disable_advice = 2
        st.session_state.input_info_dict["is_post_conversation"] = True
        
        if "user_input_add_info" in st.session_state and len(st.session_state.user_input_add_info) > 0:
            st.session_state.input_info_dict["add_info"] = st.session_state.user_input_add_info
        
        # when the user clicks on button it will fetch the API
        result = requests.post(url=f"{st.session_state.backend_url}advice", data=json.dumps(st.session_state.input_info_dict))
        rslt = json.loads(json.loads(result.text))
        st.session_state.result_answer_post = rslt.get('answer')
        
        
def click_go_to_main():
    # job 만 비워줘도 버튼이 눌리는 동작과 함께 streamlit_app.py 가 재실행되고 스크립트 끝부분을 통해 start_task 페이지가 실행된다.
    st.session_state.job = None
    
    
def copy_clipboard(markdown_text):
    # Markdown을 HTML로 변환
    html_text = markdown2.markdown(markdown_text)

    # HTML을 일반 텍스트로 변환
    soup = BeautifulSoup(html_text, 'html.parser')
    plain_text = soup.get_text()

    # HTML과 JavaScript를 사용하여 클립보드 복사 버튼을 생성
    copy_button = f"""
        <button onclick="copyToClipboard()"> Copy </button>
        <script>
            function copyToClipboard() {{
                const text = `{plain_text}`;
                navigator.clipboard.writeText(text).then(function() {{
                    console.log('Async: Copying to clipboard was successful!');
                }}, function(err) {{
                    console.error('Async: Could not copy text: ', err);
                }});
            }}
        </script>
    """
    # Streamlit Component에 HTML을 렌더링
    components.html(copy_button)


# 결과 출력
if st.session_state.disable_advice == 0 and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
    
elif st.session_state.disable_advice == 1 and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text_area(label='AI가 요청한 추가 정보를 입력 하세요.', max_chars=500, key='user_input_add_info')
    st.warning(st.session_state.result_warning_comment_1)
    
elif st.session_state.disable_advice == 2 and len(st.session_state.result_answer_post) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text(f"추가 정보:\n{st.session_state.input_info_dict.get('add_info')}")
    st.success(st.session_state.result_answer_post)
    st.info("혹시 원하는 답변이 아니라면 단어나 질문을 바꿔서 시도해 보세요.")
    st.warning(st.session_state.result_warning_comment_1)
    
    # 클립보드 복사
    #if st.button(":material/content_copy: Copy"):
    #    pyperclip.copy(st.session_state.result_answer_post)
    #    st.info('복사되었습니다!')
        
    st.button('처음으로', on_click=click_go_to_main)
    
    copy_clipboard(st.session_state.result_answer_post)
        
    st.divider()
    st.info('상담이 필요하지만 상황이 여의치 않을 경우 법률구조법에 따라 설립된 "대한법률구조공단"에서 법률 상담을 받을 수 있습니다.')
    st.page_link(f"https://www.klac.or.kr", label="대한법률구조공단 홈페이지", icon=":material/link:")
    #components.iframe(statistics_result_url[2], width=700, height=630, scrolling=True)
    components.iframe("https://www.index.go.kr/unity/openApi/chartUserShow.do?idntfcId=53B2F01062E204W6&ixCode=2479&statsCode=247901&chartNo=1", width=700, height=700, scrolling=True)
    components.iframe("https://www.index.go.kr/unity/openApi/meanAnaly.do?idntfcId=53B2F01062E204W6&ixCode=2479", width=700, height=700, scrolling=True)


if st.session_state.disable_advice == 0 or st.session_state.disable_advice == 1:    
    st.button('질문하기', key='btn_send_question', on_click=click_write_paper, disabled=False)
    
    if st.session_state.disable_advice == 1: 
        st.button('처음으로', on_click=click_go_to_main)

