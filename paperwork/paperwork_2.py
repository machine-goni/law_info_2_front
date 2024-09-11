# 서류작성 - 지급명령신청서 front-end

import streamlit as st
import json
import requests
#import pyperclip    # 클립보드 복사
import streamlit.components.v1 as components
import markdown2
from bs4 import BeautifulSoup


if st.session_state.init_backend == 200 and st.session_state.build != "write_paper_2":
    inputs = {"workflow_type": "write_paper_2"}
    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
    if result.status_code == 200:
        st.session_state.build = "write_paper_2"
    
elif st.session_state.init_backend != 200 and st.session_state.build != "write_paper_2":
    init_result = requests.post(url=f"{st.session_state.backend_url}init")
    st.session_state.init_backend = init_result.status_code
    
    if st.session_state.init_backend == 200:
        inputs = {"workflow_type": "write_paper_2"}
        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
        if result.status_code == 200:
            st.session_state.build = "write_paper_2"


if "disable_write_paper_2" not in st.session_state:
    st.session_state.disable_write_paper_2 = False
    
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
    
with st.sidebar:
    st.caption(":material/release_alert: 아래의 [대한민국법원-전자민원센터] 홈페이지를 통해 법적 절차 안내, 사건검색 등 여러정보를 얻을 수 있습니다.")
    st.page_link("https://help.scourt.go.kr/nm/main/index.html", label="전자민원센터", icon=":material/link:")


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">\"지급명령신청서\" 작성을 도와드립니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.text("")

st.subheader("지급명령이란?")
explain = """
지급명령은 민사소송법 제5편에 규정된 독촉절차의 일종으로, 금전의 지급을 요구하는 경우에 간편하고 저렴한 방법으로 집행권원을 얻는 절차입니다. 
지급명령을 신청하면, 그 주장만으로도 이유가 있으면 법원이 이를 인정해주며, 인지대도 소송의 1/10에 불과해 비용 부담이 적습니다. 
지급명령이 확정되면 일반적인 판결과는 달리 추가적인 서류 없이 바로 강제집행이 가능하다는 점이 큰 장점입니다. 
그러나 지급명령은 집행력은 있지만 기판력이 없기 때문에(지급명령은 판사가 아닌 사법보좌관이 합니다), 채무자는 지급명령이 확정된 후에라도 청구이의의 소 제기를 할 수 있습니다. 하지만, 채무자는 지급명령을 받은 즉시 이의신청을 하는 것이 권장됩니다.

채무자의 주민등록지나 실거주지를 확보할 수 있고, 채무자가 지급명령에 이의하지 않을 것 같으면 지급명령 신청이 유리하지만, 그렇지 않다면 소송을 통해 해결하는 것이 더 나을 수 있습니다. 

지급명령은 온라인으로도 신청이 가능하며, 해당 지역의 법원에 신청해야 하므로 관할에 유의해야 합니다.
신청이 부적절할 경우, 즉 지급명령의 대상에서 벗어난 청구나 관할 위반, 청구 이유가 없는 경우에는 민사소송법 제465조에 따라 신청이 각하 됩니다. 
각하될 이유가 없으면 지급명령이 이루어지게 되지만 허위 사실로 지급명령을 받은 경우, 이후 법적 절차에서 그 사실이 발각된다면 소송 사기로 처벌될 수 있습니다.(허위 증거 제출시 공문서 위조 추가)

지급명령에 대해 채무자가 이의신청을 할 경우에는 2주 이내에 신청해야 합니다. 그러면 민사소송법 제470조에 따라 지급명령은 더 이상 효력을 가지지 않으며, 소송 절차로 진행됩니다.
"""
expander = st.expander("자세히 보기")
expander.write(explain)
expander.page_link(f"https://www.law.go.kr/법령/민사소송등인지법/(20231019,19353,20230418)/제7조", label="민사소송 등 인지법 제7조 제2항", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사집행법/(20220104,18671,20220104)/제58조", label="민사집행법 제58조 제3항", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/법원조직법/(20220127,17907,20210126)/제34조", label="법원조직법 제34조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제462조", label="민사소송법 제462조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제463조", label="민사소송법 제463조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제465조", label="민사소송법 제465조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제470조", label="민사소송법 제470조", icon=":material/link:")

expander.info("아래 주소의 [대한민국법원 전자민원센터] 홈페이지를 통해 지급명령절차 정보와 지급명령신청서 양식을 얻으실 수 있습니다.")
expander.page_link(f"https://help.scourt.go.kr/nm/min_1/min_1_7/min_1_7_1/index.html", label="대한민국법원 전자민원센터 - 절차안내 - 지급명령절차", icon=":material/link:")
expander.page_link(f"https://help.scourt.go.kr/nm/minwon/doc/DocListAction.work?pageIndex=1&pageSize=5&min_gubun=&sName=&eName=&min_gubun_sel=&searchWord=%C1%F6%B1%DE%B8%ED%B7%C9%BD%C5%C3%BB%BC%AD", label="대한민국법원 전자민원센터 - 양식모음 - 지급명령신청서", icon=":material/link:")


st.warning("인지대/송달료 계산, 온라인 서류제출 등은 아래 주소의 [대한민국법원 전자소송] 홈페이지 통해 확인하실 수 있습니다.")

small_title_1 = '<p style="font-family:sans-serif; font-weight:bold; color:black; font-size: 15px;">대한민국법원 전자소송 - 온라인 서류제출([지급명령(독촉) 신청] 탭의 [지급명령 신청서])</p>'
st.markdown(small_title_1, unsafe_allow_html=True)
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF302.jsp")

small_title_2 = '<p style="font-family:sans-serif; font-weight:bold; color:black; font-size: 15px;">대한민국법원 전자소송 - 인지대, 송달료 계산</p>'
st.markdown(small_title_2, unsafe_allow_html=True)
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF304_1.jsp")

small_title_3 = '<p style="font-family:sans-serif; font-weight:bold; color:black; font-size: 15px;">대한민국법원 전자소송 - 관할법원 찾기</p>'
st.markdown(small_title_3, unsafe_allow_html=True)
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF303.jsp")

st.caption("* [대한민국법원 전자소송] 저작권 정책상 URL을 알려드릴 뿐 링크를 제공하지 않음을 양해 바랍니다. 위 주소를 직접 주소창에 넣어 이동하시면 됩니다(혹은 드래그 후 우클릭).")

st.text("")


# 입력 사항. 주소, 연락처 등은 개인정보이기도 하고 어차피 양식에 옮겨 넣을 것이기 때문에 입력받지 않는것으로 수정한다.
st.text_input(label='채권자 성명 또는 법인명을 입력 하세요.', max_chars=20, key='user_input_sender_name', placeholder="예) 임꺽정")

st.text_input(label='채무자 성명 또는 법인명을 입력 하세요.', max_chars=20, key='user_input_receiver_name', placeholder="예) 홍길동")
st.text_input(label='제출할 관할법원을 입력 하세요. 위 안내에따라 [대한민국법원 전자소송 - 관할법원 찾기]를 이용하세요.', max_chars=20, key='user_input_court', placeholder="예) 서울중앙지방법원")

st.number_input(label='청구 금액을 입력 하세요.', placeholder="예) 10000000", min_value=0, key='user_input_ask_amount', format="%d", step=1)
st.text_input(label='이자율을 입력 하세요.', max_chars=20, key='user_input_ask_interest', placeholder="예) 연 5%")

st.number_input(label='송달료를 입력 하세요.', placeholder="예) 62400", min_value=0, key='user_input_ask_transmittal_fee', format="%d", step=1)
st.number_input(label='인지대를 입력 하세요.', placeholder="예) 4500", min_value=0, key='user_input_ask_stamp_fee', format="%d", step=1)

st.text_input(label='채권 발생 사유를 입력 하세요.', max_chars=50, key='user_input_ask_reason', placeholder="예) 대여금")
st.text_area(label='청구의 구체적인 내용을 입력 하세요.', max_chars=500, key='user_input_ask_reason_detail', placeholder="예) 2024년 4월 5일에 임꺽정이 홍길동에게 10,000,000원을 변제기 2024년 5월 5일로 정하여 빌려주었다. 그러나 홍길동은 전혀 변제하지 않고 있다.")

st.text_input(label='별도로 첨부할 문서가 있다면 문서명을 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_appendix', placeholder="예) 대여금 계약서(사본), 변제기 약정서(사본) 혹은 없음")
container = st.container()


content_input_limit = 4
def click_write_paper():
    if st.session_state.disable_write_paper_2 == False:
        if (len(st.session_state.user_input_sender_name) == 0) or (len(st.session_state.user_input_receiver_name) == 0) or (len(st.session_state.user_input_court) == 0)\
        or st.session_state.user_input_ask_amount == 0 or (len(st.session_state.user_input_ask_interest) == 0) \
        or st.session_state.user_input_ask_transmittal_fee == 0 or st.session_state.user_input_ask_stamp_fee == 0  or (len(st.session_state.user_input_ask_reason) == 0) or (len(st.session_state.user_input_ask_reason_detail) == 0):
            st.session_state.result_answer = "모든 입력란에 내용을 입력 하세요."
        
        elif (len(st.session_state.user_input_court) < content_input_limit)\
        or (len(st.session_state.user_input_ask_reason_detail) < content_input_limit):
            st.session_state.result_answer = "내용이 너무 짧습니다."
            
        else:
            with container:
                with st.spinner('답변하는 중...'):
                    st.session_state.disable_write_paper_2 = True
                    st.session_state.hide_main_side = True
                    
                    appendix = st.session_state.user_input_appendix
                    if "user_input_appendix" not in st.session_state or len(st.session_state.user_input_appendix) == 0:
                        appendix = "없음"
                    
                    amount = None
                    if "user_input_ask_amount" in st.session_state and st.session_state.user_input_ask_amount > 0:
                        amount = format(st.session_state.user_input_ask_amount, ',d') + "원"
                        
                    transmittal_fee = None
                    if "user_input_ask_transmittal_fee" in st.session_state and st.session_state.user_input_ask_transmittal_fee > 0:
                        transmittal_fee = format(st.session_state.user_input_ask_transmittal_fee, ',d') + "원"
                        
                    stamp_fee = None
                    if "user_input_ask_stamp_fee" in st.session_state and st.session_state.user_input_ask_stamp_fee > 0:
                        stamp_fee = format(st.session_state.user_input_ask_stamp_fee, ',d') + "원"
                    
                    # when the user clicks on button it will fetch the API
                    user_inputs = {"sender_name": st.session_state.user_input_sender_name, \
                    "receiver_name": st.session_state.user_input_receiver_name, "court": st.session_state.user_input_court, \
                    "amount": amount, "ask_interest": st.session_state.user_input_ask_interest, \
                    "transmittal_fee": transmittal_fee, "stamp_fee": stamp_fee, \
                    "ask_reason": st.session_state.user_input_ask_reason, "ask_reason_detail": st.session_state.user_input_ask_reason_detail, \
                    "appendix": appendix}
                    
                    result = requests.post(url=f"{st.session_state.backend_url}write-paper-2", data=json.dumps(user_inputs))
                    rslt = json.loads(json.loads(result.text))
                    st.session_state.result_answer = rslt.get('answer')
            
    
if st.session_state.disable_write_paper_2 == False:    
    st.button('작성하기', key='btn_send_question', on_click=click_write_paper, disabled=False)
    
    
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
if st.session_state.disable_write_paper_2 == False and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
elif st.session_state.disable_write_paper_2 and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    st.warning(st.session_state.result_warning_comment_2)
    
    # 클립보드 복사
    #if st.button(":material/content_copy: Copy"):
    #    pyperclip.copy(st.session_state.result_answer)
    #    st.info('복사되었습니다!')
        
    # 현시점 유일한 페이지 이동 인터페이스
    st.button('처음으로', on_click=click_go_to_main)
    
    copy_clipboard(st.session_state.result_answer)

