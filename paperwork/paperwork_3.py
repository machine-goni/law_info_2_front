# 서류작성 - 지급명령이의신청서 front-end

import streamlit as st
import json
import requests


#if st.session_state.init_backend == 200 and st.session_state.build != "write_paper_3":
#    inputs = {"workflow_type": "write_paper_3"}
#    result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
#    if result.status_code == 200:
#        st.session_state.build = "write_paper_3"
    
#elif st.session_state.init_backend != 200 and st.session_state.build != "write_paper_3":
#    init_result = requests.post(url=f"{st.session_state.backend_url}init")
#    st.session_state.init_backend = init_result.status_code
    
#    if st.session_state.init_backend == 200:
#        inputs = {"workflow_type": "write_paper_3"}
#        result = requests.post(url=f"{st.session_state.backend_url}build", data=json.dumps(inputs))
#        if result.status_code == 200:
#            st.session_state.build = "write_paper_3"
    
if "result_answer" not in st.session_state:
    st.session_state.result_answer = ""
    
    
with st.sidebar:
    st.caption(":material/release_alert: 아래의 [대한민국법원-전자민원센터] 홈페이지를 통해 법적 절차 안내, 사건검색 등 여러정보를 얻을 수 있습니다.")
    st.page_link("https://help.scourt.go.kr/nm/main/index.html", label="전자민원센터", icon=":material/link:")


new_title = '<p style="font-family:sans-serif; font-weight:bold; color:gray; font-size: 20px;">\"지급명령 이의신청서\" 작성을 도와드립니다.</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.text("")

st.subheader("지급명령 이의신청이란?")
explain = """
채무자는 민사소송법 제469조 제2항에 따라 지급명령에 대해 이의신청을 할 수 있습니다. 이의신청이 접수되면, 해당 지급명령의 효력은 민사소송법 제470조에 의하여 그 범위 내에서 상실되고, 민사소송법 제472조 제2항에 의하여 소송절차로 이행됩니다.

주요 이의사유   
- 사유 예시:
  1. 돈을 빌린 사실 또는 대금을 지급할 일이 없는 경우
  2. 이미 전부 혹은 일부를 갚았거나, 소멸시효 완성 등으로 청구금액이 틀린 경우
- 소멸시효: 권리를 행사하지 않아 일정 기간이 지나면 권리가 소멸하는 제도로, 민법은 10년(민법 제162조 1항), 상법은 5년(상법 제64조) 등의 기간을 정하고 있습니다.

이의신청 방법   
- 이의신청서는 이의신청서 부본과 함께 직접 지급명령을 발한 법원에 방문하거나 우편으로 제출할 수 있습니다(인지/송달료 없음). 또한 전자소송 홈페이지를 통해 온라인으로도 제출할 수 있습니다.
- 신청서에는 지급명령에 따를 이유가 없다는 취지를 기재하면 됩니다. 구체적인 불복 사유나 항변은 작성할 필요가 없습니다. 그러나 이의신청을 했다고 하더라도 모든 절차가 종결되는 것이 아니고 소송절차로 이행되는 것이기 때문에 지급명령신청을 기각해 달라는 답변서를 함께 제출하는것이 좋습니다(본래의 답변서 제출기간은 지급명령을 송달받은 날로부터 30일 이내 제출).
- 답변서에는 구체적으로 왜 채권자의 청구가 부당한지, 어떤 이유로 지급할 수 없는지를 자세히 설명해야 합니다.

이의신청 시기   
- 기간: 채무자가 지급명령을 송달받은 날부터 2주(14일) 이내에 해야 합니다.
- 유의사항: 2주 기간이 지나면 이의신청은 부적법하여 각하됩니다. 우편의 경우 2주 이내에 신청서를 작성하여 발송했더라도 도착일이 이의신청기간(14일)을 경과한다면 각하됩니다.
- 예외사항: 책임 없는 사유(어쩔 수 없는 이유)로 기간 내 이의신청을 못 했을 경우, 사유가 없어진 날부터 2주 내에 신청할 수 있습니다.
"""
expander = st.expander("자세히 보기")
expander.write(explain)
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제469조", label="민사소송법 제469조 제2항", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제470조", label="민사소송법 제470조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민사소송법/(20231019,19354,20230418)/제472조", label="민사소송법 제472조", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/민법/(20240517,19409,20230516)/제162조", label="민법 제162조 1항", icon=":material/link:")
expander.page_link(f"https://www.law.go.kr/법령/상법/(20201229,17764,20201229)/제64조", label="상법 제64조", icon=":material/link:")

st.text("")

st.warning("지급명령 이의신청서에 작성할 [사건], [채권자] 등의 내용은 송달받은 지급명령정본을 참고하여 작성하시면 됩니다.")

st.info("지급명령 이의신청서 양식은 [대한민국법원 전자민원센터]의 [양식모음]에서 받으실 수 있습니다.")
st.page_link(f"https://help.scourt.go.kr/nm/minwon/doc/DocListAction.work?pageIndex=1&pageSize=5&min_gubun=&sName=&eName=&min_gubun_sel=&searchWord=%C1%F6%B1%DE%B8%ED%B7%C9%BF%A1%B4%EB%C7%D1%C0%CC%C0%C7%BD%C5%C3%BB%BC%AD", label="대한민국법원 전자민원센터 - 양식모음 - 지급명령 이의신청서", icon=":material/link:")

st.text("")
st.warning("지급명령 이의신청서의 제출은 아래 주소의 [대한민국법원 전자소송] 홈페이지를 통해 온라인으로 제출할 수 있습니다([지급명령(독촉) 신청] 탭의 [지급명령에 대한 이의신청서]). 작성시 [이의사유]는 위 주소에서 제공되는 양식에 적힌 문구를 참조하세요.")
st.text("https://ecfs.scourt.go.kr/ecf/ecf300/ECF302.jsp#_")
st.caption("* [대한민국법원 전자소송] 저작권 정책상 URL을 알려드릴 뿐 링크를 제공하지 않음을 양해 바랍니다. 위 주소를 직접 주소창에 넣어 이동하시면 됩니다(혹은 드래그 후 우클릭).")

