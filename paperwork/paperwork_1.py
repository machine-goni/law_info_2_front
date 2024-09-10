# 서류작성 - 내용증명 front-end

import streamlit as st
import json
import requests
import pyperclip    # 클립보드 복사


if st.session_state.init_backend == 200 and st.session_state.build != "write_paper_1":
    inputs = {"workflow_type": "write_paper_1"}
    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
    if result.status_code == 200:
        st.session_state.build = "write_paper_1"
    
elif st.session_state.init_backend != 200 and st.session_state.build != "write_paper_1":
    init_result = requests.post(url=f"{st.session_state.backend_url}init")
    st.session_state.init_backend = init_result.status_code
    
    if st.session_state.init_backend == 200:
        inputs = {"workflow_type": "write_paper_1"}
        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
        if result.status_code == 200:
            st.session_state.build = "write_paper_1"


if "disable_write_paper_1" not in st.session_state:
    st.session_state.disable_write_paper_1 = False
    
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
    
with st.sidebar:
    st.caption(":material/release_alert: 아래의 [대한민국법원-전자민원센터] 홈페이지를 통해 법적 절차 안내, 사건검색 등 여러정보를 얻을 수 있습니다.")
    st.page_link("https://help.scourt.go.kr/nm/main/index.html", label="전자민원센터", icon=":material/link:")


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">\"내용증명\" 작성을 도와드립니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.text("")

st.subheader("내용증명이란?")
explain = """
내용증명(內容證明)은 발신인이 작성한 문서를 우체국에 보내어, 해당 문서의 내용이 '언제', '누구에게' 발송되었는지를 우체국이 증명하는 제도입니다. 
이것은 민사소송 전에 상대방이 논쟁을 피하지 못하도록 사실관계를 확정짓는 중요한 법적 절차의 시작으로 자주 활용됩니다. 
실제로 강제집행을 수반하는 분쟁의 시작점이 되며, 갈등이 심화되기 전에 사전 조치를 취하는 역할을 합니다.

법적 근거로는 우편법 시행규칙 제46조에 규정되어 있으며, 내용증명 문서는 한글, 한자 또는 외국어로 명확히 기재된 문서에 한하여 취급됩니다.
내용증명의 정해진 형식은 없으나 요건을 충족해야하며 내용이 공공의 질서나 선량한 풍속에 반하지 않아야 하고, 문서가 명확히 식별 가능해야 합니다.

내용증명을 보내기 위해서는 동일한 내용의 문서 3통이 필요합니다(복사본도 가능). 이 중 1통은 우체국이 보관하고, 1통은 발신자가 보관하며, 나머지 1통은 수신자에게 발송됩니다. 
우체국은 발송된 문서를 3년간 보관하며, 발신인은 이 기간 내에 열람이나 재증명 등을 요청할 수 있습니다. 
인터넷을 통한 전자문서 발송이나 우체국에서 직접 발송 절차를 안내받을 수 있습니다.
여러 수신인을 대상으로 하는 경우에는 각각의 수신인에게 별도의 문서를 발송해야 합니다. 

내용증명의 필요성은 법적 권리와 의무의 변동 상황에서 의사표시의 증명 문제가 발생하기 때문입니다. 
일반적인 서면 증명은 수신자에게 동일한 내용이 도달했음을 입증하기 어려운데 비해, 내용증명은 발송 및 수신일을 명확히 증명합니다. 
이는 상대방이 의사표시에 대해 타당한 응답을 하지 않았을 경우, 소송에서 유리한 입증자료로 활용될 수 있습니다.

내용증명은 보통 법적 조치를 취하기 전의 최후 통첩으로 활용되며, 상대방이 서류를 받았다고해도 이에 대한 이행을 강제할 수 있는 것은 아니므로, 제도적 한계가 있습니다.
따라서 내용증명의 내용에 위협적인 문장이 있다하더라도 그 내용이 실현되는 것은 소송절차를 밟고 법원이 받아들였을때 입니다. 하지만 앞서 말했듯이 법적 조치로 이어질 수 있기 때문에 법률전문가와 상담하거나 상대방과 문제해결을 위한 합의 시도 또는 본인의 입장을 밝히는 내용증명 발신 등의 행동을 취하는 것이 좋을 수 있습니다.

이와같이 내용증명은 법적 분쟁을 예방하고, 상대방과의 원활한 소통이 어려운 경우에 유용한 수단으로 자리 잡고 있습니다.
"""
expander = st.expander("자세히 보기")
expander.write(explain)
expander.page_link(f"https://www.law.go.kr/법령/우편법시행규칙/(20240724,00129,20240724)/제46조", label="우편법 시행규칙 제46조", icon=":material/link:")
expander.page_link(f"https://service.epost.go.kr/econprf.RetrieveEConprfReqSend.postal?type=&grp=A", label="인터넷우체국 내용증명", icon=":material/link:")
expander.page_link(f"https://service.epost.go.kr/econprf.RetrieveCertForm.postal#", label="인터넷우체국 내용증명 양식 다운로드", icon=":material/link:")


# 입력 사항. 내용증명은 다른데서 뺀 개인정보를 그냥 입력받는다.
st.text_area(label='내용증명을 보내는 이유(목적)에 대해 입력 하세요.', max_chars=200, key='user_input_reason', placeholder="예) 상대방이 약속한 대금 지급을 이행하지 않았다.")
st.text_area(label='사실 관계에 대한 구체적인 내용을 입력 하세요.', max_chars=500, key='user_input_fact', placeholder="예) 2024년 4월 4일에 계약을 체결했고, 1개월 이내에 대금 지급을 완료하기로 했다.")
st.text_area(label='상대방에게 요구할 구체적인 사항을 입력 하세요.', max_chars=200, key='user_input_ask', placeholder="예) 2024년 7월 4일까지 대금 500만원을 지급하라.")
st.text_area(label='강조할 사항을 입력 하세요.', max_chars=100, key='user_input_point', placeholder="예) 대금 지급이 되지 않을시 법적 책임을 물을 것이라는 내용 강조")

st.text_input(label='내용증명을 보내는 사람의  이름과 주소를 입력 하세요.', max_chars=50, key='user_input_sender', placeholder="예) 임꺽정, 서울시 강남구 테헤란로 456")
st.text_input(label='상대방이 연락할 수 있는 보내는 사람의 연락처를 입력 하세요.', max_chars=50, key='user_input_phone', placeholder="예) 전화번호:010-1234-5678, 이메일:xxxxx@yyyyy.com")
st.text_input(label='내용증명을 받을 사람의 이름과 주소를 입력 하세요.', max_chars=50, key='user_input_receiver', placeholder="예) 홍길동, 서울시 강남구 테헤란로 123")

st.text_input(label='별도로 첨부할 문서가 있다면 문서명을 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_appendix', placeholder="예) 차용증1, 차용증2 혹은 없음")
st.selectbox('어조를 선택하세요.', ('강한 어조', '정중한 어조', '부드럽고 완곡한 어조'), key='user_input_style')

content_input_limit = 4
def click_write_paper():
    if st.session_state.disable_write_paper_1 == False:
        if (len(st.session_state.user_input_reason) == 0) or (len(st.session_state.user_input_fact) == 0) or (len(st.session_state.user_input_ask) == 0) or (len(st.session_state.user_input_point) == 0) or (len(st.session_state.user_input_receiver) == 0) or (len(st.session_state.user_input_sender) == 0) or (len(st.session_state.user_input_phone) == 0):
            st.session_state.result_answer = "모든 입력란에 내용을 입력 하세요."
        elif (len(st.session_state.user_input_reason) < content_input_limit) or (len(st.session_state.user_input_fact) < content_input_limit) or (len(st.session_state.user_input_ask) < content_input_limit) or (len(st.session_state.user_input_point) < content_input_limit) or (len(st.session_state.user_input_receiver) < content_input_limit) or (len(st.session_state.user_input_sender) < content_input_limit) or (len(st.session_state.user_input_phone) < content_input_limit):
            st.session_state.result_answer = "내용이 너무 짧습니다."
        else:
            st.session_state.disable_write_paper_1 = True
            # hide_main_side 의 셋팅은 타이밍이 중요하다. 화면(사이드바)이 갱신된 후에 변수가 바뀌면 다음 동작까지는 화면이 그대로 있는다.
            st.session_state.hide_main_side = True
            
            appendix = st.session_state.user_input_appendix
            if "user_input_appendix" not in st.session_state or len(st.session_state.user_input_appendix) == 0:
                appendix = "없음"
            
            # when the user clicks on button it will fetch the API
            user_inputs = {"reason": st.session_state.user_input_reason, "fact": st.session_state.user_input_fact, "ask": st.session_state.user_input_ask, "point": st.session_state.user_input_point, "receiver": st.session_state.user_input_receiver, "sender": st.session_state.user_input_sender, "phone": st.session_state.user_input_phone, "appendix": appendix, "style": st.session_state.user_input_style}
            result = requests.post(url=f"{st.session_state.backend_url}write-paper-1", data=json.dumps(user_inputs))
            rslt = json.loads(json.loads(result.text))
            st.session_state.result_answer = rslt.get('answer')
            
    
if st.session_state.disable_write_paper_1 == False:    
    st.button('작성하기', key='btn_send_question', on_click=click_write_paper, disabled=False)


def click_go_to_main():
    # job 만 비워줘도 버튼이 눌리는 동작과 함께 streamlit_app.py 가 재실행되고 스크립트 끝부분을 통해 start_task 페이지가 실행된다.
    st.session_state.job = None
    

# 결과 출력
if st.session_state.disable_write_paper_1 == False and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
elif st.session_state.disable_write_paper_1 and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    st.warning(st.session_state.result_warning_comment_2)

    # 클립보드 복사
    if st.button(":material/content_copy: Copy"):
        pyperclip.copy(st.session_state.result_answer)
        st.info('복사되었습니다!')
        
    # 현시점 유일한 페이지 이동 인터페이스
    st.button('처음으로', on_click=click_go_to_main)

