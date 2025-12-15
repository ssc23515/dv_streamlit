import re
import html
from itertools import combinations
from collections import Counter

import numpy as np
import pandas as pd

import streamlit as st
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False

import seaborn as sns
import altair as alt
import plotly.express as px

from wordcloud import WordCloud
import networkx as nx

try:
    from pyvis.network import Network
    PYVIS_OK = True
except Exception:
    PYVIS_OK = False


# =========================
# 전처리
# =========================
def strip_tags(s: str) -> str:
    s = "" if s is None else str(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def normalize_text(s: str) -> str:
    s = strip_tags(s)
    s = re.sub(r"http\S+|www\.\S+", " ", s)
    s = re.sub(r"[^0-9A-Za-z가-힣\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# 기본 불용어 집합
DEFAULT_STOPWORDS = set([
    "있다","하다","되다","이다","그리고","그냥","진짜","너무","정말",
    "이번","오늘","내일","저번","관련","생각","느낌","가능","이유",
])

def simple_tokenize(s: str, stopwords: set):
    s = normalize_text(s)
    toks = [t for t in s.split() if len(t) >= 2]
    toks = [t for t in toks if t not in stopwords]
    return toks


# =========================
# 데이터가져오긴
# =========================
@st.cache_data(show_spinner=False)
def load_csv(file, encoding="utf-8-sig"):
    df = pd.read_csv(file, encoding=encoding)
    return df

def prepare_df(df: pd.DataFrame, col_date: str, col_title: str, col_desc: str, col_blogger: str,
               stopwords: set):
    out = df.copy()

    # 날짜 컬럼을 datetime으로 바꾸기ㅣ
    out[col_date] = pd.to_datetime(out[col_date], errors="coerce")
    out = out.dropna(subset=[col_date]).reset_index(drop=True)

    # 텍스트 합치기
    out["title_clean"] = out[col_title].fillna("").map(strip_tags)
    out["desc_clean"]  = out[col_desc].fillna("").map(strip_tags)
    out["text"] = (out["title_clean"] + " " + out["desc_clean"]).map(normalize_text)

    # 토큰
    out["tokens"] = out["text"].map(lambda x: simple_tokenize(x, stopwords))
    out["blogger_clean"] = out[col_blogger].fillna("").map(strip_tags)

    return out


# =========================
# 분석을 위한 함수
# =========================
def top_keywords(token_lists, top_n=30):
    all_tokens = [t for toks in token_lists for t in toks]
    return Counter(all_tokens).most_common(top_n)

def build_cooccurrence_edges(token_lists, top_vocab=80, min_count=5):
    vocab = set([w for w, _ in Counter([t for toks in token_lists for t in toks]).most_common(top_vocab)])

    edges = []
    for toks in token_lists:
        toks = [t for t in set(toks) if t in vocab]
        if len(toks) < 2:
            continue
        edges.extend(combinations(sorted(toks), 2))

    edge_counts = Counter(edges)
    edge_w = {e: c for e, c in edge_counts.items() if c >= min_count}
    return edge_w

def build_graph(edge_w: dict):
    G = nx.Graph()
    for (u, v), w in edge_w.items():
        G.add_edge(u, v, weight=w)
    return G

def centrality_table(G: nx.Graph, top_n=15):
    deg = nx.degree_centrality(G)
    rows = sorted(deg.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return pd.DataFrame(rows, columns=["keyword", "degree_centrality"])


# =========================
# Plotly 기반 팬덤 핵심요인 사전
# 임의로 나눠본 분류에 따라 케데헌에 대해 팬덤이 형성되는 요인을 나누어놓음.
# =========================
FACTOR_DICT = {
    "OST/음악": ["ost","노래","음악","보컬","랩","가사","golden",'빌보드'],
    "캐릭터/세계관": ["캐릭터","세계관","설정","호랑이","까치","더피"],
    "굿즈/팝업": ["굿즈","팝업","스토어","성수","예약","구매"],
    "팬덤/확산": ["팬","팬덤","입덕","덕질","바이럴","유행","밈","추천","공유","챌린지","후기"],
    "논란/이슈": ["논란","비판","불매","문제","혐오","실망","사건"],
}

def doc_factor_counts(tokens, factor_dict=FACTOR_DICT):
    # tokens는 공백기반이므로 lower 비교로 보정
    s = set([str(t).lower() for t in tokens])
    out = {}
    for f, kws in factor_dict.items():
        kws_l = [str(k).lower() for k in kws]
        out[f] = sum(k in s for k in kws_l)
    return out


# =========================
# Streamlit UI 부분
# =========================
st.set_page_config(page_title="Issue Finder (Template)", layout="wide")

# ---- 상단 헤더(학번/이름 필수 표기) ----
st.title("🧭 Issue Finder: 팬덤/여론 탐색 대시보드 (템플릿)")
st.caption("C321036 신상철")

INTRO_TEXT = "2025년 가장 이슈가 된 Netflix 드라마 '케데헌' 관련 블로그 데이터를 분석함."
if INTRO_TEXT.strip() != "":
    st.markdown(INTRO_TEXT)

# =========================
# (수정) 사이드바: 공통 위젯만 남김
# =========================
with st.sidebar:
    st.header("데이터 입력")
    uploaded = st.file_uploader("블로그 수집 CSV 업로드", type=["csv"])
    st.caption('CSV에 "postdate / title / description / bloggername" 컬럼이 있는 데이터 기준으로 만듦.')

    st.divider()
    st.header("공통 필터(모든 탭 공통 적용)")
    query_include = st.text_input("포함 키워드(선택)", value="케데헌")
    query_exclude = st.text_input("제외 키워드(선택)", value="")

    st.divider()
    st.header("불용어(간단)")
    add_stopwords = st.text_input("추가 불용어(쉼표로 구분)", value="케데헌,케이팝,데몬,헌터스")


# 데이터 없으면 안내
if not uploaded:
    st.info("왼쪽에서 CSV를 업로드하면 대시보드가 표시됩니다.")
    st.stop()

raw = load_csv(uploaded)

# -------------------------
# (유지) 컬럼 매핑은 기본값 고정
# -------------------------
col_date = "postdate"
col_title = "title"
col_desc = "description"
col_blogger = "bloggername"

# 불용어 세트 구성
stopwords = set(DEFAULT_STOPWORDS)
extra = [w.strip() for w in add_stopwords.split(",") if w.strip()]
stopwords.update(extra)

# 필수 컬럼 체크
for c in [col_date, col_title, col_desc, col_blogger]:
    if c not in raw.columns:
        st.error(f'CSV에 "{c}" 컬럼이 없습니다. (현재 컬럼: {list(raw.columns)[:30]}...)')
        st.stop()

# 준비 (유지: 제목+요약 사용)
df = raw.copy()
df = prepare_df(df, col_date, col_title, col_desc, col_blogger, stopwords)

# 포함/제외 키워드 필터
if query_include.strip():
    df = df[df["text"].str.contains(query_include.strip(), na=False)]
if query_exclude.strip():
    df = df[~df["text"].str.contains(query_exclude.strip(), na=False)]

if len(df) == 0:
    st.warning("필터 적용 후 데이터가 0건입니다. 포함/제외 조건을 조정하세요.")
    st.stop()

# KPI (metric은 날짜(datetime)  를 숫자로 못 받아서 문자열로)
dmin = df[col_date].min()
dmax = df[col_date].max()

c1, c2, c3, c4 = st.columns(4)
c1.metric("문서 수", f"{len(df):,}")
c2.metric("기간(최소)", str(dmin.date()) if pd.notna(dmin) else "-")
c3.metric("기간(최대)", str(dmax.date()) if pd.notna(dmax) else "-")
c4.metric("작성자 수", f"{df['blogger_clean'].nunique():,}")

# 날짜 범위 위젯 (데이터 있는 날짜만 선택 가능)
available_dates = sorted(df[col_date].dt.date.dropna().unique().tolist())

start_d, end_d = st.select_slider(
    "분석 기간(데이터 있는 날짜만 선택)",
    options=available_dates,
    value=(available_dates[0], available_dates[-1]),
)

mask = (df[col_date].dt.date >= start_d) & (df[col_date].dt.date <= end_d)
sub = df.loc[mask].copy()

if len(sub) == 0:
    st.warning("해당 기간 범위에 데이터가 없습니다.")
    st.stop()

# 탭(단일 페이지 안에서만)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Altair", "Seaborn", "Plotly", "WordCloud", "Network"
])

# =========================
# 그래프 1) Altair (흐름)  + (추가) 탭별 위젯 1개
# =========================
with tab1:
    freq = st.selectbox("집계 단위", ["D", "W", "M"], index=0, key="t1_freq")

    st.subheader("📈 언급량 추이 (Altair)")
    EXPLAIN_1 = "다양한 블로그에서 '케데헌' 관련 글이 언제 많이 작성되었는지 추이로 확인가능하였음. 다만 네이버 검색 api 특성상 blog 에서 가져온 내용이므로, " \
    "블로그에 들어가서 직접 확인하게 되면, 해쉬태그 등으로 관련없는 내용에서도 나타나기도 함.."  
    if EXPLAIN_1.strip() != "":
        st.markdown(EXPLAIN_1)

    ts = sub.set_index(col_date).resample(freq).size().rename("count").reset_index()
    chart = (
        alt.Chart(ts)
        .mark_line()
        .encode(
            x=alt.X(f"{col_date}:T", title="Date"),
            y=alt.Y("count:Q", title="Posts"),
            tooltip=[alt.Tooltip(f"{col_date}:T"), alt.Tooltip("count:Q")]
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader("샘플 문서")
    st.dataframe(sub[[col_date, "blogger_clean", "title_clean", "link"]].head(20), use_container_width=True)

# =========================
# 그래프 2) Seaborn (Top 키워드 막대) + (추가) 탭별 위젯 1개
# =========================
with tab2:
    topN_kw = st.slider("Top 키워드 개수", 10, 100, 30, 5, key="t2_topN")

    st.subheader("🏷️ Top 키워드 (Seaborn)")
    EXPLAIN_2 = "케데헌과 관련한 직접적인 단어들을 골라 확인함으로서 요즘 이슈나 트렌드가 되게 되면, 자연스럽게 따라오는 굿즈, 팝업스토어 등이 덩달아 많이 등장하는 것을 알 수 있었음." 
    if EXPLAIN_2.strip() != "":
        st.markdown(EXPLAIN_2)

    top_kw = top_keywords(sub["tokens"], top_n=topN_kw)
    kw_df = pd.DataFrame(top_kw, columns=["keyword", "count"])

    fig = plt.figure(figsize=(10, 5))
    sns.barplot(data=kw_df, x="count", y="keyword")
    plt.tight_layout()
    st.pyplot(fig)

    st.dataframe(kw_df, use_container_width=True)

# =========================
# 그래프 3) Plotly (교체: 팬덤 핵심요인 추이) + (추가) 탭별 위젯 1개
# =========================
with tab3:
    mode = st.radio("표현 방식", ["비율(%)", "카운트"], horizontal=True, key="t3_mode")

    st.subheader("📌 팬덤 형성 핵심요인 추이 (Plotly, 룰 기반)")
    EXPLAIN_3 = "논란과 같은 내용이 있어 유명해진 것이 아니라, 음악(OST), 캐릭터/세계관, 굿즈/팝업, 팬덤/확산 등의 요인들이 복합적으로 작용하여 케데헌이 이슈가 되고 팬덤이 형성된 것을 알 수 있었고, 사람들이 한 번 유명해진 이슈/트렌드에 대해서 관성저긍로 팬덤이 커지거나, 굿즈 팝업 등의 IP 산업이 활발하게 전개되고 관심도가 높음또한 알 수 있었음."  
    if EXPLAIN_3.strip() != "":
        st.markdown(EXPLAIN_3)

    factor_rows = sub["tokens"].apply(lambda toks: doc_factor_counts(toks, FACTOR_DICT))
    factor_df = pd.DataFrame(list(factor_rows))

    tmp = pd.concat([sub[[col_date]].reset_index(drop=True), factor_df.reset_index(drop=True)], axis=1)
    tmp = tmp.dropna(subset=[col_date])

    daily = (
        tmp.groupby(tmp[col_date].dt.date)[list(FACTOR_DICT.keys())]
        .sum()
        .reset_index()
        .rename(columns={col_date: "date"})
    )

    if mode.startswith("비율"):
        daily["total"] = daily[list(FACTOR_DICT.keys())].sum(axis=1).replace(0, np.nan)
        for f in FACTOR_DICT.keys():
            daily[f] = (daily[f] / daily["total"]) * 100.0

        fig = px.area(daily, x="date", y=list(FACTOR_DICT.keys()), title="핵심요인 비율(%) 추이")
        fig.update_yaxes(title="%")
    else:
        fig = px.area(daily, x="date", y=list(FACTOR_DICT.keys()), title="핵심요인 카운트 추이")
        fig.update_yaxes(title="count")

    st.plotly_chart(fig, use_container_width=True)
    st.caption("※ 형태소 분석 없이 tokens(공백 기반) + 키워드 사전으로 계산한 룰 기반 요약입니다.")

# =========================
# 그래프 4) WordCloud + (추가) 탭별 위젯 1개
# =========================
with tab4:
    wc_max_words = st.slider("WordCloud 최대 단어 수", 30, 300, 120, 10, key="t4_wc")

    st.subheader("☁️ WordCloud")
    EXPLAIN_4 = "Seaborn 과 유사한 내용을 워드클라우드라는 다른 시각화 방식으로 표현함으로서, 케데헌과 관련하여 자주 언급되는 단어들을 직관적인 모양으로 파악할 수 있었음." 
    if EXPLAIN_4.strip() != "":
        st.markdown(EXPLAIN_4)

    freq_counter = Counter([t for toks in sub["tokens"] for t in toks])


    FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"

    wc = WordCloud(
        font_path=FONT_PATH,
        background_color="white",
        width=1000,
        height=450,
        max_words=wc_max_words
    ).generate_from_frequencies(freq_counter)

    fig = plt.figure(figsize=(12, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)

# =========================
# 그래프 5) 네트워크 (pyvis 우선) + (추가) 탭별 위젯 1개
# =========================
with tab5:
    top_vocab = st.slider("네트워크 vocab(top)", 30, 300, 80, 10, key="t5_vocab")
    min_edge = st.slider("네트워크 edge 최소 동시출현(min_count)", 2, 50, 5, 1, key="t5_minEdge")

    st.subheader("🕸️ 키워드 관계망 (동시출현 네트워크)")
    EXPLAIN_5 = " 케데헌과 관련된 키워드들의 연관관계를 시각화함으로서, 주요 키워드들이 어떤 맥락에서 자주 함께 언급되는지를 파악할 수 있었고, 그로 인해 케데헌이 골든글로브에 노미네이트 되는 등 음악(OST)적인 측면에서 특히 주목받았음과 동시에 노이즈 또한 발견 가능했음." 
    if EXPLAIN_5.strip() != "":
        st.markdown(EXPLAIN_5)

    edge_w = build_cooccurrence_edges(sub["tokens"], top_vocab=top_vocab, min_count=min_edge)
    G = build_graph(edge_w)

    if G.number_of_nodes() == 0:
        st.warning("네트워크가 비었습니다. min_count를 낮추거나 vocab 크기를 늘려보세요.")
        st.stop()

    st.write("**중심성 Top 키워드**")
    st.dataframe(centrality_table(G, top_n=15), use_container_width=True)

    if PYVIS_OK:
        net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#222222")
        net.barnes_hut()

        for n in G.nodes():
            net.add_node(n, label=n)

        for u, v, d in G.edges(data=True):
            w = int(d.get("weight", 1))
            net.add_edge(u, v, value=w, title=f"co-occur: {w}")

        st.components.v1.html(net.generate_html(), height=650, scrolling=True)
    else:
        st.info("pyvis 미설치/환경 이슈로 NetworkX 기본 시각화로 대체합니다.")
        fig = plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G, k=0.7, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=500, font_size=9, font_family="Malgun Gothic")
        st.pyplot(fig)

st.divider()

# 다운로드
st.download_button(
    "📥 (필터 적용) 데이터 CSV 다운로드",
    data=sub.to_csv(index=False).encode("utf-8-sig"),
    file_name="filtered_blog_data.csv",
    mime="text/csv",
)

# (TODO) 맺음말/요약 자리
FOOTER_TEXT = ""
if FOOTER_TEXT.strip() != "":
    st.markdown(FOOTER_TEXT)


"""
[AI 주요 활용]
- 사용 목적: Streamlit/Altair/Plotly/Seaborn/WordCloud/NetworkX들의 사용법을 확인하고 오류의 원인을 확인하기 위해.
- 도움 받지 않은 부분: 해석들 및 그래프 선택 및 배치.
- 소명자료를 같이 제출 예정 AI 대화록 첨부
"""
