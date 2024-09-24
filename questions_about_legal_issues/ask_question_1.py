# 판례검색과 질문 front-end

import streamlit as st
import streamlit.components.v1 as components
import json
import requests


# 서버에서의 프로세스 수정으로 주석처리
# build_workflow 는 작업마다 다르게 호출해 준다.
# 이렇게 체크를 해주지 않으면 기능이 실행될때마다 계속 리퀘스트를 날리고 workflow 를 새로 build 해버린다.
#if st.session_state.init_backend == 200 and st.session_state.build != "rag":
#    inputs = {"workflow_type": "rag"}
#    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
    #print(f"build result.status_code: {result.status_code}")
#    if result.status_code == 200:
        # 왜 그런진 알 수 없지만 아래처럼 str(result.text) 넣어도 if 문에서 "rag" 와 다른걸로 나온다. 그래서 "rag" 를 그대로 넣어준다.
        #st.session_state.build = str(result.text)
#        st.session_state.build = "rag"
    
#elif st.session_state.init_backend != 200 and st.session_state.build != "rag":
#    init_result = requests.post(url=f"{st.session_state.backend_url}init")
#    st.session_state.init_backend = init_result.status_code
    
#    if st.session_state.init_backend == 200:
#        inputs = {"workflow_type": "rag"}
#        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
#        if result.status_code == 200:
#            st.session_state.build = "rag"


# 사이드바
with st.sidebar:
    st.header('국가법령정보센터')
    #work_type = st.selectbox('작업종류를 선택하세요.', ('법률관련 질문', '법적절차 정보', '서류 작성'))
    
    st.page_link(f"https://www.law.go.kr/lsSc.do?menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060114", label="법령(법조문) 찾기", icon=":material/link:")
    st.page_link(f"https://www.law.go.kr/lsTrmSc.do?menuId=13&subMenuId=65", label="법령용어찾기", icon=":material/link:")
    #legal_word = st.text_input(label='법령용어찾기', max_chars=20)
    #st.link_button(label="찾기", url=f"https://www.law.go.kr/lsTrmSc.do?menuId=13&subMenuId=65&query={legal_word}")
    
    st.divider()
    st.caption("[출처] 여기서 보여지는 판례는 '국가법령정보센터', 통계자료는 'e-나라지표' 에서 제공되었습니다.")
    

# iframe 의 width 가 화면사이즈에 맞게 조절되게 하려면 CSS 를 써야 한다.
st.markdown(
    """
    <style>
    iframe {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">판례를 기반으로 질문에 답변합니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
#st.subheader('판례를 기반으로 질문에 답변합니다.', divider="gray")
st.caption("관련성 있는 판례가 있다면 판례 기반의 답변을, 그렇지 않을 때는 그 외 검색된 정보를 기반으로 답변합니다.")
st.text("")

#case_type = st.selectbox('사건종류를 선택하세요.', ('형사', '민사', '가사', '행정'))
st.selectbox('사건종류를 선택하세요.', ('형사', '민사', '가사'), key='case_type')
st.caption('사건 종류를 정확히 선택하면 관련된 판례를 검색하는 데 도움이 됩니다. 그렇지 않을 경우 답변이 적절하지 않을 수 있습니다.')
#user_question = st.text_input(label='무엇이 궁금하세요?', max_chars=500)
st.text_area(label='무엇이 궁금하세요?', max_chars=500, key='user_question')
# spinner 의 위치를 정하기 위해 st.container 를 사용한다. 아래 st.container 생성 위치가 페이지에서 UI 위치이다. 이거 안해주면 맨 위에 그려진다.
container = st.container()
container.empty()


# 판례 검색 기능은 한번 진입해서 질문하면 더이상 질문할 수 없도록 하기 위해 보내기 버튼의 활성/비활성을 저장해논다
# streamlit 에서 버튼 자체를 비활성하는 방법은 찾지 못했고, 레퍼런스에도 이런식으로 해놔서 나도 이렇게 처리
if "disable_send_question" not in st.session_state:
    st.session_state.disable_send_question = False

# 중요!! 지역 변수는 streamlit 에서 소용이 없다. 될 때도 있지만 구조에 따라 변수를 찾질 못한다.
# 그래서 값을 유지하고 싶다면 st.session_state 를 써야 한다.
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
if "result_relevance" not in st.session_state:
    st.session_state.result_relevance = False
    
if "result_vectordb_choice" not in st.session_state:
    st.session_state.result_vectordb_choice = {}
    
if "result_etc" not in st.session_state:
    st.session_state.result_etc = []
    
if "result_urls" not in st.session_state:
    st.session_state.result_urls = []


# 버튼 콜백에서 주의 할점은 input ui 에서 리턴 받은 변수에 값이 들어가는 타이밍 보다 콜백호출이 빠르다(브라우져마다 다른듯).
# 따라서 user_question = st.text_area 이런식으로 하면 최신 값을 못 얻을때가 있다. 저렇게 쓰지 말고 key를 지정하고 불러와야한다.
#def click_send_question(arg):  # args 를 넣었다면 이렇게 그냥 받아써주면 된다.
def click_send_question():
    if st.session_state.disable_send_question == False:
        if len(st.session_state.user_question) == 0:
            st.session_state.result_answer = "질문을 적어 주세요."
        elif len(st.session_state.user_question) < 10:
            st.session_state.result_answer = "내용이 너무 짧습니다. 좀 더 구체적인 질문이나 상황을 적어 주세요."
        else:
            with container:
                with st.spinner('답변하는 중...'): 
                    st.session_state.disable_send_question = True
                    st.session_state.hide_main_side = True
                    
                    # when the user clicks on button it will fetch the API
                    user_inputs = {"question": st.session_state.user_question, "case_type":st.session_state.case_type}
                    result = requests.post(url=f"{st.session_state.backend_url}question", data=json.dumps(user_inputs))
                    #print(f"click_send_question: {result}")
                    rslt = json.loads(json.loads(result.text))
                    #print(f"rslt is {type(rslt)}")
                    st.session_state.result_answer = rslt.get('answer')
                    st.session_state.result_relevance = rslt.get('relevance')
                    st.session_state.result_vectordb_choice = rslt.get('vectordb_choice')
                    st.session_state.result_etc = rslt.get('etc_relevant_precs')
                    st.session_state.result_urls = rslt.get('statistics_url')
                    #print(f"click_send_question \nrelevance: {st.session_state.result_relevance}, \nvectordb_choice: {st.session_state.result_vectordb_choice}, \netc: {st.session_state.result_etc}")


if st.session_state.disable_send_question == False:    
    #st.button('질문하기', key='btn_send_question', on_click=click_send_question, args=('Hi!',), disabled=False)
    st.button('질문하기', on_click=click_send_question)

    
def click_go_to_main():
    # job 만 비워줘도 버튼이 눌리는 동작과 함께 streamlit_app.py 가 재실행되고 스크립트 끝부분을 통해 start_task 페이지가 실행된다.
    st.session_state.job = None


# 결과 출력
if st.session_state.disable_send_question == False and len(st.session_state.result_answer) > 0:
    st.warning(st.session_state.result_answer)
elif st.session_state.disable_send_question and len(st.session_state.result_answer) > 0:
    st.success(st.session_state.result_answer)
    
    #print(f"st.session_state.result_vectordb_choice: {st.session_state.result_vectordb_choice}")
    
    # 판례 링크, 참조 조문
    if st.session_state.result_relevance and st.session_state.result_vectordb_choice != None and "prec_no" in st.session_state.result_vectordb_choice:
        st.caption('[판례보기] 아래 사건번호를 누르면 검색된 판례전문을 볼 수 있습니다.')
        st.page_link(f"https://www.law.go.kr/DRF/lawService.do?OC=xivaroma&target=prec&ID={st.session_state.result_vectordb_choice['prec_no']}&type=html", label=st.session_state.result_vectordb_choice['case_no'], icon=":material/link:")
            
    if st.session_state.result_vectordb_choice != None and "ref_article" in st.session_state.result_vectordb_choice:
        st.text("")
        st.caption('[관련조문]')
        st.text(st.session_state.result_vectordb_choice['ref_article'])
        #print(f"ref_article: {st.session_state.result_vectordb_choice['ref_article']}")
    
    st.info("혹시 원하는 답변이 아니라면 단어나 질문을 바꿔서 시도해 보세요.")
    st.warning(st.session_state.result_warning_comment_1)
    st.button('처음으로', on_click=click_go_to_main)
            

    statistics_result_url = st.session_state.result_urls
    if statistics_result_url != None and len(st.session_state.result_urls) > 0:
        st.divider()
        components.iframe(statistics_result_url[2], height=630, scrolling=True)
        components.iframe(statistics_result_url[0], height=700, scrolling=True)
        components.iframe(statistics_result_url[3], height=700, scrolling=True)


#components.html(
#    """
#    """,
#    width=1080, height=900, scrolling=True
#)

