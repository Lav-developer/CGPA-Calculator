import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.title("CGPA Calculator")

# Custom CSS for background and table
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        color: #fff;
    }
    .stApp {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
    }
    .stTable {
        background-color: #232526 !important;
    }
    .st-bb {
        color: #fff !important;
    }
    .stDataFrame thead tr th {
        text-align: center !important;
        color: #00ffd0 !important;
        font-size: 18px !important;
        background: #232526 !important;
    }
    .stDataFrame tbody tr td {
        text-align: center !important;
        font-size: 16px !important;
        background: #232526 !important;
        color: #fff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center; color: #00ffd0;'>✨ CGPA Calculator ✨</h2>", unsafe_allow_html=True)

grade_map = {
    'O': 10,
    'A+': 9,
    'A': 8,
    'B+': 7,
    'B': 6,
    'C': 5,
    'P': 4,
    'F': 0
}

num_subjects = st.number_input("Enter number of subjects:", min_value=1, step=1)
grades_list = []
credits_list = []

if num_subjects:
    st.write("#### 📚 Enter details for each subject:")
    for i in range(int(num_subjects)):
        cols = st.columns(2)
        grade = cols[0].selectbox(
            f"Letter grade for subject {i+1}",
            options=list(grade_map.keys()),
            key=f"grade_{i}"
        )
        credits = cols[1].number_input(
            f"Credits for subject {i+1}",
            min_value=1,
            step=1,
            key=f"credits_{i}"
        )
        grades_list.append(grade)
        credits_list.append(credits)

    if st.button("🚀 Calculate CGPA"):
        total_points = 0
        total_credits = 0
        table_data = []

        for i in range(int(num_subjects)):
            grade = grades_list[i]
            credits = credits_list[i]
            grade_point = grade_map.get(grade, 0)
            points = grade_point * credits
            total_points += points
            total_credits += credits
            table_data.append({
                "Subject": i+1,
                "Grade": grade,
                "Credits": credits,
                "Grade Point": grade_point,
                "Points": points
            })

        df = pd.DataFrame(table_data)

        # Style the table
        styled_df = df.style.set_properties(**{
            'text-align': 'center',
            'background-color': '#232526',
            'color': '#fff',
            'font-size': '16px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center'), ('color', '#00ffd0'), ('font-size', '18px'), ('background', '#232526')]}
        ])

        st.write("### 🧮 Calculation Details")
        st.table(styled_df)

        st.write("---")
        st.markdown(f"<span style='color:#00ffd0;font-size:18px;'><b>Total Credits:</b></span> <b>{total_credits}</b>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#00ffd0;font-size:18px;'><b>Total Points:</b></span> <b>{total_points}</b>", unsafe_allow_html=True)

        if total_credits == 0:
            st.warning("No credits entered.")
        else:
            cgpa = total_points / total_credits
            st.markdown(f"<h3 style='color:#00ffd0;'>🎯 Your CGPA is: <span style='color:#fff;'>{cgpa:.2f}</span></h3>", unsafe_allow_html=True)
            st.progress(min(cgpa/10, 1.0), text=f"CGPA Progress: {cgpa:.2f}/10")

            st.info(
                "#### ℹ️ How CGPA is calculated:\n"
                "- CGPA = Total Points / Total Credits\n"
                "- Total Points = Sum of (Grade Point × Credits) for all subjects\n"
                "- Total Credits = Sum of credits for all subjects\n"
                "- Grade Point is assigned based on the letter grade you entered."
            )

            def show_modal(message, icon):
                modal_code = f"""
                <div id="customModal" style="
                    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                    background: rgba(0,0,0,0.7); backdrop-filter: blur(3px);
                    display: flex; align-items: center; justify-content: center; z-index: 99999;">
                  <div style="
                    background: #18191a; color: #fff; padding: 60px 60px 32px 60px; border-radius: 32px;
                    min-width: 400px; max-width: 95vw; text-align: center; position: relative;
                    box-shadow: 0 12px 48px #000c; border: 3px solid #00ffd0;">
                    <span id="closeModal" style="
                      position: absolute; top: 18px; right: 32px; font-size: 40px; cursor: pointer; color: #00ffd0;">&times;</span>
                    <div style="font-size: 60px; margin-bottom: 18px;">{icon}</div>
                    <div style="font-size: 32px; margin: 24px 0 32px 0; font-weight: bold;">{message}</div>
                    <div id="countdown" style="font-size: 22px; color: #00ffd0; margin-top: 18px;">
                        This will close in <span id='timer'>10</span> seconds.
                    </div>
                  </div>
                </div>
                <script>
                let seconds = 10;
                let timer = setInterval(function() {{
                    seconds -= 1;
                    document.getElementById('timer').innerText = seconds;
                    if (seconds <= 0) {{
                        clearInterval(timer);
                        document.getElementById('customModal').style.display = 'none';
                    }}
                }}, 1000);
                document.getElementById('closeModal').onclick = function() {{
                    document.getElementById('customModal').style.display = 'none';
                    clearInterval(timer);
                }};
                </script>
                """
                components.html(modal_code, height=500)

            # Motivational or congratulatory message
            if cgpa < 7.5:
                show_modal("💡 Keep pushing! Your CGPA can improve with consistent effort. Stay motivated and keep learning! 🚀", "💡")
            elif cgpa >= 9.0:
                show_modal("🏆 Congratulations! You have achieved an outstanding CGPA. Keep up the excellent work! 🌟", "🏆")
            else:
                show_modal("👏 Good job! Your CGPA is above average. Keep striving for excellence!", "👏")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;color:#888;'>Made with ❤️ by <b>Lav Kush</b></div>", unsafe_allow_html=True)

        def show_alert(message):
            components.html(f"<script>alert('{message}');</script>", height=0)

        if cgpa < 7.5:
            show_alert("💡 Keep pushing! Your CGPA can improve with consistent effort. Stay motivated and keep learning! 🚀")
        elif cgpa >= 9.0:
            show_alert("🏆 Congratulations! You have achieved an outstanding CGPA. Keep up the excellent work! 🌟")
        else:
            show_alert("👏 Good job! Your CGPA is above average. Keep striving for excellence!🏆")
