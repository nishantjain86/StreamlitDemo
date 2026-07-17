import streamlit as st
import pandas as pd
import re

# Page setup and design
st.set_page_config(page_title="Demo", page_icon="💧", layout="centered")

# Set a fixed global goal for the fundraising drive
GOAL_USD = 10000.0

# Initialize global tracking metrics across page reloads
if "water_footprint" not in st.session_state:
    st.session_state.water_footprint = 0
if "total_donated" not in st.session_state:
    st.session_state.total_donated = 1340.0  # Starting mock simulation baseline seed
if "donation_count" not in st.session_state:
    st.session_state.donation_count = 42     # Number of previous simulated donations

# App Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "🌍 1. Global Water Crisis", 
    "📝 2. Your Water Quiz", 
    "💰 3. Make a Donation",
    "📊 4. Campaign Progress"
])

# ==============================================================================
# PAGE 1: GLOBAL WATER CRISIS INFORMATION
# ==============================================================================
if page == "🌍 1. Global Water Crisis":
    st.title("🌍 Global Water Scarcity")
    st.markdown("### The Reality of the Global Water Crisis")
    st.write(
        "Clean water is a basic human right, yet billions of people live without it. "
        "Developing regions, particularly across parts of Africa and Asia, face severe daily water stress."
    )
    
    # Visual Data Table of affected regions
    st.subheader("📊 Key Metrics by Region")
    data = {
        "Country / Region": ["South Africa (Cape)", "Somalia", "Yemen", "Chad"],
        "Main Cause": ["Infrastructure & Drought", "Severe Prolonged Drought", "Conflict & Lack of Sources", "Desertification"],
        "People Lacking Clean Water": ["Over 5 Million", "Approx. 60% of population", "Over 16 Million", "Approx. 55% of population"]
    }
    df = pd.DataFrame(data)
    st.table(df)

    st.markdown("### ✨ Why South Africa Needs Help")
    st.write(
        "While South Africa has highly developed cities, its rural provinces face massive water grid failures. "
        "Children often walk several kilometers a day to fetch muddy river water instead of sitting in school classrooms."
    )
    st.info("💡 Next Step: Click 'Your Water Quiz' in the sidebar to see how much water you use compared to these countries!")

# ==============================================================================
# PAGE 2: PERSONAL WATER CONSUMPTION QUIZ
# ==============================================================================
elif page == "📝 2. Your Water Quiz":
    st.title("📝 Your Personal Water Footprint")
    st.write("Answer these questions about your daily routine to see how many liters of water you consume.")

    # Quiz Inputs
    shower_time = st.slider("How long is your daily shower? (Minutes)", 0, 20, 15)
    flush_count = st.number_input("How many times do you flush the toilet per day?", min_value=0, max_value=20, value=5)
    tap_running = st.radio("Do you leave the tap running while brushing your teeth?", ["Yes", "No"])
    diet_type = st.selectbox("What does your primary diet look like? (Meat requires vastly more water to produce)", ["Meat Eater", "Vegetarian", "Vegan"])

    if st.button("📊 Calculate My Water Footprint"):
        # Math formulas approximating water consumption in liters
        shower_liters = shower_time * 9  
        flush_liters = flush_count * 6   
        brush_liters = 12 if tap_running == "Yes" else 1
        diet_liters = 4000 if diet_type == "Meat Eater" else (2500 if diet_type == "Vegetarian" else 1500)
        
        total_footprint = shower_liters + flush_liters + brush_liters + diet_liters
        st.session_state.water_footprint = total_footprint
        
        # Display results with educational context
        st.subheader("📋 Your Results:")
        st.metric(label="Your Daily Water Use", value=f"{total_footprint} Liters")
        st.warning(f"Comparison: You use {total_footprint} liters a day. An average person in rural South Africa survives on less than 20 liters.")
        st.success("Footprint saved! Proceed to the 'Make a Donation' page to bridge the gap.")

# ==============================================================================
# PAGE 3: DONATION GATEWAY (WITH MANDATORY CREDIT CARD DETAILS)
# ==============================================================================
elif page == "💰 3. Make a Donation":
    st.title("💰 Help Provide Clean Water")
    st.write("Turn your awareness into action. Please enter your donation and payment information below.")
    
    if st.session_state.water_footprint > 0:
        st.info(f"Your calculated daily footprint: **{st.session_state.water_footprint} Liters**.")

    # 1. Donation Details
    st.subheader("💳 1. Donation Amount")
    col1, col2 = st.columns(2)
    with col1:
        donor_name = st.text_input("Cardholder Full Name:")
    with col2:
        country_target = st.selectbox("Select Country to Help:", ["South Africa", "Somalia", "Chad"])
        
    donation_amount = st.number_input("Enter Donation Amount ($ USD):", min_value=1, max_value=1000, value=10)
    liters_bought = donation_amount * 50  
    st.caption(f"✨ This donation will provide roughly **{liters_bought} liters** of clean water.")

    st.markdown("---")

    # 2. Mandatory Credit Card Details Panel
    st.subheader("🔒 2. Secure Payment Details")
    card_number = st.text_input("Credit Card Number (16 Digits):", max_chars=16, help="Enter digits only without spaces")
    
    col3, col4 = st.columns(2)
    with col3:
        expiry_date = st.text_input("Expiration Date (MM/YY):", max_chars=5, placeholder="10/28")
    with col4:
        cvv_code = st.text_input("Security Code (CVV):", type="password", max_chars=3, help="3 digits on back of card")

    # 3. Processing and Field Validation Logic
    if st.button("🚀 Process Secure Donation"):
        clean_card = re.sub(r"\s+", "", card_number)
        clean_expiry = re.sub(r"\s+", "", expiry_date)
        
        if not donor_name:
            st.error("❌ Mandatory Field Missing: Please enter the Cardholder Full Name.")
        elif not re.match(r"^\d{16}$", clean_card):
            st.error("❌ Invalid Card: Credit Card number must be exactly 16 numeric digits.")
        elif not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", clean_expiry):
            st.error("❌ Invalid Expiry: Expiration date must follow the exact MM/YY format (e.g., 04/27).")
        elif not re.match(r"^\d{3}$", cvv_code):
            st.error("❌ Invalid CVV: Security code must be a 3-digit numeric value.")
        else:
            # Add transaction balance to live pool trackers
            st.session_state.total_donated += float(donation_amount)
            st.session_state.donation_count += 1
            
            st.balloons()
            st.success(
                f"🎉 Thank you, {donor_name}! Your transaction of **${donation_amount:.2f}** was approved. "
                f"**{liters_bought} liters** of clean water are on the way to families in {country_target}! "
                f"Check 'Campaign Progress' to see our updated campaign targets."
            )

# ==============================================================================
# PAGE 4: LIVE CAMPAIGN PROGRESS & GOALS
# ==============================================================================
elif page == "📊 4. Campaign Progress":
    st.title("📊 Campaign Impact & Goals")
    st.write("Track the school community's global contribution progress in real-time.")

    # Calculations
    current_funds = st.session_state.total_donated
    distance_left = max(0.0, GOAL_USD - current_funds)
    funding_percentage = min(1.0, current_funds / GOAL_USD)
    total_liters_delivered = current_funds * 50

    # Layout Row: Financial Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total Funds Raised", value=f"${current_funds:,.2f}")
    with c2:
        st.metric(label="Remaining to Target", value=f"${distance_left:,.2f}")
    with c3:
        st.metric(label="Total Contributions", value=f"{st.session_state.donation_count} Donations")
    with c4:
        st.metric(label="Total Contributions", value=10000)

    # Progress Visualizer Bar
    st.subheader(r"🎯 Target Drive Progress")
    st.progress(funding_percentage)
    st.caption(f"**{funding_percentage * 100:.1f}%** of our **${GOAL_USD:,.2f}** school benchmark goal achieved!")

    # Cumulative Real World Translation Block
    st.markdown("---")
    st.subheader("📦 Transformed Community Resources")
    st.info(
        f"💧 Together, this funding pool maps directly to providing approximately "
        f"**{total_liters_delivered:,.0f} Liters** of purified distribution tank or borehole water "
        f"for infrastructure projects across South Africa and surrounding territories."
    )
