"""
TalentMapper AI — Streamlit Application
"""
from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="TalentMapper AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ──────────────────────────────────────────────────────────────
ACCENT     = "#e94560"
SIDEBAR_BG = "#1a1a2e"
PAGE_BG    = "#f4f6f9"
CARD_BG    = "#ffffff"
TEXT_DARK  = "#1a1a2e"
TEXT_MID   = "#4a5568"
TEXT_LIGHT = "#718096"
BORDER     = "#e2e8f0"
GREEN      = "#22c55e"
ORANGE     = "#f97316"
PURPLE     = "#8b5cf6"
TEAL       = "#0ea5e9"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {PAGE_BG};
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
.main .block-container {{
    background-color: {PAGE_BG};
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}}
/* Sidebar — target every structural layer so it stays dark on all pages */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG} !important;
    min-height: 100vh;
}}
[data-testid="stSidebar"] * {{ color: #e2e8f0 !important; }}
[data-testid="stSidebar"] .stRadio > label {{
    color: #94a3b8 !important;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 700;
}}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
    color: #e2e8f0 !important;
    font-size: 0.94rem;
}}
[data-testid="stSidebar"] hr {{ border-color: #2d3561 !important; }}

[data-testid="metric-container"] {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] p {{
    color: {TEXT_MID} !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {TEXT_DARK} !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}}

button[kind="primary"] {{
    background-color: {ACCENT} !important;
    border-color: {ACCENT} !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}}
button[kind="primary"]:hover {{
    background-color: #c73852 !important;
    border-color: #c73852 !important;
}}

h1 {{ color: {TEXT_DARK} !important; font-weight: 800 !important; letter-spacing: -0.02em; }}
h2, h3 {{ color: {TEXT_DARK} !important; font-weight: 700 !important; }}

[data-testid="stTextInput"] input {{
    border-radius: 10px !important;
    border: 1.5px solid {BORDER} !important;
    font-size: 1rem !important;
    background: {CARD_BG} !important;
    padding: 10px 14px !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px rgba(233,69,96,0.10) !important;
}}

hr {{ border-color: {BORDER} !important; }}
[data-testid="stCheckbox"] label {{ color: {TEXT_DARK} !important; font-size: 0.9rem !important; }}

.tm-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}}
.tm-card:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.09); }}

.tm-badge {{
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin-right: 5px;
}}
.tm-badge-green  {{ background: #dcfce7; color: #15803d; }}
.tm-badge-blue   {{ background: #dbeafe; color: #1d4ed8; }}
.tm-badge-orange {{ background: #fff7ed; color: #c2410c; }}
.tm-badge-gray   {{ background: #f1f5f9; color: #475569; }}
.tm-badge-accent {{ background: #fde8ec; color: {ACCENT}; }}

.tm-skill-tag {{
    display: inline-block;
    background: #f1f5f9;
    color: {TEXT_MID};
    border-radius: 6px;
    padding: 2px 9px;
    font-size: 0.76rem;
    font-weight: 500;
    margin: 2px 3px 2px 0;
}}
.tm-skill-match {{ background: #dcfce7; color: #15803d; font-weight: 700; }}

.tm-label {{
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {TEXT_LIGHT};
    margin-bottom: 5px;
    margin-top: 10px;
}}
.tm-link {{ color: {ACCENT}; font-weight: 600; text-decoration: none; }}
.tm-link:hover {{ text-decoration: underline; }}

.tm-match-high {{ color: #15803d; font-weight: 800; font-size: 1.7rem; line-height: 1; }}
.tm-match-mid  {{ color: #b45309; font-weight: 800; font-size: 1.7rem; line-height: 1; }}
.tm-match-low  {{ color: #b91c1c; font-weight: 800; font-size: 1.7rem; line-height: 1; }}

.tm-chart-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 22px 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
.tm-chart-title {{
    font-size: 0.88rem;
    font-weight: 700;
    color: {TEXT_DARK};
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}}
</style>
""", unsafe_allow_html=True)


# ── Skill categories ───────────────────────────────────────────────────────────
SKILL_CATEGORIES: dict[str, dict] = {
    "Food & Hospitality": {
        "skills": ["Cooking", "Serving", "Bartending", "Hosting", "Barista", "Food Prep", "Baking", "Kitchen Management"],
        "color": ORANGE,
    },
    "Animal Care": {
        "skills": ["Pet Grooming", "Vet Tech", "Pet Handling", "Dog Walking", "Pet Sitting", "Animal Care"],
        "color": GREEN,
    },
    "Cleaning & Facility Services": {
        "skills": ["Housekeeping", "Sanitation", "Laundry Services", "Deep Cleaning", "Janitorial"],
        "color": TEAL,
    },
    "Management & Operations": {
        "skills": ["Scheduling", "Hiring & Recruiting", "Team Leadership", "Operations Management", "Supervision"],
        "color": PURPLE,
    },
    "Data & Analytics": {
        "skills": ["Reporting", "Excel / Spreadsheets", "Inventory Management", "Data Entry", "Analytics"],
        "color": ACCENT,
    },
}

ALL_SKILLS: list[str] = [s for cat in SKILL_CATEGORIES.values() for s in cat["skills"]]

# ── Mock analytics data ────────────────────────────────────────────────────────
MOCK_ANALYTICS = {
    "total_searches":    47,
    "total_businesses":  230,
    "total_hr_signals":  184,
    "total_career_pages": 201,
    "top_categories":    ["Food & Beverage", "Animal Care", "Amusement & Rec", "Cleaning & Facility", "Retail & Specialty"],
    "category_counts":   [89, 45, 38, 31, 27],
    "email_labels":      ["HR Signal", "Sales Contact", "Ambiguous"],
    "email_counts":      [184, 92, 41],
    "skill_categories":  ["Cleaning & Facility", "Food & Hospitality", "Management & Ops", "Animal Care", "Data & Analytics"],
    "skill_match_rates": [81, 72, 64, 58, 43],
    "timeline_days":     ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "timeline_counts":   [5, 8, 12, 7, 6, 4, 5],
}

# ── Graph node config ──────────────────────────────────────────────────────────
GRAPH_COLORS = {
    "business": ACCENT, "group": SIDEBAR_BG, "skill": GREEN,
    "email": ORANGE, "career": PURPLE, "signal_label": TEAL, "unknown": "#94a3b8",
}
GRAPH_SIZES = {
    "business": 26, "group": 18, "skill": 13,
    "email": 13, "career": 15, "signal_label": 16, "unknown": 11,
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _skill_match(user_skills: list[str], required: list[str]):
    """Returns (pct, matched_list, missing_list)."""
    if not required:
        return 0, [], []
    matched = [s for s in required if s in user_skills]
    missing = [s for s in required if s not in user_skills]
    return round(len(matched) / len(required) * 100), matched, missing


def _stars(rating: float) -> str:
    n = round(float(rating)) if rating else 0
    return "★" * n + "☆" * (5 - n)


def _skill_tags_html(skills: list[str], highlight: set | None = None) -> str:
    parts = []
    for s in skills:
        cls = "tm-skill-tag tm-skill-match" if (highlight and s in highlight) else "tm-skill-tag"
        parts.append('<span class="' + cls + '">' + s + "</span>")
    return "".join(parts)


def _chart_base(height: int = 280) -> dict:
    return dict(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="system-ui, -apple-system, sans-serif", color=TEXT_DARK, size=12),
        margin=dict(l=10, r=10, t=24, b=10),
        showlegend=False,
    )


# ── Chart builders ─────────────────────────────────────────────────────────────

def _chart_categories() -> go.Figure:
    d = MOCK_ANALYTICS
    fig = go.Figure(go.Bar(
        x=d["category_counts"],
        y=d["top_categories"],
        orientation="h",
        marker_color=ACCENT,
        text=[str(v) for v in d["category_counts"]],
        textposition="outside",
        textfont=dict(size=11, color=TEXT_MID),
    ))
    layout = _chart_base(260)
    layout["xaxis"] = dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, showticklabels=False)
    layout["yaxis"] = dict(showgrid=False, zeroline=False, autorange="reversed")
    fig.update_layout(**layout)
    return fig


def _chart_email_dist() -> go.Figure:
    d = MOCK_ANALYTICS
    fig = go.Figure(go.Pie(
        labels=d["email_labels"],
        values=d["email_counts"],
        hole=0.58,
        marker=dict(colors=[GREEN, ORANGE, "#94a3b8"], line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate="%{label}: %{value}<extra></extra>",
    ))
    layout = _chart_base(260)
    layout["showlegend"] = False
    layout["annotations"] = [dict(
        text="<b>317</b><br>total",
        x=0.5, y=0.5,
        font=dict(size=13, color=TEXT_DARK),
        showarrow=False,
    )]
    fig.update_layout(**layout)
    return fig


def _chart_skill_match_rate() -> go.Figure:
    d = MOCK_ANALYTICS
    rates = d["skill_match_rates"]
    colors = [GREEN if r >= 70 else ORANGE if r >= 50 else ACCENT for r in rates]
    fig = go.Figure(go.Bar(
        x=rates,
        y=d["skill_categories"],
        orientation="h",
        marker_color=colors,
        text=[str(r) + "%" for r in rates],
        textposition="outside",
        textfont=dict(size=11, color=TEXT_MID),
    ))
    layout = _chart_base(260)
    layout["xaxis"] = dict(range=[0, 100], showgrid=True, gridcolor="#f1f5f9", zeroline=False, showticklabels=False)
    layout["yaxis"] = dict(showgrid=False, zeroline=False, autorange="reversed")
    fig.update_layout(**layout)
    return fig


def _chart_timeline() -> go.Figure:
    d = MOCK_ANALYTICS
    fig = go.Figure(go.Scatter(
        x=d["timeline_days"],
        y=d["timeline_counts"],
        mode="lines+markers",
        fill="tozeroy",
        line=dict(color=ACCENT, width=2.5),
        fillcolor="rgba(233,69,96,0.08)",
        marker=dict(color=ACCENT, size=7, line=dict(color="white", width=2)),
        hovertemplate="%{x}: %{y} searches<extra></extra>",
    ))
    layout = _chart_base(260)
    layout["xaxis"] = dict(showgrid=False, zeroline=False)
    layout["yaxis"] = dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False)
    fig.update_layout(**layout)
    return fig


# ── Page: Search ──────────────────────────────────────────────────────────────

def render_search():
    st.markdown("## TalentMapper AI")
    st.markdown(
        '<p style="color:' + TEXT_MID + ';font-size:1.05rem;margin-top:-6px;margin-bottom:24px;">'
        "TalentMapper AI finds businesses actively hiring for your skills "
        "— bypassing job boards entirely."
        "</p>",
        unsafe_allow_html=True,
    )

    # ── Search input
    query = st.text_input(
        "prompt",
        placeholder='e.g. "cafe jobs in Chicago" or "pet care near Austin"',
        value=st.session_state.last_query,
        label_visibility="collapsed",
    )

    examples = ["cafe jobs in Chicago", "pet care in Austin", "cleaning jobs in New York", "entertainment venues in Denver"]
    ex_cols = st.columns(len(examples))
    search_triggered = False
    for i, ex in enumerate(examples):
        if ex_cols[i].button(ex, key="ex_" + str(i), use_container_width=True):
            query = ex
            search_triggered = True

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Radius + Skills
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
        st.markdown("**Search radius**")
        radius = st.radio(
            "radius",
            [1, 5, 10, 25],
            format_func=lambda x: str(x) + (" mile" if x == 1 else " miles"),
            index=st.session_state.get("radius_idx", 1),
            label_visibility="collapsed",
        )
        st.session_state.radius_idx = [1, 5, 10, 25].index(radius)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Find Matching Jobs", type="primary", use_container_width=True):
            search_triggered = True

    with right_col:
        st.markdown("**Your skills** — select everything you can do")
        st.markdown("<br>", unsafe_allow_html=True)
        for cat_name, cat_data in SKILL_CATEGORIES.items():
            st.markdown(
                '<span style="font-size:0.78rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:0.07em;color:' + TEXT_LIGHT + ';">' + cat_name + "</span>",
                unsafe_allow_html=True,
            )
            skill_cols = st.columns(2)
            for j, skill in enumerate(cat_data["skills"]):
                default_checked = skill in st.session_state.get("user_skills", [])
                skill_cols[j % 2].checkbox(skill, value=default_checked, key="skill_" + skill)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Collect selected skills from widget state
    current_skills = [s for s in ALL_SKILLS if st.session_state.get("skill_" + s, False)]
    st.session_state.user_skills = current_skills

    # ── Run pipeline
    if search_triggered and query.strip():
        st.session_state.last_query = query
        st.session_state.search_radius = radius

        with st.spinner("Running pipeline..."):
            import time
            from pipeline.discovery import parse_prompt, search_businesses
            from pipeline.skill_tagger import tag_all
            from pipeline.email_classifier import classify_all
            from pipeline.career_detector import detect_all
            from pipeline.graph_rag import build_graph

            prog = st.progress(0, text="Parsing prompt...")
            parsed = parse_prompt(query)
            time.sleep(0.2)
            prog.progress(20, text="Discovering businesses...")
            businesses = search_businesses(parsed)
            businesses = [b for b in businesses if b.get("distance_miles", 0) <= radius]
            time.sleep(0.25)
            prog.progress(45, text="Tagging skills...")
            businesses = tag_all(businesses)
            time.sleep(0.2)
            prog.progress(65, text="Classifying emails...")
            businesses = classify_all(businesses)
            time.sleep(0.15)
            prog.progress(82, text="Detecting career pages...")
            businesses = detect_all(businesses)
            time.sleep(0.1)
            prog.progress(95, text="Building knowledge graph...")
            st.session_state.graph = build_graph(businesses)
            prog.progress(100, text="Done.")
            st.session_state.results = businesses
            st.session_state.parsed_prompt = parsed

        match_pcts = [_skill_match(current_skills, b.get("required_skills", []))[0] for b in businesses]
        avg_match = round(sum(match_pcts) / max(len(match_pcts), 1))
        hr_count = sum(1 for b in businesses if b.get("has_hr_signal"))
        career_count = sum(1 for b in businesses if b.get("has_career_page"))

        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Businesses Found", len(businesses))
        m2.metric("HR Signals", hr_count)
        m3.metric("Avg Skill Match", str(avg_match) + "%")
        m4.metric("Career Pages", career_count)
        st.success("Search complete — view results on the **Results** page.")

    elif search_triggered:
        st.warning("Enter a search prompt to continue.")

    if not st.session_state.results:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Select your skills and enter a prompt above to get started. No API keys required.")


# ── Page: Results ─────────────────────────────────────────────────────────────

def render_results():
    if not st.session_state.results:
        st.info("Run a search first on the Search page.")
        return

    businesses = st.session_state.results
    parsed = st.session_state.get("parsed_prompt", {})
    user_skills = st.session_state.get("user_skills", [])
    radius = st.session_state.get("search_radius", 10)

    st.markdown("## Results")
    btype = parsed.get("business_type", "Businesses")
    bloc = parsed.get("location", "your area")
    st.markdown(
        '<p style="color:' + TEXT_MID + ';margin-top:-6px;margin-bottom:20px;">'
        + btype + " near " + bloc
        + " &nbsp;·&nbsp; within " + str(radius) + " mile" + ("s" if radius != 1 else "")
        + " &nbsp;·&nbsp; " + str(len(user_skills)) + " skill" + ("s" if len(user_skills) != 1 else "") + " selected"
        + "</p>",
        unsafe_allow_html=True,
    )

    match_pcts = [_skill_match(user_skills, b.get("required_skills", []))[0] for b in businesses]
    hr_count = sum(1 for b in businesses if b.get("has_hr_signal"))
    career_count = sum(1 for b in businesses if b.get("has_career_page"))
    avg_match = round(sum(match_pcts) / max(len(match_pcts), 1))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Businesses", len(businesses))
    m2.metric("HR Signals", hr_count)
    m3.metric("Your Avg Match", str(avg_match) + "%")
    m4.metric("Career Pages", career_count)
    st.markdown("<br>", unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3 = st.columns([2, 2, 3])
    with fc1:
        only_high = st.checkbox("High match only (≥ 60%)", value=False)
    with fc2:
        only_hr = st.checkbox("Hiring signal only", value=False)
    with fc3:
        sort_opt = st.selectbox(
            "Sort",
            ["Match % — high to low", "Rating — high to low", "Distance — nearest first"],
            label_visibility="collapsed",
        )

    enriched = list(zip(businesses, match_pcts))
    if only_high:
        enriched = [(b, p) for b, p in enriched if p >= 60]
    if only_hr:
        enriched = [(b, p) for b, p in enriched if b.get("has_hr_signal")]
    if sort_opt.startswith("Match"):
        enriched.sort(key=lambda x: x[1], reverse=True)
    elif sort_opt.startswith("Rating"):
        enriched.sort(key=lambda x: x[0].get("rating", 0), reverse=True)
    else:
        enriched.sort(key=lambda x: x[0].get("distance_miles", 99))

    st.markdown(
        "Showing **" + str(len(enriched)) + "** of " + str(len(businesses)) + " businesses",
    )
    st.divider()

    for biz, pct in enriched:
        _render_business_card(biz, pct, user_skills)

    st.divider()
    import pandas as pd
    rows = [{
        "name": b["name"],
        "address": b.get("address", ""),
        "rating": b.get("rating", ""),
        "distance_miles": b.get("distance_miles", ""),
        "skill_match_pct": p,
        "has_hr_signal": b.get("has_hr_signal", False),
        "top_hr_email": b.get("top_hr_email", ""),
        "has_career_page": b.get("has_career_page", False),
        "career_page_url": b.get("career_page_url", ""),
        "required_skills": ", ".join(b.get("required_skills", [])),
    } for b, p in enriched]
    csv = pd.DataFrame(rows).to_csv(index=False)
    st.download_button("Download CSV", csv, "talentmapper_results.csv", "text/csv")


def _render_business_card(biz: dict, match_pct: int, user_skills: list[str]):
    required = biz.get("required_skills", [])
    _, matched, _ = _skill_match(user_skills, required)
    matched_set = set(matched)

    if match_pct >= 70:
        pct_cls, ring = "tm-match-high", GREEN
    elif match_pct >= 40:
        pct_cls, ring = "tm-match-mid", ORANGE
    else:
        pct_cls, ring = "tm-match-low", "#ef4444"

    # Status badges
    badges = ""
    if biz.get("has_hr_signal"):
        badges += '<span class="tm-badge tm-badge-green">HR Signal</span>'
    if biz.get("has_career_page"):
        badges += '<span class="tm-badge tm-badge-blue">Career Page</span>'
    dist = biz.get("distance_miles", "?")
    badges += '<span class="tm-badge tm-badge-gray">' + str(dist) + " mi</span>"

    # Email classification rows
    email_rows = ""
    for ec in biz.get("email_classifications", []):
        label = ec.get("label", "")
        email = ec.get("email", "")
        conf = ec.get("confidence", 0)
        if label == "HR":
            badge_cls = "tm-badge tm-badge-green"
        elif label == "Sales":
            badge_cls = "tm-badge tm-badge-orange"
        else:
            badge_cls = "tm-badge tm-badge-gray"
        conf_str = str(round(conf * 100)) + "%"
        email_rows += (
            '<div style="margin:3px 0;">'
            '<code style="font-size:0.81rem;color:' + TEXT_MID + ';background:#f8fafc;'
            'padding:1px 6px;border-radius:4px;">' + email + "</code>"
            ' &nbsp;<span class="' + badge_cls + '">' + label + " · " + conf_str + "</span>"
            "</div>"
        )

    # Career link
    career_row = ""
    if biz.get("has_career_page") and biz.get("career_page_url"):
        url = biz["career_page_url"]
        career_row = (
            '<div style="margin-top:4px;">'
            '<a class="tm-link" href="' + url + '" target="_blank">'
            "View career page &rarr;"
            "</a></div>"
        )

    # Skill tags
    skills_html = _skill_tags_html(required, highlight=matched_set)
    no_match_msg = '<em style="color:#94a3b8;font-size:0.81rem">No skills match — consider expanding your selection</em>'
    matched_html = _skill_tags_html(matched, highlight=matched_set) if matched else no_match_msg

    name = biz.get("name", "")
    address = biz.get("address", "")
    rating = biz.get("rating", 0)
    desc = biz.get("description", "")
    match_count_str = str(len(matched)) + "/" + str(len(required))

    st.markdown(
        '<div class="tm-card">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:18px;">'

        # Left: main content
        '<div style="flex:1;min-width:0;">'
        '<div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:5px;">'
        '<span style="font-size:1.05rem;font-weight:700;color:' + TEXT_DARK + ';">' + name + "</span>"
        + badges +
        "</div>"
        '<div style="color:' + TEXT_MID + ';font-size:0.86rem;margin-bottom:3px;">'
        + address +
        ' &nbsp;·&nbsp; <span style="color:#d97706;font-weight:600;">' + _stars(rating) + " " + str(rating) + "</span>"
        "</div>"
        '<div style="color:' + TEXT_LIGHT + ';font-size:0.85rem;margin-bottom:12px;">' + desc + "</div>"

        '<div class="tm-label">Skills needed</div>'
        '<div style="margin-bottom:8px;">' + (skills_html if skills_html else "<em>—</em>") + "</div>"

        '<div class="tm-label">Your matching skills</div>'
        '<div style="margin-bottom:8px;">' + matched_html + "</div>"

        + ('<div class="tm-label">Contact signals</div>' + email_rows + career_row if (email_rows or career_row) else "") +
        "</div>"

        # Right: match score panel
        '<div style="text-align:center;flex-shrink:0;background:#f8fafc;border-radius:12px;'
        'padding:16px 18px;border:2px solid ' + ring + "22;min-width:86px;max-width:100px;\">"
        '<div class="' + pct_cls + '">' + str(match_pct) + "%</div>"
        '<div style="font-size:0.68rem;font-weight:800;text-transform:uppercase;'
        'letter-spacing:0.07em;color:' + TEXT_LIGHT + ';margin-top:2px;">Match</div>'
        '<div style="font-size:0.78rem;color:' + TEXT_MID + ';margin-top:8px;">' + match_count_str + " skills</div>"
        "</div>"

        "</div></div>",
        unsafe_allow_html=True,
    )


# ── Page: Analytics Dashboard ─────────────────────────────────────────────────

def render_analytics():
    st.markdown("## Analytics Dashboard")
    st.markdown(
        '<p style="color:' + TEXT_MID + ';margin-top:-6px;margin-bottom:24px;">'
        "Aggregate intelligence from all searches run through TalentMapper AI."
        "</p>",
        unsafe_allow_html=True,
    )

    d = MOCK_ANALYTICS

    # ── Metric cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Searches", d["total_searches"])
    m2.metric("Businesses Discovered", d["total_businesses"])
    m3.metric("HR Signals Detected", d["total_hr_signals"])
    m4.metric("Career Pages Found", d["total_career_pages"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 1
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="tm-chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="tm-chart-title">Top Business Categories</div>', unsafe_allow_html=True)
        st.plotly_chart(_chart_categories(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="tm-chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="tm-chart-title">Email Signal Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(_chart_email_dist(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 2
    c3, c4 = st.columns(2, gap="large")
    with c3:
        st.markdown('<div class="tm-chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="tm-chart-title">Skill Match Rate by Category</div>', unsafe_allow_html=True)
        st.plotly_chart(_chart_skill_match_rate(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="tm-chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="tm-chart-title">Searches — Last 7 Days</div>', unsafe_allow_html=True)
        st.plotly_chart(_chart_timeline(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Mini knowledge graph
    st.markdown("### Knowledge Graph")
    st.markdown(
        '<p style="color:' + TEXT_MID + ';font-size:0.9rem;margin-top:-6px;margin-bottom:16px;">'
        "Relationships between businesses, skill requirements, email signals, and career pages."
        "</p>",
        unsafe_allow_html=True,
    )

    if st.session_state.graph is None:
        st.info("Run a search on the Search page to populate the knowledge graph.")
        return

    _render_mini_graph()


def _render_mini_graph():
    import networkx as nx
    from pipeline.graph_rag import graph_stats, query_hr_signals

    G = st.session_state.graph
    stats = graph_stats(G)

    gs1, gs2, gs3 = st.columns(3)
    gs1.metric("Nodes", stats["total_nodes"])
    gs2.metric("Edges", stats["total_edges"])
    gs3.metric("HR Signals", len(query_hr_signals(G)))

    st.markdown("<br>", unsafe_allow_html=True)

    # Node type filter
    node_types = list(stats["node_types"].keys())
    selected = st.multiselect("Filter node types", options=node_types, default=node_types, key="graph_filter")
    visible_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type", "unknown") in selected]
    sub_G = G.subgraph(visible_nodes).copy() if visible_nodes else nx.DiGraph()

    if sub_G.number_of_nodes() == 0:
        st.warning("No nodes visible — adjust the filter above.")
        return

    try:
        pos = nx.kamada_kawai_layout(sub_G)
    except Exception:
        pos = nx.circular_layout(sub_G)

    node_x, node_y, node_text, node_color, node_size, node_hover = [], [], [], [], [], []
    for nid, data in sub_G.nodes(data=True):
        x, y = pos[nid]
        ntype = data.get("node_type", "unknown")
        label = data.get("label", nid.split("::")[-1])
        node_x.append(x)
        node_y.append(y)
        node_text.append(label)
        node_color.append(GRAPH_COLORS.get(ntype, "#94a3b8"))
        node_size.append(GRAPH_SIZES.get(ntype, 11))
        hover = "<b>" + label + "</b><br>Type: " + ntype
        if ntype == "email":
            hover += "<br>Signal: " + data.get("email_label", "?")
        node_hover.append(hover)

    edge_x, edge_y = [], []
    for u, v in sub_G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    fig = go.Figure(
        data=[
            go.Scatter(x=edge_x, y=edge_y, mode="lines",
                       line=dict(width=1, color="#cbd5e1"), hoverinfo="none"),
            go.Scatter(
                x=node_x, y=node_y,
                mode="markers+text",
                text=node_text,
                textposition="top center",
                textfont=dict(size=9, color=TEXT_DARK),
                hovertext=node_hover,
                hoverinfo="text",
                marker=dict(size=node_size, color=node_color,
                            line=dict(width=1.5, color="white")),
            ),
        ],
        layout=go.Layout(
            height=420,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=10, l=10, r=10, t=10),
            paper_bgcolor="white",
            plot_bgcolor=PAGE_BG,
            font=dict(color=TEXT_DARK),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Legend
    legend_items = [
        ("Business", ACCENT), ("Group", SIDEBAR_BG), ("Skill", GREEN),
        ("Email", ORANGE), ("Career", PURPLE), ("Label", TEAL),
    ]
    legend_parts = []
    for name, color in legend_items:
        legend_parts.append(
            '<span style="display:inline-flex;align-items:center;gap:5px;margin-right:14px;">'
            '<span style="width:10px;height:10px;border-radius:50%;background:' + color + ';display:inline-block;"></span>'
            '<span style="font-size:0.8rem;color:' + TEXT_MID + ';">' + name + "</span>"
            "</span>"
        )
    st.markdown(
        '<div style="margin-top:8px;">' + "".join(legend_parts) + "</div>",
        unsafe_allow_html=True,
    )


# ── Session state init ────────────────────────────────────────────────────────
_defaults = [
    ("results", []), ("graph", None), ("last_query", ""),
    ("parsed_prompt", {}), ("user_skills", []), ("search_radius", 10), ("radius_idx", 1),
]
for _key, _val in _defaults:
    if _key not in st.session_state:
        st.session_state[_key] = _val

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:10px 0 6px;">'
        '<div style="font-size:1.35rem;font-weight:800;color:#ffffff;letter-spacing:-0.01em;">'
        "🎯 TalentMapper AI"
        "</div>"
        '<div style="font-size:0.78rem;color:#64748b;margin-top:4px;line-height:1.5;">'
        "Business intelligence<br>and talent signal detection"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    page = st.radio(
        "Navigation",
        ["Search", "Results", "Analytics"],
        index=0,
    )

# ── Router ────────────────────────────────────────────────────────────────────
if page == "Search":
    render_search()
elif page == "Results":
    render_results()
else:
    render_analytics()
