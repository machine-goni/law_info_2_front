import streamlit as st
#from PIL import Image
import datetime
import requests


# --- 변수 및 back end 초기화 ---
# 전역은 st.session_state 에 key 를 만들어 넣어주면 된다.


#if "build" not in st.session_state:    
#    st.session_state.build = None

if "backend_url" not in st.session_state:
    #st.session_state.backend_url = "http://127.0.0.1:8000/"        
    st.session_state.backend_url = st.secrets["my_url"]

if "job" not in st.session_state:
    st.session_state.job = None
    
if "dialogue_session_id" not in st.session_state:
    st.session_state.dialogue_session_id = None

# 메인 사이드바를 감출수 있도록 하기위한 플래그
if "hide_main_side" not in st.session_state:
    st.session_state.hide_main_side = False
    
if "result_warning_comment_1" not in st.session_state:
    st.session_state.result_warning_comment_1 = "작성된 조언은 참고용으로만 사용하시기 바랍니다. 정확하고 적법한 자문은 반드시 법률 자격을 갖춘 전문가와 상의하세요. 또한, 입력한 개인 정보가 유출되지 않도록 주의하시고, 특히 공용PC 등은 사용하지 않으시길 권고합니다."
    
if "result_warning_comment_2" not in st.session_state:
    st.session_state.result_warning_comment_2 = "작성된 내용은 기본적인 초안이므로 활용하시기 전 검증 절차가 필요합니다. 또한, 입력한 개인 정보가 유출되지 않도록 주의하시고, 특히 공용PC 등은 사용하지 않으시길 권고합니다."
    
    
def init_backend():
    # 서버가 정상이면 200 을 리턴
    if ("init_backend" not in st.session_state) or st.session_state.init_backend != 200:
        result = requests.post(url=f"{st.session_state.backend_url}init")
        print(f"init_backend: {result}")    # type: requests.models.Response
        #print(f"requests.models.Response.status_code: {result.status_code}")   # 서버 status code
        #print(f"requests.models.Response.text: {result.text}")                 # 함수 리턴
        st.session_state.init_backend = result.status_code

init_backend()

# --- 변수 및 back end 초기화 ---


#CATEGORIES = [None, "법률 QnA", "서류작성", "절차안내"]
CATEGORIES = [None, "법률 QnA", "서류작성"]

# set_page_config 는 페이지당 한번만 호출되야하고, 제일 첫 부분에 호출되야한다.
# 여기서 set_page_config 를 호출하면 각 페이지의 icon, title 은 무시되고 여기의 설정으로 세팅된다.
#st.set_page_config(page_title="None", page_icon="images/ic_launcher.png", layout="centered")


# 전역 변수 초기화. 첫 페이지로 돌아갈때 리셋해줘야 하는 것들은 여기서.
def init_global_var():
    st.session_state.job = None
    st.session_state.hide_main_side = False
    st.session_state.dialogue_session_id = None
        
    st.session_state.result_answer = ""
    st.session_state.result_answer_post = ""
    st.session_state.result_relevance = False
    st.session_state.result_vectordb_choice = {}
    st.session_state.result_etc = []
    st.session_state.result_urls = []
    st.session_state.input_info_dict = {}
    
    st.session_state.disable_send_question = False
    st.session_state.disable_advice = 0
    st.session_state.disable_write_paper_1 = False
    st.session_state.disable_write_paper_2 = False
    st.session_state.disable_write_paper_4 = 0
    st.session_state.disable_write_paper_5 = 0
    st.session_state.disable_write_paper_6 = 0
    
    if "user_question" in st.session_state:
        st.session_state.user_question = ""
        
    if "user_input_status" in st.session_state:
        st.session_state.user_input_status = ""
        
    if "user_input_question" in st.session_state:
        st.session_state.user_input_question = ""
        
    if "user_input_reason" in st.session_state:
        st.session_state.user_input_reason = ""
        
    if "user_input_fact" in st.session_state:
        st.session_state.user_input_fact = ""
        
    if "user_input_ask" in st.session_state:
        st.session_state.user_input_ask = ""
        
    if "user_input_point" in st.session_state:
        st.session_state.user_input_point = ""
        
    if "user_input_sender" in st.session_state:
        st.session_state.user_input_sender = ""
        
    if "user_input_phone" in st.session_state:
        st.session_state.user_input_phone = ""
        
    if "user_input_receiver" in st.session_state:
        st.session_state.user_input_receiver = ""
        
    if "user_input_appendix" in st.session_state:
        st.session_state.user_input_appendix = ""
        
    if "user_input_sender_name" in st.session_state:
        st.session_state.user_input_sender_name = ""
        
    if "user_input_receiver_name" in st.session_state:
        st.session_state.user_input_receiver_name = ""
        
    if "user_input_court" in st.session_state:
        st.session_state.user_input_court = ""
        
    if "user_input_ask_amount" in st.session_state:
        st.session_state.user_input_ask_amount = 0
        
    if "user_input_ask_interest" in st.session_state:
        st.session_state.user_input_ask_interest = ""
        
    if "user_input_ask_transmittal_fee" in st.session_state:
        st.session_state.user_input_ask_transmittal_fee = 0
        
    if "user_input_ask_stamp_fee" in st.session_state:
        st.session_state.user_input_ask_stamp_fee = 0
        
    if "user_input_ask_reason" in st.session_state:
        st.session_state.user_input_ask_reason = ""
        
    if "user_input_ask_reason_detail" in st.session_state:
        st.session_state.user_input_ask_reason_detail = ""
        
    if "user_input_case_no" in st.session_state:
        st.session_state.user_input_case_no = ""
        
    if "user_input_case_name" in st.session_state:
        st.session_state.user_input_case_name = ""
        
    if "user_input_case_purpose" in st.session_state:
        st.session_state.user_input_case_purpose = ""
        
    if "user_input_case_cause" in st.session_state:
        st.session_state.user_input_case_cause = ""
        
    if "user_input_case_prove" in st.session_state:
        st.session_state.user_input_case_prove = ""
        
    if "user_input_case_appendix" in st.session_state:
        st.session_state.user_input_case_appendix = ""
        
    if "user_input_case_court" in st.session_state:
        st.session_state.user_input_case_court = ""
        
    if "user_input_rebut" in st.session_state:
        st.session_state.user_input_rebut = ""
        
    if "user_input_add_info" in st.session_state:
        st.session_state.user_input_add_info = ""
        
    if "user_input_receiver_etc" in st.session_state:
        st.session_state.user_input_receiver_etc = ""
        
    if "user_input_purpose" in st.session_state:
        st.session_state.user_input_purpose = ""
        
    if "user_input_crime_time" in st.session_state:
        st.session_state.user_input_crime_time = ""
        
    if "user_input_crime_history" in st.session_state:
        st.session_state.user_input_crime_history = ""
        
    if "user_input_damage" in st.session_state:
        st.session_state.user_input_damage = ""
        
    if "user_input_evidence" in st.session_state:
        st.session_state.user_input_evidence = ""
        
    if "user_input_etc_accuse" in st.session_state:
        st.session_state.user_input_etc_accuse = ""
        
    if "user_input_station" in st.session_state:
        st.session_state.user_input_station = ""


# 첫 페이지
def start_task():
    #st.header("AI 법률 도우미")
    job = st.selectbox("작업을 선택하세요.", CATEGORIES)
    init_global_var()

    if st.button("다음"):
        if ("init_backend" not in st.session_state) or st.session_state.init_backend != 200:
            popup_code = f"<script>alert('서버연결이 원활하지 않습니다. 잠시 후 다시 시도해 보세요.\\nServer Code: {st.session_state.init_backend}')</script>"
            st.components.v1.html(popup_code, height=0, width=0)
            
            init_backend()
            #st.toast('Your edited image was saved!', icon='😍')
        else:
            # epoch time 으로 dialogue_session_id 생성
            now = datetime.datetime.now()
            timestamp = now.timestamp()
            st.session_state.dialogue_session_id = str(timestamp)
            #one_hour_later = now + datetime.timedelta(hours=1)
            #print(f"start_task - timestamp: {st.session_state.dialogue_session_id}")   # 출력 예: 1726045120.690278
            #print(f"one_hour_later: {one_hour_later.timestamp()}")                     # 출력 예: 1726048720.690278
            #print(f"diff timestamp: {one_hour_later.timestamp() - timestamp}")         # 출력 예: 3600.0
            
            st.session_state.job = job
            if job != None:
                #print(f"job: {job}, {type(job)}")
                st.rerun()
    
    st.text("")
    st.text("")
    # 저작권. 가운데 정렬
    st.markdown("<h6 style='text-align: center; color: grey;'>COPYRIGHTⓒ 2024 ONTHETIME. ALL RIGHTS RESERVED.</h6>", unsafe_allow_html=True)


def end_task():
    init_global_var()
    
    st.rerun()


job = st.session_state.job


# 페이지 정의
end_task = st.Page(end_task, title="처음으로", icon=":material/gavel:")

question_1 = st.Page(
    "questions_about_legal_issues/ask_question_1.py", title="판례검색과 질문", icon=":material/quiz:", default=(job == "법률 QnA"))
question_2 = st.Page(
    "questions_about_legal_issues/ask_question_2.py", title="법률 조언", icon=":material/quiz:")

paperwork_1 = st.Page(
    "paperwork/paperwork_1.py", title="내용증명", icon=":material/article:", default=(job == "서류작성"))
paperwork_2 = st.Page(
    "paperwork/paperwork_2.py", title="지급명령 신청서", icon=":material/article:")
paperwork_3 = st.Page(
    "paperwork/paperwork_3.py", title="지급명령 이의신청서", icon=":material/article:")
paperwork_6 = st.Page(
    "paperwork/paperwork_6.py", title="(민사)소장", icon=":material/article:")
paperwork_4 = st.Page(
    "paperwork/paperwork_4.py", title="(민사)답변서", icon=":material/article:")
paperwork_5 = st.Page(
    "paperwork/paperwork_5.py", title="고소장", icon=":material/article:")

#guide_1 = st.Page(
#    "procedural_guide/guide_1.py", title="안내 1", icon=":material/info:", default=(job == "절차안내"))
#guide_2 = st.Page(
#    "procedural_guide/guide_2.py", title="안내 2", icon=":material/info:")


top_pages = [end_task]
question_pages = [question_1, question_2]
paperwork_pages = [paperwork_1, paperwork_2, paperwork_3, paperwork_6, paperwork_4, paperwork_5]
#guide_pages = [guide_1, guide_2]

# logo 는 size 조절 옵션이 없다. 그래서 아래처럼 style 을 넣어 조절하는 편법을 써야 한다.
# logo 중 image 는 사이드바가 열렸을 때, icon_image 는 사이드바가 없거나 닫혔을 때 나온다.
#st.html("""
#  <style>
#    [alt=Logo] {
#      height: 2.5rem;
#    }
#  </style>
#        """)
st.logo("images/logo_550x55.png", icon_image="images/courthouse_256_white.png")


# 그냥 path 로는 안되고 먼저 이미지를 불러와야 한다.
#left_co, cent_co, last_co = st.columns(3)  # 정렬을 위해 구역을 3부분으로 설정
#img = Image.open('images/ic_launcher.png')
#with cent_co:      # 중앙 정렬
#    st.image(img, width=240)


st.title("AI 법률 도우미")
st.info("당신의 법률 문제를 도와드립니다!")
st.caption("[주의] 본 서비스는 법률문제에 대해 누구나 쉽게 접근하는 것을 목적으로 만들어졌으며, 일반적인 조언을 제공함으로써 상황을 좀 더 잘 이해할 수 있도록 돕습니다. 하지만 본 서비스가 실제 변호사나 법률 자격이 있는 것은 아니므로 조언의 이용에 대한 책임은 전적으로 사용자에게 있으며 참고용으로만 사용하시기 바랍니다. 정확하고 적법한 자문은 반드시 법률 자격을 갖춘 전문가와 상의하세요.")

# kakao adfit
kakao_adfit = """
<style>
    .adfit-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
    }
</style>

<div class="adfit-container">
    <ins class="kakao_ad_area" style="display:none;width:100%;"
	data-ad-unit = "DAN-hQpUDnckvfjqi2tK"
	data-ad-width = "320"
	data-ad-height = "100"></ins>
    <script async type="text/javascript" charset="utf-8" src="https://t1.daumcdn.net/kas/static/ba.min.js"></script>
</div>
"""
st.components.v1.html(kakao_adfit)

st.divider()
st.text("")


page_dict = {}
if st.session_state.job in ["법률 QnA"]:
    page_dict["QnA"] = question_pages
if st.session_state.job in ["서류작성"]:
    page_dict["Paperwork"] = paperwork_pages
#if st.session_state.job == "절차안내":
#    page_dict["Info"] = guide_pages


if len(page_dict) > 0:
    # LLM 에게 답변을 한번이라도 받았다면(페이지의 기능을 실행시켰다면) 사이드바의 이동경로를 없애서 무조건 첫페이지로만 이동하도록 만든다.
    if st.session_state.hide_main_side == False:
        pg = st.navigation({"Top": top_pages} | page_dict, position="sidebar")
    else:
        pg = st.navigation({"Top": top_pages} | page_dict, position="hidden")
else:
    pg = st.navigation([st.Page(start_task, title="AI Legal Assistant", icon=":material/gavel:")])


pg.run()


# 페이지 로드시 scroll position 을 top 으로 올린다. streamlit 에서 지원을 하지 않아 js 를 사용.
# 주의 할 점은 app(메인) 페이지 뿐만 아니라 하위 페이지도 모두 적용이 된다. 따라서 제한을 걸어야 한다.
if st.session_state.job == None:
    js = '''
    <script>
        var body = window.parent.document.querySelector(".main");
        console.log(body);
        body.scrollTop = 0;
    </script>
    '''
    st.components.v1.html(js)



#'''
#For running the streamlit server we need to run the following command:
#streamlit run streamlit_app.py

#It will launch the app in the browser, you can go to http://localhost:8501 The web app
#Press CTRL+C to quit
#'''

