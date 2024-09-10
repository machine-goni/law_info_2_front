# 서류작성 - 답변서 front-end

import streamlit as st
import json
import requests
#import pyperclip    # 클립보드 복사
import streamlit.components.v1 as components
import markdown2
from bs4 import BeautifulSoup


if st.session_state.init_backend == 200 and st.session_state.build != "write_paper_4":
    inputs = {"workflow_type": "write_paper_4"}
    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
    if result.status_code == 200:
        st.session_state.build = "write_paper_4"
    
elif st.session_state.init_backend != 200 and st.session_state.build != "write_paper_4":
    init_result = requests.post(url=f"{st.session_state.backend_url}init")
    st.session_state.init_backend = init_result.status_code
    
    if st.session_state.init_backend == 200:
        inputs = {"workflow_type": "write_paper_4"}
        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
        if result.status_code == 200:
            st.session_state.build = "write_paper_4"


if "disable_write_paper_4" not in st.session_state:
    st.session_state.disable_write_paper_4 = 0      # 0: 작성하기 답변받은적 없음, 1: 작성하기 첫답변 받음, 2: 작성하기 최종 완료
        
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
if "result_answer_post" not in st.session_state:
    st.session_state.result_answer_post = ""
    
if "input_info_dict" not in st.session_state:
    st.session_state.input_info_dict = {}
    

with st.sidebar:
    st.caption(":material/release_alert: 아래의 [대한민국법원-전자민원센터] 홈페이지를 통해 법적 절차 안내, 사건검색 등 여러정보를 얻을 수 있습니다.")
    st.page_link("https://help.scourt.go.kr/nm/main/index.html", label="전자민원센터", icon=":material/link:")


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">\"민사소송 소장에 대한 답변서\" 작성을 도와드립니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.text("")

st.subheader("민사소송의 답변서란?")
explain = """
민사소송법 제256조에 따르면, 피고는 원고의 주장을 반박하는 답변서를 소장을 받고 30일 이내에 제출해야 합니다.   

만약 이 기간 내에 답변서를 제출하지 않으면, 피고가 원고의 청구를 모두 인정한 것으로 간주되어 민사소송법 제257조 제1항에 따라 법원은 변론 없이 원고에게 승소 판결을 내릴 수 있습니다.   

이렇게 판결이 나오는 것을 무변론판결이라고 하는데, 즉 피고가 아무 답변을 하지 않으면 재판부는 '피고는 다툴의사가 없다'라고 판단하게 되고 결국 패소하는 결과로 이어질 수 있습니다.   

하지만 원고의 승소 판결이 즉시 내려지는 것은 아니닙다. 법원은 무변론 판결을 선고하는 날을 따로 정해서 판결을 하게 되는데 그 판결 선고일에 법원에 출석해 "나는 이 주장을 반박하겠다"는 의사를 밝히면, 변론기일을 다시 잡게 되고 정식으로 재판을 계속 진행할 수 있게 됩니다.   

결론적으로, 소송을 당했다면 답변서를 제때 제출하는 것이 매우 중요합니다.

참고로, 가사/행정소송의 경우에는 본질적으로 무변론판결이 허용되지 않기때문에 변론기일이 잡히게 됩니다.   

이 외에도 '상고이유서에 대한 답변서', '형사소송에서의 답변서', '행정심판에서의 답변서' 등도 있습니다.
"""
expander = st.expander("자세히 보기")
expander.write(explain)
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제256조", label="민사소송법 제256조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제257조", label="민사소송법 제257조 제1항", icon=":material/link:")

expander.info("답변서 양식은 [대한민국법원 전자민원센터]의 [양식모음]에서 받으실 수 있습니다.")
expander.page_link(f"https://help.scourt.go.kr/nm/minwon/doc/DocListAction.work?pageIndex=1&pageSize=5&min_gubun=&sName=&eName=&min_gubun_sel=&searchWord=%B4%E4%BA%AF%BC%AD", label="대한민국법원 전자민원센터 - 양식모음 - 답변서", icon=":material/link:")

st.text("")
st.warning("답변서 제출은 아래 주소의 [대한민국법원 전자소송] 홈페이지를 통해 온라인으로 제출할 수 있습니다([민사 본안] 탭의 [답변서] 또는 [지급명령(독촉) 신청] 탭의 하단 [지급명령 절차 관련] 부분 [답변서]).")
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF302.jsp")
st.caption("* [대한민국법원 전자소송] 저작권 정책상 URL을 알려드릴 뿐 링크를 제공하지 않음을 양해 바랍니다. 위 주소를 직접 주소창에 넣어 이동하시면 됩니다(혹은 드래그 후 우클릭).")

st.text("")


# 입력 사항
if st.session_state.disable_write_paper_4 == 0:
    st.info("아래의 입력사항은 받은 소장의 내용을 참조하여 기재 하세요.")
    st.text_input(label='원고 이름을 입력 하세요.', max_chars=20, key='user_input_sender_name', placeholder="예) 임꺽정")
    st.text_input(label='피고 이름을 입력 하세요.', max_chars=20, key='user_input_receiver_name', placeholder="예) 홍길동")

    st.text_input(label='사건번호를 입력 하세요.', max_chars=20, key='user_input_case_no', placeholder="예) 20 가")
    st.text_input(label='소 제목을 입력 하세요.', max_chars=50, key='user_input_case_name', placeholder="예) 대여금 청구의 소")
    st.text_area(label='청구취지를 모두 입력 하세요.', max_chars=500, key='user_input_case_purpose', placeholder="예) 피고는 원고에게 10,000,000원 및 이에 대하여... 등")
    st.text_area(label='청구원인을 모두 입력 하세요.', max_chars=1000, key='user_input_case_cause', placeholder="예) 원고는 2024년 4월 5일에 피고에게 금 10,000,000원을 변제기... 등")
    st.text_input(label='입증방법에 내용이 있다면 문서명을 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_case_prove', placeholder="예) 1. 갑 제1호증 거래내영서, 1. 갑 2호증 문자 메시지")
    st.text_input(label='첨부서류에 내용이 있다면 문서명을 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_case_appendix', placeholder="예) 소송 비용 납부서 각 1부, 소장부분 1부")
    st.text_input(label='관할법원을 입력 하세요.', max_chars=20, key='user_input_case_court', placeholder="예) 서울중앙지방법원")

    st.text("")
    st.warning("아래는 반박할 내용을 기재 하세요.")
    st.text_area(label='구체적인 사실과 반박 내용을 입력 하세요.', max_chars=500, key='user_input_rebut', placeholder="예) 실제로 돈을 빌린 것은 맞으나 빌린 돈을 갚는 대신 원고의 친구에게 내 차 소유권을 이전 하였음.")
    st.text_input(label='별도로 첨부할 증거 문서가 있다면 문서명을 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_appendix', placeholder="예) 차량 소유권 이전 증명서, 거래 내역 증명 서류")
    
else:
    input_info_title_1 = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 14px;">소장에 대한 입력정보</p>'
    st.markdown(input_info_title_1, unsafe_allow_html=True)
    st.text(f"원고: {st.session_state.input_info_dict.get('sender_name')}")
    st.text(f"피고: {st.session_state.input_info_dict.get('receiver_name')}")
    st.text(f"사건번호: {st.session_state.input_info_dict.get('case_no')}")
    st.text(f"소 제목: {st.session_state.input_info_dict.get('case_name')}")
    st.text(f"청구취지:\n{st.session_state.input_info_dict.get('case_purpose')}")
    st.text(f"청구원인:\n{st.session_state.input_info_dict.get('case_cause')}")
    st.text(f"입증방법: {st.session_state.input_info_dict.get('case_prove')}")
    st.text(f"첨부서류: {st.session_state.input_info_dict.get('case_appendix')}")
    st.text(f"관할법원: {st.session_state.input_info_dict.get('case_court')}")

    st.text("")
    input_info_title_2 = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 14px;">답변에 대한 입력정보</p>'
    st.markdown(input_info_title_2, unsafe_allow_html=True)
    st.text(f"사실과 반박:\n{st.session_state.input_info_dict.get('rebut')}")
    st.text(f"첨부문서: {st.session_state.input_info_dict.get('appendix')}")
    

content_input_limit = 4
def click_write_paper():
    if st.session_state.disable_write_paper_4 == 0:
        if (len(st.session_state.user_input_sender_name) == 0) or (len(st.session_state.user_input_receiver_name) == 0) \
        or (len(st.session_state.user_input_case_no) == 0) or (len(st.session_state.user_input_case_name) == 0) or (len(st.session_state.user_input_case_purpose) == 0) or (len(st.session_state.user_input_case_cause) == 0) or (len(st.session_state.user_input_case_court) == 0) \
        or (len(st.session_state.user_input_rebut) == 0):
            st.session_state.result_answer = "모든 입력란에 내용을 입력 하세요."
        
        elif (len(st.session_state.user_input_case_purpose) < content_input_limit) or (len(st.session_state.user_input_case_cause) < content_input_limit) or (len(st.session_state.user_input_case_court) < content_input_limit) or (len(st.session_state.user_input_rebut) < content_input_limit):
            st.session_state.result_answer = "내용이 너무 짧습니다."
            
        else:
            st.session_state.disable_write_paper_4 = 1
            st.session_state.hide_main_side = True
            
            case_prove = st.session_state.user_input_case_prove
            if "user_input_case_prove" not in st.session_state or len(st.session_state.user_input_case_prove) == 0:
                case_prove = "없음"
                
            case_appendix = st.session_state.user_input_case_appendix
            if "user_input_case_appendix" not in st.session_state or len(st.session_state.user_input_case_appendix) == 0:
                case_appendix = "없음"
                
            appendix = st.session_state.user_input_appendix
            if "user_input_appendix" not in st.session_state or len(st.session_state.user_input_appendix) == 0:
                appendix = "없음"
            
            user_inputs = {"is_post_conversation": False, "sender_name": st.session_state.user_input_sender_name, "receiver_name": st.session_state.user_input_receiver_name, \
            "case_no": st.session_state.user_input_case_no, "case_name": st.session_state.user_input_case_name, "case_purpose": st.session_state.user_input_case_purpose, "case_cause": st.session_state.user_input_case_cause, "case_prove": case_prove, "case_appendix": case_appendix, "case_court": st.session_state.user_input_case_court, \
            "rebut": st.session_state.user_input_rebut, "appendix": appendix, "add_info": "없음"}
            
            # 입력정보 저장
            st.session_state.input_info_dict = user_inputs
            
            # when the user clicks on button it will fetch the API
            result = requests.post(url=f"{st.session_state.backend_url}write-paper-4", data=json.dumps(user_inputs))
            rslt = json.loads(json.loads(result.text))
            st.session_state.result_answer = rslt.get('answer')
            
    elif st.session_state.disable_write_paper_4 == 1:
        st.session_state.disable_write_paper_4 = 2
        st.session_state.input_info_dict["is_post_conversation"] = True
        
        if "user_input_add_info" in st.session_state and len(st.session_state.user_input_add_info) > 0:
            st.session_state.input_info_dict["add_info"] = st.session_state.user_input_add_info
        
        # when the user clicks on button it will fetch the API
        result = requests.post(url=f"{st.session_state.backend_url}write-paper-4", data=json.dumps(st.session_state.input_info_dict))
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
if st.session_state.disable_write_paper_4 == 0 and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
    
elif st.session_state.disable_write_paper_4 == 1 and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text_area(label='AI가 요청한 추가 정보를 입력 하세요.', max_chars=500, key='user_input_add_info', placeholder="예) 차 소유권 이전을 증명할 차량 등록증이 있고 차량 소유권 이전으로 변제를 대신하기로 합의한 대화문자메세지 있음.")
    st.warning(st.session_state.result_warning_comment_2)
    
elif st.session_state.disable_write_paper_4 == 2 and len(st.session_state.result_answer_post) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text(f"추가 정보:\n{st.session_state.input_info_dict.get('add_info')}")
    st.success(st.session_state.result_answer_post)
    st.warning(st.session_state.result_warning_comment_2)


if st.session_state.disable_write_paper_4 == 0 or st.session_state.disable_write_paper_4 == 1:    
    st.button('작성하기', key='btn_send_question', on_click=click_write_paper, disabled=False)
    
    if st.session_state.disable_write_paper_4 == 1:
        st.button('처음으로', on_click=click_go_to_main)
    
elif st.session_state.disable_write_paper_4 == 2:
    # 클립보드 복사
    #if st.button(":material/content_copy: Copy"):
    #    pyperclip.copy(st.session_state.result_answer_post)
    #    st.info('복사되었습니다!')
        
    st.button('처음으로', on_click=click_go_to_main)
    
    copy_clipboard(st.session_state.result_answer_post)

