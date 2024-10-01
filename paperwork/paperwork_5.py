# 서류작성 - 고소장 front-end

import streamlit as st
import json
import requests
#import pyperclip    # 클립보드 복사
import streamlit.components.v1 as components
import markdown2
from bs4 import BeautifulSoup


#if st.session_state.init_backend == 200 and st.session_state.build != "write_paper_5":
#    inputs = {"workflow_type": "write_paper_5"}
#    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
#    if result.status_code == 200:
#        st.session_state.build = "write_paper_5"
    
#elif st.session_state.init_backend != 200 and st.session_state.build != "write_paper_5":
#    init_result = requests.post(url=f"{st.session_state.backend_url}init")
#    st.session_state.init_backend = init_result.status_code
    
#    if st.session_state.init_backend == 200:
#        inputs = {"workflow_type": "write_paper_5"}
#        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
#        if result.status_code == 200:
#            st.session_state.build = "write_paper_5"


if "disable_write_paper_5" not in st.session_state:
    st.session_state.disable_write_paper_5 = 0      # 0: 작성하기 답변받은적 없음, 1: 작성하기 첫답변 받음, 2: 작성하기 최종 완료
        
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
if "result_answer_post" not in st.session_state:
    st.session_state.result_answer_post = ""
    
if "input_info_dict" not in st.session_state:
    st.session_state.input_info_dict = {}
    
    
with st.sidebar:
    st.caption(":material/release_alert: 아래의 [대한민국법원-전자민원센터] 홈페이지를 통해 법적 절차 안내, 사건검색 등 여러정보를 얻을 수 있습니다.")
    st.page_link("https://help.scourt.go.kr/nm/main/index.html", label="전자민원센터", icon=":material/link:")


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">\"고소장\" 작성을 도와드립니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.text("")

st.subheader("고소장이란?")
explain = """
고소장은 피해자가 범죄를 신고하기 위해 수사기관에 제출하는 서류로, 법적으로 정해진 양식은 없지만 경찰청 민원포털에서 표준서식을 다운로드할 수 있습니다.   
법률구조공단에서는 모욕죄, 폭행죄와 같은 일반적인 범죄에 대한 고소장 양식을 제공하고 있으니 참고하면 좋습니다.

고소장을 작성할 때 중요한 것은 범죄 피해 사실을 6하 원칙에 맞춰 자세하고 명확히 기재하는 것입니다.   
바꿔말하면 범죄가 성립하기 위한 범죄의 구성 요건이 잘 드러나도록 기재하는 것이 좋습니다.    
피고소인의 행위와 고소인이 입은 피해사실, 그리고 그 둘 간의 인과 관계를 명확히 기재해야하는 것입니다.

고소 취지나 법리 평가, 입증 자료는 첨부할 수 있지만 반드시 필요하지는 않습니다.   
다만 입증 자료가 없는 고소장은 수사기관에서 반려될 위험이 높으며, 소명자료로 쓸 입증 자료가 없다면 영장청구 역시 어렵기 때문에 수사가 진행될 가능성도 떨어집니다.

만약 범죄 사실이 너무 많아 고소장에 모두 포함하기 어렵다면 범죄일람표를 작성해 첨부하는 방법도 있습니다.   
이 표는 사건을 간소화해 이해하기 쉽게 만들어, 수사관이 사건을 잘 파악할 수 있도록 돕는 역할을 합니다.

구두로 고소를 할 수도 있으나 사건 발생 장소 또는 피고소인의 주소를 관할하는 경찰서에 제출하는 것이 일반적입니다(검찰청 제출 가능).   
방문 제출뿐만 아니라, 등기우편이나 온라인 문서 제출 서비스인 문서24를 통해서도 제출할 수 있습니다. 

고소, 고발 방식은 형사소송법 제237조에 명시되어 있습니다.
"""
expander = st.expander("자세히 보기")
expander.write(explain)
expander.page_link(f"https://www.law.go.kr/법령/형사소송법/(20240213,20265,20240213)/제237조", label="형사소송법 제237조", icon=":material/link:")

expander.text("")
expander.info("고소장 양식은 아래 주소의 [경찰 민원포털 - 고객센터 - 민원서식의 수사 탭 중 고소장] 에서 받으실 수 있습니다.")
expander.text("https://minwon.police.go.kr/#customerCenter/fileDown")
expander.caption("* [경찰 민원포털] 저작권 정책상 URL을 알려드릴 뿐 링크를 제공하지 않음을 양해 바랍니다. 위 주소를 직접 주소창에 넣어 이동하시면 됩니다(혹은 드래그 후 우클릭).")


# 입력 사항
if st.session_state.disable_write_paper_5 == 0:
    st.text_input(label='고소인 이름을 입력 하세요.', max_chars=20, key='user_input_sender_name', placeholder="예) 임꺽정")
    st.text_input(label='피고소인 이름을 입력 하세요.', max_chars=20, key='user_input_receiver_name', placeholder="예) 홍길동")
    st.text_area(label='피고소인과 관련된 기타 사항이 있다면 입력 하세요.', max_chars=200, key='user_input_receiver_etc', placeholder="예) 고소인과의 관계, 성별, 외모 특징 등")
    st.caption("기타사항에는 고소인과의 관계나 피고소인의 인적사항과 연락처를 정확히 알 수 없을 경우 성별, 외모 특징, 인상착의 등을 구체적으로 기재하세요. 여러가지라면 콤마(,)로 구분하여 넣으세요.")
    st.text("")
    
    st.text_input(label='어떤 범죄(죄목)로 고소할 것인지 입력 하세요.', max_chars=100, key='user_input_purpose', placeholder="예) 사기죄")
    st.text_input(label='사건이 일어난 일시와 장소를 입력 하세요.', max_chars=50, key='user_input_crime_time', placeholder="예) 2023년 4월 5일. 서울 강남구 XXX앞")
    st.text_area(label='사건이 일어났을 때의 정황을 설명해 주세요.', max_chars=500, key='user_input_crime_history', placeholder="참고) 사건이 일어나게된 이유 등 정황")
    st.text_area(label='해당 사건으로 인해 입은 피해 사실을 입력 하세요.', max_chars=500, key='user_input_damage', placeholder="예) 20,000,000원의 금전피해 및 정신적 피해")
    st.text_area(label='고소할 결심과 처벌을 원하는 이유를 입력 하세요.', max_chars=500, key='user_input_reason', placeholder="예) 피고소인이 돈을 빌려간 후 갚지 않고 잠적한 상태로 인한 심각한 재정위기 및 정신적 피해")
    st.text_input(label='제출할 수 있는 증거 자료가 있다면 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_evidence', placeholder="예) 문자메세지, 거래 내역서")
    st.text_input(label='같은 내용의 고소장을 이미 접수하거나 제출한 적이 있는지 입력 하세요.', max_chars=100, key='user_input_etc_accuse', placeholder="예) 본 사건과 관련된 형사 사건 수사 없음")
    st.text_input(label='고소장을 제출할 경철서명을 입력 하세요.', max_chars=50, key='user_input_station', placeholder="예) 강남경찰서")
    container = st.container()
    container.empty()
    
else:
    input_info_title_1 = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 14px;">입력정보</p>'
    st.markdown(input_info_title_1, unsafe_allow_html=True)
    st.text(f"고소인: {st.session_state.input_info_dict.get('sender_name')}")
    st.text(f"피고소인: {st.session_state.input_info_dict.get('receiver_name')}")
    st.text(f"피고소인 기타 사항: {st.session_state.input_info_dict.get('receiver_etc')}")
    
    st.text(f"죄목: {st.session_state.input_info_dict.get('purpose')}")
    st.text(f"사건 발생 일시 및 장소:\n{st.session_state.input_info_dict.get('crime_time')}")
    st.text(f"사건 경위:\n{st.session_state.input_info_dict.get('crime_history')}")
    st.text(f"피해 사실: {st.session_state.input_info_dict.get('damage')}")
    st.text(f"고소 이유: {st.session_state.input_info_dict.get('reason')}")
    st.text(f"첨부할 증거 자료: {st.session_state.input_info_dict.get('evidence')}")
    st.text(f"동일 내용의 고소장 제출 이력 여부: {st.session_state.input_info_dict.get('etc_accuse')}")
    st.text(f"제출 경찰서: {st.session_state.input_info_dict.get('station')}")
    

content_input_limit = 4
def click_write_paper():
    if st.session_state.disable_write_paper_5 == 0:
        if (len(st.session_state.user_input_sender_name) == 0) or (len(st.session_state.user_input_receiver_name) == 0) \
        or (len(st.session_state.user_input_purpose) == 0) or (len(st.session_state.user_input_crime_time) == 0) or (len(st.session_state.user_input_crime_history) == 0) \
        or (len(st.session_state.user_input_damage) == 0) or (len(st.session_state.user_input_reason) == 0) \
        or (len(st.session_state.user_input_etc_accuse) == 0) or (len(st.session_state.user_input_station) == 0):
            st.session_state.result_answer = "모든 입력란에 내용을 입력 하세요."
        
        elif (len(st.session_state.user_input_crime_time) < content_input_limit) or (len(st.session_state.user_input_crime_history) < content_input_limit) \
            or (len(st.session_state.user_input_damage) < content_input_limit) or (len(st.session_state.user_input_reason) < content_input_limit):
            st.session_state.result_answer = "내용이 너무 짧습니다."
            
        else:
            with container:
                with st.spinner('답변하는 중...'):
                    st.session_state.disable_write_paper_5 = 1
                    st.session_state.hide_main_side = True
                    
                    receiver_etc = st.session_state.user_input_receiver_etc
                    if "user_input_receiver_etc" not in st.session_state or len(st.session_state.user_input_receiver_etc) == 0:
                        receiver_etc = "없음"
                        
                    evidence = st.session_state.user_input_evidence
                    if "user_input_evidence" not in st.session_state or len(st.session_state.user_input_evidence) == 0:
                        evidence = "없음"
                    
                    user_inputs = {"dialogue_session_id": st.session_state.dialogue_session_id, "is_post_conversation": False, "sender_name": st.session_state.user_input_sender_name, "receiver_name": st.session_state.user_input_receiver_name, \
                    "receiver_etc": receiver_etc, "purpose": st.session_state.user_input_purpose, "crime_time": st.session_state.user_input_crime_time, "crime_history": st.session_state.user_input_crime_history, \
                    "damage": st.session_state.user_input_damage, "reason": st.session_state.user_input_reason, "evidence": evidence, \
                    "etc_accuse": st.session_state.user_input_etc_accuse, "station": st.session_state.user_input_station, "add_info": "없음"}
                    
                    # 입력정보 저장
                    st.session_state.input_info_dict = user_inputs
                    
                    # when the user clicks on button it will fetch the API
                    result = requests.post(url=f"{st.session_state.backend_url}write-paper-5", data=json.dumps(user_inputs))
                    rslt = json.loads(result.text)
                    st.session_state.result_answer = rslt.get('answer')
            
    elif st.session_state.disable_write_paper_5 == 1:
        with container:
            with st.spinner('답변하는 중...'):
                st.session_state.disable_write_paper_5 = 2
                st.session_state.input_info_dict["is_post_conversation"] = True
                
                if "user_input_add_info" in st.session_state and len(st.session_state.user_input_add_info) > 0:
                    st.session_state.input_info_dict["add_info"] = st.session_state.user_input_add_info
                
                # when the user clicks on button it will fetch the API
                result = requests.post(url=f"{st.session_state.backend_url}write-paper-5", data=json.dumps(st.session_state.input_info_dict))
                rslt = json.loads(result.text)
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
if st.session_state.disable_write_paper_5 == 0 and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
    
elif st.session_state.disable_write_paper_5 == 1 and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text_area(label='AI가 요청한 추가 정보를 입력 하세요.', max_chars=500, key='user_input_add_info')
    st.warning(st.session_state.result_warning_comment_2)
    container = st.container()
    container.empty()
    
elif st.session_state.disable_write_paper_5 == 2 and len(st.session_state.result_answer_post) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text(f"추가 정보:\n{st.session_state.input_info_dict.get('add_info')}")
    st.success(st.session_state.result_answer_post)
    st.warning(st.session_state.result_warning_comment_2)


if st.session_state.disable_write_paper_5 == 0 or st.session_state.disable_write_paper_5 == 1:    
    st.button('작성하기', key='btn_send_question', on_click=click_write_paper, disabled=False)
    
    if st.session_state.disable_write_paper_5 == 1:
        st.button('처음으로', on_click=click_go_to_main)
    
elif st.session_state.disable_write_paper_5 == 2:
    # 클립보드 복사
    #if st.button(":material/content_copy: Copy"):
    #    pyperclip.copy(st.session_state.result_answer_post)
    #    st.info('복사되었습니다!')
        
    st.button('처음으로', on_click=click_go_to_main)
    
    copy_clipboard(st.session_state.result_answer_post)

