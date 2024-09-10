# 서류작성 - (민사)소장 front-end

import streamlit as st
import json
import requests
import pyperclip    # 클립보드 복사


if st.session_state.init_backend == 200 and st.session_state.build != "write_paper_6":
    inputs = {"workflow_type": "write_paper_6"}
    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
    if result.status_code == 200:
        st.session_state.build = "write_paper_6"
    
elif st.session_state.init_backend != 200 and st.session_state.build != "write_paper_6":
    init_result = requests.post(url=f"{st.session_state.backend_url}init")
    st.session_state.init_backend = init_result.status_code
    
    if st.session_state.init_backend == 200:
        inputs = {"workflow_type": "write_paper_6"}
        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
        if result.status_code == 200:
            st.session_state.build = "write_paper_6"


if "disable_write_paper_6" not in st.session_state:
    st.session_state.disable_write_paper_6 = 0      # 0: 작성하기 답변받은적 없음, 1: 작성하기 첫답변 받음, 2: 작성하기 최종 완료
        
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
if "result_answer_post" not in st.session_state:
    st.session_state.result_answer_post = ""
    
if "input_info_dict" not in st.session_state:
    st.session_state.input_info_dict = {}
    
    
with st.sidebar:
    st.caption(":material/release_alert: 아래의 [대한민국법원-전자민원센터] 홈페이지를 통해 법적 절차 안내, 사건검색 등 여러정보를 얻을 수 있습니다.")
    st.page_link("https://help.scourt.go.kr/nm/main/index.html", label="전자민원센터", icon=":material/link:")


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">\"(민사)소장\" 작성을 도와드립니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.text("")

st.subheader("소장이란?")
explain = """
민사소송법 제248조에 따라 민사소송을 제기할 때 작성하는 소장은 본안의 재판을 받기 위해 법원에 제출하는 문서로, 소송의 기본적인 내용과 주장을 포함합니다.   

소장은 원고(소송을 제기한 사람)와 피고(소송을 당한 사람), 소송의 원인과 청구 내용, 그리고 그에 대한 법적 근거를 명시하는 소송에서 가장 중요한 문서입니다.   
만약 지급명령신청과 같이 다른 절차에서 본안으로 이행된다면 신청서가 소장의 역할을 대신하게 됩니다.

소장의 기재 사항은 민사소송법 제249조에 명시되어 있으며, 이에 따라 당사자, 법정대리인(당사자가 제한 능력자인 경우), 청구취지, 청구원인을 필수적으로 기재해야 합니다.   
작성 시 유의할 점은 내용은 기재 사항을 빠짐없이 적시해야 하며 명확하고 간결하게 작성해야 합니다. 그리고 주장하는 사실관계가 정확해야 합니다.

항목 중 '청구 취지'의 경우 이는 '피고에게 금 1,000만 원을 지급하라'와 같이 원고가 법원에 요구하는 내용이며 판결의 주문에 대응하는 매우 중요한 부분이므로 판결서의 기재례를 참조하는 것이 좋습니다.   

'청구 원인' 항목은 청구취지와 같은 판결이 선고되어야 하는 이유를 설명하는 것으로써, 청구를 뒷받침하는 구체적인 사유와 사건의 경과, 사실관계, 법리적 근거 등을 포함해야 합니다.   
또한 피고가 반박할 것으로 충분히 예상되는 사실에 대해서도 진술하는 것이 좋습니다.   
'청구 원인'은 사건별로 기재해야 할 사항(요건 사실: 법률상 청구가 성립하기 위해 필요한 사실)이 다른데, 이는 '대한민국법원 나홀로소송' 홈페이지에서 찾아볼 수 있습니다.

소장을 법원에 제출하고 피고에게 소장 부본이 송달되면 피고는 제출 기한인 30일 이내에 답변서를 제출해야 하며, 피고가 답변서를 기한 내 제출하지 않았거나 자백 혹은 인정하는 취지의 답변서를 제출하는 경우엔 무변론 판결 대상 사건으로 분류되게 됩니다.   
하지만 그렇지 않은 경우 계속 진행되어 다투게 됩니다.

소장은 '대한민국법원 전자소송' 홈페이지에서 작성 및 제출이 가능합니다.   
이 경우 부본을 첨부할 필요가 없습니다(전자소송이 아닌 경우에는 피고의 수에 따라 첨부할 소장 부본의 수가 결정됩니다).
"""
expander = st.expander("자세히 보기")
expander.write(explain)
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제248조", label="민사소송법 제248조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제249조", label="민사소송법 제249조", icon=":material/link:")

expander.info("소장 양식은 [대한민국법원 전자민원센터]의 [양식모음]에서 받으실 수 있습니다.")
expander.page_link(f"https://help.scourt.go.kr/nm/minwon/doc/DocListAction.work?pageIndex=1&pageSize=5&min_gubun=&sName=&eName=&min_gubun_sel=&searchWord=%BC%D2%C0%E5", label="대한민국법원 전자민원센터 - 양식모음 - [민사] 소장", icon=":material/link:")


st.warning("관할법원 찾기, 온라인 서류제출 등은 아래 주소의 [대한민국법원 전자소송] 홈페이지 통해 확인하실 수 있습니다.")

small_title_1 = '<p style="font-family:sans-serif; font-weight:bold; color:black; font-size: 15px;">대한민국법원 전자소송 - 온라인 서류제출([민사 본안] 탭의 [소장])</p>'
st.markdown(small_title_1, unsafe_allow_html=True)
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF302.jsp")

small_title_2 = '<p style="font-family:sans-serif; font-weight:bold; color:black; font-size: 15px;">대한민국법원 전자소송 - 관할법원 찾기</p>'
st.markdown(small_title_2, unsafe_allow_html=True)
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF303.jsp")

st.caption("* [대한민국법원 전자소송] 저작권 정책상 URL을 알려드릴 뿐 링크를 제공하지 않음을 양해 바랍니다. 위 주소를 직접 주소창에 넣어 이동하시면 됩니다(혹은 드래그 후 우클릭).")
st.text("")


# 입력 사항
if st.session_state.disable_write_paper_6 == 0:
    st.text_input(label='원고 이름을 입력 하세요.', max_chars=20, key='user_input_sender_name', placeholder="예) 임꺽정")
    st.text_input(label='피고 이름을 입력 하세요.', max_chars=20, key='user_input_receiver_name', placeholder="예) 홍길동")
    
    st.text_input(label='사건명을 입력 하세요.', max_chars=50, key='user_input_case_name', placeholder="예) 대여금 청구 소송")
    st.text_area(label='원고가 요구하는 사항을 명확하게 기술 하세요.', max_chars=300, key='user_input_purpose', placeholder="예) 피고는 원고에게 대여금 10,000,000원 및 이에 대하여 소장부본 송달 다음 날부터 다 갚는 날까지 연 10%의 비율로 계산한 돈을 지급하라. 소송비용은 피고가 부담한다.")
    st.text_area(label='청구원인에 대한 구체적인 사실을 기술 하세요. 즉, 위 항의 요구를 하게된 이유를 설명 하세요.', max_chars=1000, key='user_input_reason', placeholder="예) 피고는 원고에게 2024년 1월 1일에 10,000,000원을 빌려 2024년 2월 1일까지 갚기로 하였으나 현재까지 갚지 않고 있습니다.")
    st.text_input(label='위에서 기술한 청구원인을 입증할 증거가 있다면 콤마(,)로 구분하여 넣으세요.', max_chars=200, key='user_input_evidence', placeholder="예) 문자메세지, 차용증")
    st.text_input(label='제출할 관할법원을 입력 하세요. 위 안내에따라 [대한민국법원 전자소송 - 관할법원 찾기]를 이용하세요.', max_chars=20, key='user_input_court', placeholder="예) 서울중앙지방법원")
    
else:
    input_info_title_1 = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 14px;">입력정보</p>'
    st.markdown(input_info_title_1, unsafe_allow_html=True)
    st.text(f"원고: {st.session_state.input_info_dict.get('sender_name')}")
    st.text(f"피고: {st.session_state.input_info_dict.get('receiver_name')}")
    
    st.text(f"사건명: {st.session_state.input_info_dict.get('case_name')}")
    st.text(f"청구 취지: {st.session_state.input_info_dict.get('purpose')}")
    st.text(f"청구 원인: {st.session_state.input_info_dict.get('reason')}")
    st.text(f"입증 방법: {st.session_state.input_info_dict.get('evidence')}")
    st.text(f"관할 법원: {st.session_state.input_info_dict.get('court')}")
    

content_input_limit = 4
def click_write_paper():
    if st.session_state.disable_write_paper_6 == 0:
        if (len(st.session_state.user_input_sender_name) == 0) or (len(st.session_state.user_input_receiver_name) == 0) \
        or (len(st.session_state.user_input_case_name) == 0) or (len(st.session_state.user_input_purpose) == 0) or (len(st.session_state.user_input_reason) == 0) or (len(st.session_state.user_input_court) == 0):
            st.session_state.result_answer = "모든 입력란에 내용을 입력 하세요."
        
        elif (len(st.session_state.user_input_case_name) < content_input_limit) or (len(st.session_state.user_input_purpose) < content_input_limit) or (len(st.session_state.user_input_reason) < content_input_limit):
            st.session_state.result_answer = "내용이 너무 짧습니다."
            
        else:
            st.session_state.disable_write_paper_6 = 1
            st.session_state.hide_main_side = True
                
            evidence = st.session_state.user_input_evidence
            if "user_input_evidence" not in st.session_state or len(st.session_state.user_input_evidence) == 0:
                evidence = "없음"
            
            user_inputs = {"is_post_conversation": False, "sender_name": st.session_state.user_input_sender_name, "receiver_name": st.session_state.user_input_receiver_name, \
            "case_name": st.session_state.user_input_case_name, "purpose": st.session_state.user_input_purpose, "reason": st.session_state.user_input_reason, "evidence": evidence, \
            "court": st.session_state.user_input_court, "add_info": "없음"}
            
            # 입력정보 저장
            st.session_state.input_info_dict = user_inputs
            
            # when the user clicks on button it will fetch the API
            result = requests.post(url=f"{st.session_state.backend_url}write-paper-6", data=json.dumps(user_inputs))
            rslt = json.loads(json.loads(result.text))
            st.session_state.result_answer = rslt.get('answer')
            
    elif st.session_state.disable_write_paper_6 == 1:
        st.session_state.disable_write_paper_6 = 2
        st.session_state.input_info_dict["is_post_conversation"] = True
        
        if "user_input_add_info" in st.session_state and len(st.session_state.user_input_add_info) > 0:
            st.session_state.input_info_dict["add_info"] = st.session_state.user_input_add_info
        
        # when the user clicks on button it will fetch the API
        result = requests.post(url=f"{st.session_state.backend_url}write-paper-6", data=json.dumps(st.session_state.input_info_dict))
        rslt = json.loads(json.loads(result.text))
        st.session_state.result_answer_post = rslt.get('answer')
        
        
def click_go_to_main():
    # job 만 비워줘도 버튼이 눌리는 동작과 함께 streamlit_app.py 가 재실행되고 스크립트 끝부분을 통해 start_task 페이지가 실행된다.
    st.session_state.job = None


# 결과 출력
if st.session_state.disable_write_paper_6 == 0 and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
    
elif st.session_state.disable_write_paper_6 == 1 and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text_area(label='AI가 요청한 추가 정보를 입력 하세요.', max_chars=500, key='user_input_add_info')
    st.warning(st.session_state.result_warning_comment_2)
    
elif st.session_state.disable_write_paper_6 == 2 and len(st.session_state.result_answer_post) > 0:
    st.success(st.session_state.result_answer)
    st.text("")
    
    st.text(f"추가 정보:\n{st.session_state.input_info_dict.get('add_info')}")
    st.success(st.session_state.result_answer_post)
    st.warning(st.session_state.result_warning_comment_2)


if st.session_state.disable_write_paper_6 == 0 or st.session_state.disable_write_paper_6 == 1:    
    st.button('작성하기', key='btn_send_question', on_click=click_write_paper, disabled=False)
    
    if st.session_state.disable_write_paper_6 == 1:
        st.button('처음으로', on_click=click_go_to_main)
    
elif st.session_state.disable_write_paper_6 == 2:
    # 클립보드 복사
    if st.button(":material/content_copy: Copy"):
        pyperclip.copy(st.session_state.result_answer_post)
        st.info('복사되었습니다!')
        
    st.button('처음으로', on_click=click_go_to_main)

