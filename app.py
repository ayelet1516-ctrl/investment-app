import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Smart Investment Tool",
    page_icon="📈",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .stRadio > div {
        direction: rtl;
    }
    .stSlider > div {
        direction: ltr;
    }
    label {
        direction: rtl;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: right; direction: rtl;">
    <h1>אפליקציית חישוב סיכון והשקעה 📈</h1>
    <p style="font-size: 18px; color: gray;">ענה על 5 שאלות קצרות וקבל המלצה מותאמת אישית ✨</p>
    (מיועד למשקיעים מתחילים שרוצים להבין את פרופיל הסיכון שלהם — בלי ארגון פיננסי.)
</div>
""", unsafe_allow_html=True)

st.divider()

q1 = st.radio(
    "1. אם ההשקעה שלך ירדה 20% תוך חודש, מה היית עושה?",
    ["מוכר מיד — לא יכול לשאת את זה", "מוכר חלק מתיק ההשקעה", "ממתין ולא עושה כלום", "קונה עוד — זו הזדמנות"]
)
st.divider()

q2 = st.radio(
    "2. מה טווח ההשקעה שלך?",
    ["פחות משנה", "1–3 שנים", "3–10 שנים", "יותר מ-10 שנים"]
)
st.divider()

q3 = st.radio(
    "3. מה מטרת ההשקעה?",
    ["לשמור על ערך הכסף", "צמיחה מתונה ויציבה", "צמיחה מהירה — מוכן לסיכון", "מקסום תשואה בכל מחיר"]
)
st.divider()

q4 = st.radio(
    "4. כמה מהחסכונות שלך אתה מוכן להשקיע?",
    ["פחות מ-20%", "20%–40%", "40%–70%", "יותר מ-70%"]
)
st.divider()

st.write("5. כמה כסף אתה רוצה להשקיע?")
amount = st.slider("גרור לבחירת סכום", min_value=5000, max_value=1000000, value=50000, step=5000)
st.write(f"💰 סכום להשקעה: ₪{amount:,}")
st.divider()

# --- פונקציות ---
def calc_profile(q1, q2, q3, q4):
    score = 0
    score += ["מוכר מיד — לא יכול לשאת את זה", "מוכר חלק מתיק ההשקעה", "ממתין ולא עושה כלום", "קונה עוד — זו הזדמנות"].index(q1)
    score += ["פחות משנה", "1–3 שנים", "3–10 שנים", "יותר מ-10 שנים"].index(q2)
    score += ["לשמור על ערך הכסף", "צמיחה מתונה ויציבה", "צמיחה מהירה — מוכן לסיכון", "מקסום תשואה בכל מחיר"].index(q3)
    score += ["פחות מ-20%", "20%–40%", "40%–70%", "יותר מ-70%"].index(q4)
    if score <= 2:
        return "שמרני", [0.65, 0.20, 0.12, 0.03], score
    elif score <= 5:
        return "מתון", [0.45, 0.20, 0.28, 0.07], score
    elif score <= 8:
        return "מאוזן", [0.25, 0.15, 0.42, 0.18], score
    else:
        return "אגרסיבי", [0.10, 0.08, 0.45, 0.37], score

def calc_metrics(weights, returns, risks):
    port_return = sum(w * r for w, r in zip(weights, returns))
    port_risk   = np.sqrt(sum((w * r) ** 2 for w, r in zip(weights, risks)))
    sharpe      = (port_return - 0.045) / port_risk
    return port_return, port_risk, sharpe

def future_value(amount, annual_return, years):
    return [amount * (1 + annual_return) ** y for y in range(years + 1)]

def get_horizon(q2):
    mapping = {
        "פחות משנה": 1,
        "1–3 שנים": 3,
        "3–10 שנים": 10,
        "יותר מ-10 שנים": 20
    }
    return mapping[q2]

assets  = ["אג\"ח ממשלתי", "זהב", "S&P 500", "NASDAQ"]
returns = [0.043, 0.078, 0.121, 0.183]
risks   = [0.051, 0.124, 0.152, 0.221]
colors  = ["#185FA5", "#854F0B", "#0F6E56", "#993C1D"]

all_profiles = {
    "שמרני":   [0.65, 0.20, 0.12, 0.03],
    "מתון":    [0.45, 0.20, 0.28, 0.07],
    "מאוזן":   [0.25, 0.15, 0.42, 0.18],
    "אגרסיבי": [0.10, 0.08, 0.45, 0.37],
}
future_colors = {
    "שמרני": "#185FA5",
    "מתון": "#854F0B",
    "מאוזן": "#0F6E56",
    "אגרסיבי": "#993C1D"
}
if st.button("חשב את הבחירות שלי ←"):

    st.markdown("""
        <style>
        h2, h3 {
            direction: rtl !important;
            text-align: right !important;
        }
        </style>
    """, unsafe_allow_html=True)

    profile, weights, score = calc_profile(q1, q2, q3, q4)
    port_return, port_risk, sharpe = calc_metrics(weights, returns, risks)
    horizon = get_horizon(q2)

    st.subheader(f"הפרופיל שלך: {profile}")

    # --- מד סיכון ---
    st.write("**מד הסיכון שלך:**")
    risk_pct = min(score / 12, 1.0)

    bar_html = f"""
    <div style="
        background: linear-gradient(to left, #22c55e, #eab308, #f97316, #ef4444);
        border-radius: 10px;
        height: 24px;
        width: 100%;
        position: relative;
        margin-bottom: 6px;
    ">
        <div style="
            position: absolute;
            right: {risk_pct*100:.0f}%;
            top: -6px;
            transform: translateX(50%);
            font-size: 22px;
        ">▼</div>
    </div>

    <div style="
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: gray;
        direction: rtl;
    ">
        <span>🟢 שמרני</span>
        <span>🟡 מתון</span>
        <span>🟠 מאוזן</span>
        <span>🔴 אגרסיבי</span>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3)
    col1.metric("תשואה שנתית צפויה", f"{port_return*100:.1f}%")
    col2.metric("סיכון (סטיית תקן)", f"{port_risk*100:.1f}%")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

    st.divider()

    # --- גרף עוגה ---
    fig_pie = go.Figure(go.Pie(
        labels=assets,
        values=weights,
        marker_colors=colors,
        hole=0.4
    ))
    fig_pie.update_layout(
        title=dict(text="הקצאת נכסים", x=0.95, xanchor="right"),
        height=350
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    for i, asset in enumerate(assets):
        st.write(f"• {asset}: {weights[i]*100:.0f}% = ₪{amount*weights[i]:,.0f}")

    st.divider()

    # --- גרף סיכון מול תשואה ---
    st.subheader(" סיכון מול תשואה — כל הפרופילים📊")

    fig_f = go.Figure()

    for name, w in all_profiles.items():
        r, s, _ = calc_metrics(w, returns, risks)
        is_mine = name == profile

        fig_f.add_trace(go.Scatter(
            x=[s * 100],
            y=[r * 100],
            mode="markers+text",
            name=name,
            marker=dict(
                size=22 if is_mine else 14,
                color=future_colors[name],
                symbol="star" if is_mine else "circle",
                line=dict(color="white", width=2)
            ),
            text=[f"  {name}"],
            textposition="middle right",
            textfont=dict(
                size=13 if is_mine else 11,
                color=future_colors[name]
            )
        ))

    fig_f.update_layout(
        title=dict(text="סיכון מול תשואה — איפה הפרופיל שלך?", x=0.95, xanchor="right"),
        xaxis_title="סיכון — סטיית תקן (%)",
        yaxis_title="תשואה שנתית (%)",
        height=400,
        showlegend=False,
        xaxis=dict(gridcolor="#E5E7EB", range=[0, 15]),
        yaxis=dict(gridcolor="#E5E7EB", range=[0, 15]),
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_f, use_container_width=True)
    st.caption(f"★ הכוכב מסמן את הפרופיל שלך: {profile}")

    st.divider()

    # --- השוואת תרחישים ---
    st.subheader(" השוואת תרחישים🔀")

    profile_names, profile_rets, profile_risks = [], [], []

    for name, w in all_profiles.items():
        r, s, _ = calc_metrics(w, returns, risks)
        profile_names.append(name)
        profile_rets.append(round(r * 100, 1))
        profile_risks.append(round(s * 100, 1))

    fig_compare = go.Figure()

    fig_compare.add_trace(go.Bar(
        name="תשואה %",
        x=profile_names,
        y=profile_rets,
        marker_color=["#0F6E56" if n == profile else "#CBD5E1" for n in profile_names],
        text=profile_rets,
        textposition="outside"
    ))

    fig_compare.add_trace(go.Bar(
        name="סיכון %",
        x=profile_names,
        y=profile_risks,
        marker_color=["#993C1D" if n == profile else "#FCA5A5" for n in profile_names],
        text=profile_risks,
        textposition="outside"
    ))

    fig_compare.update_layout(
        barmode="group",
        title=dict(text=f"השוואה — הפרופיל שלך ({profile}) מסומן בכהה", x=0.95, xanchor="right"),
        height=400
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.divider()

    # --- סימולציית עתיד ---
    st.subheader(f" סימולציית עתיד — הכסף שלך עוד {horizon} שנים📅")

    years = list(range(horizon + 1))

    if horizon == 1:
        milestones = [1]
    elif horizon == 3:
        milestones = [1, 2, 3]
    elif horizon == 10:
        milestones = [2, 4, 6, 8, 10]
    else:
        milestones = [5, 10, 15, 20]

    fig_future = go.Figure()

    for name, w in all_profiles.items():
        r, _, _ = calc_metrics(w, returns, risks)
        fv = future_value(amount, r, horizon)
        is_mine = name == profile

        fig_future.add_trace(go.Scatter(
            x=years,
            y=fv,
            mode="lines",
            name=name,
            line=dict(
                color=future_colors[name],
                width=4 if is_mine else 1.5,
                dash="solid" if is_mine else "dot"
            )
        ))

        if is_mine:
            milestones_no_last = [m for m in milestones if m != horizon]
            milestone_y = [future_value(amount, r, y)[-1] for y in milestones_no_last]

            fig_future.add_trace(go.Scatter(
                x=milestones_no_last, y=milestone_y,
                mode="markers+text",
                marker=dict(size=12, color=future_colors[name], symbol="circle"),
                text=[f"₪{v:,.0f}" for v in milestone_y],
                textposition="top center",
                textfont=dict(size=10, color=future_colors[name]),
                showlegend=False
            ))


            final_value = future_value(amount, r, horizon)[-1]

            fig_future.add_trace(go.Scatter(
                x=[horizon],
                y=[final_value],
                mode="markers+text",
                marker=dict(
                    size=22,
                    color="#FFD700",
                    symbol="star",
                    line=dict(color=future_colors[name], width=2)
                ),
                text=[f"⭐ ₪{final_value:,.0f}"],
                textposition="top center",
                textfont=dict(size=12, color=future_colors[name]),
                name="הסכום הצפוי שלך",
            ))

    fig_future.update_layout(
        title=dict(text=f"₪{amount:,} עוד {horizon} שנים — הפרופיל שלך ({profile}) מודגש", x=0.95, xanchor="right"),
        xaxis_title="שנים",
        yaxis_title="שווי (₪)",
        height=450,
        yaxis=dict(tickformat=",.0f"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig_future, use_container_width=True)

    final_value = future_value(amount, port_return, horizon)[-1]
    st.success(f"לפי הפרופיל שלך ({profile}), ₪{amount:,} יהפכו ל-₪{final_value:,.0f} עוד {horizon} שנים!")

    st.divider()

 # --- המלצה בשפה אנושית ---
    st.subheader(" ההמלצה שלנו💡")
    recommendations = {
        "שמרני": f"נראה שאת מישהי שמעדיפה שקט נפשי על פני סיכון — וזה בסדר גמור! 🟢 התוצאות שלך מבוססות בעיקר על אג\"ח ממשלתי, שמספק יציבות ושומר על הכסף שלך. אל תצפה להתעשרות מהירה, אבל לפחות תישן טוב בלילה. התשואה השנתית הצפויה היא {port_return*100:.1f}%, עם רמת סיכון נמוכה.",
        "מתון": f"את במקום מצוין — לא שמרנית מדי ולא אגרסיבית מדי! 🟡 התוצאות שלך משלב יציבות של אג\"ח עם פוטנציאל צמיחה של S&P 500. זו הדרך החכמה לצמוח לאט ובטוח לאורך זמן. התשואה השנתית הצפויה היא {port_return*100:.1f}% — צמיחה יציבה בלי הפתעות.",
        "מאוזן": f"את מבינה שכדי להרוויח צריך לקחת קצת סיכון — וזה גישה חכמה! 🟠 החלק הגדול ב-S&P 500 נותן לך חשיפה לשוק האמריקאי, שהיסטורית צמח יפה לאורך זמן. התשואה השנתית הצפויה היא {port_return*100:.1f}% — פוטנציאל טוב לטווח הבינוני.",
        "אגרסיבי": f"את משקיעה בגדול! 🔴 הפרופיל שלך כולל חשיפה גבוהה ל-NASDAQ ו-S&P 500 — שני מדדים שיכולים לתת תשואות גבוהות לאורך זמן, אבל גם לרדת בחדות בשנים רעות. התשואה השנתית הצפויה היא {port_return*100:.1f}%. חשוב: ודאי שיש לך אורך נשימה של לפחות 7 שנים ושהכסף הזה לא דחוף לך.",
    }
    st.info(recommendations[profile])
    st.caption("⚠️ הנתונים מבוססים על ממוצעים היסטוריים בלבד. כלי זה אינו מהווה ייעוץ פיננסי מוסדר. לפני כל השקעה — מומלץ להתייעץ עם איש מקצוע.")