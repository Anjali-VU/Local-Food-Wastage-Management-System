import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
page_title="Local Food Wastage Management System",
page_icon="🍲",
layout="wide"
)
conn = sqlite3.connect("food_wastage.db")
st.sidebar.title("🍲 Navigation")

page = st.sidebar.radio(
"Select Page",
[
"📊 Dashboard",
"🏢 Providers",
"🙋 Receivers",
"🍽 Food Listings",
"📦 Claims",
"📊 EDA & Charts",
"📈 SQL Analysis",
"✏️ CRUD Operations"
]
)
# ---------------- Dashboard ----------------
if page == "📊 Dashboard":

    st.markdown("""
    <div style='background:linear-gradient(90deg,#1E3C72,#2A5298);
    padding:25px;border-radius:15px;color:white;text-align:center'>
    <h1>🍲 Local Food Wastage Management System</h1>
    <h4>Connecting Food Providers with Receivers</h4>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- KPI Cards ----------------

    total_providers = pd.read_sql(
        "SELECT COUNT(*) AS count FROM providers", conn).iloc[0,0]

    total_receivers = pd.read_sql(
        "SELECT COUNT(*) AS count FROM receivers", conn).iloc[0,0]

    total_food = pd.read_sql(
        "SELECT COUNT(*) AS count FROM food_listings", conn).iloc[0,0]

    total_claims = pd.read_sql(
        "SELECT COUNT(*) AS count FROM claims", conn).iloc[0,0]

    total_quantity = pd.read_sql(
        "SELECT SUM(Quantity) FROM food_listings", conn).iloc[0,0]

    completed = pd.read_sql(
        "SELECT COUNT(*) FROM claims WHERE Status='Completed'", conn).iloc[0,0]

    pending = pd.read_sql(
        "SELECT COUNT(*) FROM claims WHERE Status='Pending'", conn).iloc[0,0]

    cancelled = pd.read_sql(
        "SELECT COUNT(*) FROM claims WHERE Status='Cancelled'", conn).iloc[0,0]

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("🏢 Providers", total_providers)
    c2.metric("🙋 Receivers", total_receivers)
    c3.metric("🍽 Food Listings", total_food)
    c4.metric("📦 Claims", total_claims)

    c5,c6,c7,c8 = st.columns(4)

    c5.metric("🍲 Food Quantity", total_quantity)
    c6.metric("✅ Completed", completed)
    c7.metric("⏳ Pending", pending)
    c8.metric("❌ Cancelled", cancelled)

    st.markdown("---")

    # ---------------- First Row ----------------
    col1,col2 = st.columns(2)

    status_df = pd.read_sql("""
    SELECT Status,
    COUNT(*) Total
    FROM claims
    GROUP BY Status
    """,conn)

    fig1 = px.pie(
        status_df,
        names="Status",
        values="Total",
        hole=.5,
        title="Claim Status"
    )

    with col1:
        st.plotly_chart(fig1,use_container_width=True)

    food_df = pd.read_sql("""
    SELECT Food_Type,
    COUNT(*) Total
    FROM food_listings
    GROUP BY Food_Type
    """,conn)

    fig2 = px.bar(
        food_df,
        x="Food_Type",
        y="Total",
        color="Food_Type",
        title="Food Type Distribution"
    )

    with col2:
        st.plotly_chart(fig2,use_container_width=True)

    # ---------------- Second Row ----------------

    col3,col4 = st.columns(2)

    meal_df = pd.read_sql("""
    SELECT Meal_Type,
    COUNT(*) Total
    FROM food_listings
    GROUP BY Meal_Type
    """,conn)

    fig3 = px.bar(
        meal_df,
        x="Meal_Type",
        y="Total",
        color="Meal_Type",
        title="Meal Type Distribution"
    )

    with col3:
        st.plotly_chart(fig3,use_container_width=True)

    city_df = pd.read_sql("""
    SELECT Location,
    SUM(Quantity) Total_Quantity
    FROM food_listings
    GROUP BY Location
    ORDER BY Total_Quantity DESC
    LIMIT 10
    """,conn)

    fig4 = px.bar(
        city_df,
        x="Location",
        y="Total_Quantity",
        color="Total_Quantity",
        title="Top 10 Cities by Food Quantity"
    )

    with col4:
        st.plotly_chart(fig4,use_container_width=True)

    # ---------------- Third Row ----------------

    col5,col6 = st.columns(2)

    provider_df = pd.read_sql("""
    SELECT Provider_Type,
    SUM(Quantity) Total
    FROM food_listings
    GROUP BY Provider_Type
    """,conn)

    fig5 = px.pie(
        provider_df,
        names="Provider_Type",
        values="Total",
        hole=.5,
        title="Provider Contribution"
    )

    with col5:
        st.plotly_chart(fig5,use_container_width=True)

    top_provider = pd.read_sql("""
    SELECT p.Name,
    SUM(f.Quantity) Total_Donated
    FROM providers p
    JOIN food_listings f
    ON p.Provider_ID=f.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Donated DESC
    LIMIT 10
    """,conn)

    fig6 = px.bar(
        top_provider,
        x="Name",
        y="Total_Donated",
        color="Total_Donated",
        title="Top 10 Providers"
    )

    with col6:
        st.plotly_chart(fig6,use_container_width=True)

    st.markdown("### 🏆 Top 10 Providers by Donation")
    st.dataframe(top_provider,use_container_width=True)
    # ---------------- Providers ----------------
# ---------------- Providers ----------------

# ---------------- Providers ----------------
elif page == "🏢 Providers":

    st.title("🏢 Food Providers")
    st.markdown("Manage and view all registered food providers.")

    providers = pd.read_sql("SELECT * FROM providers", conn)

    # ================= KPI Cards =================
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏢 Total Providers",
        len(providers)
    )

    col2.metric(
        "🏙 Cities",
        providers["City"].nunique()
    )

    col3.metric(
        "🍽 Provider Types",
        providers["Type"].nunique()
    )

    st.markdown("---")

    # ================= Provider Table =================
    st.subheader("📋 Provider Details")

    st.dataframe(
        providers,
        use_container_width=True
    )

    st.markdown("---")

    # ================= Charts =================
    col1, col2 = st.columns(2)

    # Chart 1
    with col1:

        provider_type = (
            providers["Type"]
            .value_counts()
            .reset_index()
        )

        provider_type.columns = [
            "Provider Type",
            "Count"
        ]

        fig1 = px.bar(
            provider_type,
            x="Provider Type",
            y="Count",
            color="Provider Type",
            title="Providers by Type"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # Chart 2
    with col2:

        city_provider = (
            providers["City"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        city_provider.columns = [
            "City",
            "Providers"
        ]

        fig2 = px.bar(
            city_provider,
            x="City",
            y="Providers",
            color="Providers",
            title="Top 10 Cities by Providers"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )
        # ---------------- Receivers ----------------
elif page == "🙋 Receivers":

    st.title("🙋 Food Receivers")
    st.markdown("View and manage registered food receivers.")

    receivers = pd.read_sql("SELECT * FROM receivers", conn)

    # ================= KPI Cards =================
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🙋 Total Receivers",
        len(receivers)
    )

    col2.metric(
        "🏙 Cities",
        receivers["City"].nunique()
    )

    col3.metric(
        "📍 Locations",
        receivers["City"].count()
    )

    st.markdown("---")

    # ================= Receiver Table =================
    st.subheader("📋 Receiver Details")

    st.dataframe(
        receivers,
        use_container_width=True
    )

    st.markdown("---")

    # ================= Charts =================
    col1, col2 = st.columns(2)

    # Chart 1 - Receivers by City
    with col1:

        city_df = (
            receivers["City"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        city_df.columns = [
            "City",
            "Receivers"
        ]

        fig1 = px.bar(
            city_df,
            x="City",
            y="Receivers",
            color="Receivers",
            title="Top 10 Cities by Receivers"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # Chart 2 - Receiver Distribution
    with col2:

        pie_df = (
            receivers["City"]
            .value_counts()
            .head(8)
            .reset_index()
        )

        pie_df.columns = [
            "City",
            "Receivers"
        ]

        fig2 = px.pie(
            pie_df,
            names="City",
            values="Receivers",
            title="Receiver Distribution by City",
            hole=0.45
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )
        # ---------------- Food Listings ----------------
elif page == "🍽 Food Listings":

    st.title("🍽 Food Listings")
    st.markdown("Browse available food donations using filters.")

    food = pd.read_sql("SELECT * FROM food_listings", conn)

    # ================= Filters =================
    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.selectbox(
            "📍 Select City",
            ["All"] + sorted(food["Location"].unique())
        )

    with col2:
        food_type = st.selectbox(
            "🥗 Select Food Type",
            ["All"] + sorted(food["Food_Type"].unique())
        )

    with col3:
        meal_type = st.selectbox(
            "🍽 Select Meal Type",
            ["All"] + sorted(food["Meal_Type"].unique())
        )

    filtered = food.copy()

    if city != "All":
        filtered = filtered[filtered["Location"] == city]

    if food_type != "All":
        filtered = filtered[filtered["Food_Type"] == food_type]

    if meal_type != "All":
        filtered = filtered[filtered["Meal_Type"] == meal_type]

    # ================= KPI Cards =================
    total_quantity = filtered["Quantity"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🍲 Listings", len(filtered))
    col2.metric("📦 Food Units", int(total_quantity))
    col3.metric("🥗 Food Types", filtered["Food_Type"].nunique())
    col4.metric("🍽 Meal Types", filtered["Meal_Type"].nunique())

    st.markdown("---")

    # ================= Data Table =================
    st.subheader("📋 Available Food Listings")

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.markdown("---")

    # ================= Charts Row 1 =================
    col1, col2 = st.columns(2)

    with col1:

        food_chart = (
            filtered["Food_Type"]
            .value_counts()
            .reset_index()
        )

        food_chart.columns = ["Food Type", "Count"]

        fig1 = px.bar(
            food_chart,
            x="Food Type",
            y="Count",
            color="Food Type",
            title="Food Type Distribution"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        meal_chart = (
            filtered["Meal_Type"]
            .value_counts()
            .reset_index()
        )

        meal_chart.columns = ["Meal Type", "Count"]

        fig2 = px.pie(
            meal_chart,
            names="Meal Type",
            values="Count",
            hole=0.45,
            title="Meal Type Distribution"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ================= Charts Row 2 =================
    col3, col4 = st.columns(2)

    with col3:

        city_chart = (
            filtered.groupby("Location")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig3 = px.bar(
            city_chart,
            x="Location",
            y="Quantity",
            color="Quantity",
            title="Top Cities by Food Quantity"
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col4:

        provider_chart = (
            filtered.groupby("Provider_Type")["Quantity"]
            .sum()
            .reset_index()
        )

        fig4 = px.pie(
            provider_chart,
            names="Provider_Type",
            values="Quantity",
            hole=0.45,
            title="Provider Type Contribution"
        )

        st.plotly_chart(fig4, use_container_width=True)
        # ---------------- Claims ----------------
elif page == "📦 Claims":

    st.title("📦 Food Claims")
    st.markdown("View and analyze all food claims.")

    claims = pd.read_sql("SELECT * FROM claims", conn)

    # ================= KPI Cards =================
    total_claims = len(claims)
    completed = len(claims[claims["Status"] == "Completed"])
    pending = len(claims[claims["Status"] == "Pending"])
    cancelled = len(claims[claims["Status"] == "Cancelled"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total Claims", total_claims)
    col2.metric("✅ Completed", completed)
    col3.metric("⏳ Pending", pending)
    col4.metric("❌ Cancelled", cancelled)

    st.markdown("---")

    # ================= Claims Table =================
    st.subheader("📋 Claims Details")

    st.dataframe(
        claims,
        use_container_width=True
    )

    st.markdown("---")

    # ================= Charts =================
    col1, col2 = st.columns(2)

    with col1:

        status_df = (
            claims["Status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Count"
        ]

        fig1 = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.45,
            title="Claim Status Distribution"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        receiver_df = (
            claims.groupby("Receiver_ID")
            .size()
            .reset_index(name="Total Claims")
            .sort_values(
                by="Total Claims",
                ascending=False
            )
            .head(10)
        )

        fig2 = px.bar(
            receiver_df,
            x="Receiver_ID",
            y="Total Claims",
            color="Total Claims",
            title="Top 10 Receivers by Claims"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ================= Second Row =================
    col3, col4 = st.columns(2)

    with col3:

        food_df = (
            claims.groupby("Food_ID")
            .size()
            .reset_index(name="Claims")
            .sort_values(
                by="Claims",
                ascending=False
            )
            .head(10)
        )

        fig3 = px.bar(
            food_df,
            x="Food_ID",
            y="Claims",
            color="Claims",
            title="Most Claimed Food Items"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col4:

        fig4 = px.histogram(
            claims,
            x="Status",
            color="Status",
            title="Claim Status Histogram"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )
        # ---------------- EDA & Charts ----------------
elif page == "📊 EDA & Charts":

    st.title("📊 Exploratory Data Analysis (EDA) & Charts")
    st.markdown("Interactive visual analysis of the Local Food Wastage Management System.")

    food = pd.read_sql("SELECT * FROM food_listings", conn)
    providers = pd.read_sql("SELECT * FROM providers", conn)
    receivers = pd.read_sql("SELECT * FROM receivers", conn)
    claims = pd.read_sql("SELECT * FROM claims", conn)

    # ---------------- Row 1 ----------------
    col1, col2 = st.columns(2)

    with col1:
        food_type = food.groupby("Food_Type").size().reset_index(name="Count")
        fig = px.bar(
            food_type,
            x="Food_Type",
            y="Count",
            color="Food_Type",
            title="Food Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            claims,
            names="Status",
            title="Claim Status Distribution",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Row 2 ----------------
    col3, col4 = st.columns(2)

    with col3:
        meal = food.groupby("Meal_Type").size().reset_index(name="Count")
        fig = px.bar(
            meal,
            x="Meal_Type",
            y="Count",
            color="Meal_Type",
            title="Meal Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        city = food.groupby("Location")["Quantity"].sum().reset_index()
        city = city.sort_values("Quantity", ascending=False).head(10)

        fig = px.bar(
            city,
            x="Location",
            y="Quantity",
            color="Quantity",
            title="Top 10 Cities by Food Quantity"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Row 3 ----------------
    col5, col6 = st.columns(2)

    with col5:
        provider = food.groupby("Provider_Type")["Quantity"].sum().reset_index()

        fig = px.pie(
            provider,
            names="Provider_Type",
            values="Quantity",
            title="Provider Contribution",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        top_provider = food.groupby("Provider_ID")["Quantity"].sum().reset_index()
        top_provider = top_provider.sort_values("Quantity", ascending=False).head(10)

        fig = px.bar(
            top_provider,
            x="Provider_ID",
            y="Quantity",
            color="Quantity",
            title="Top Providers by Quantity"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Row 4 ----------------
    col7, col8 = st.columns(2)

    with col7:
        expiry = food.groupby("Expiry_Date").size().reset_index(name="Listings")

        fig = px.line(
            expiry,
            x="Expiry_Date",
            y="Listings",
            title="Food Expiry Trend"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col8:
        food_name = food.groupby("Food_Name").size().reset_index(name="Count")
        food_name = food_name.sort_values("Count", ascending=False).head(10)

        fig = px.bar(
            food_name,
            x="Food_Name",
            y="Count",
            color="Count",
            title="Top 10 Food Items"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Row 5 ----------------
    col9, col10 = st.columns(2)

    with col9:
        quantity = food.groupby("Food_Type")["Quantity"].sum().reset_index()

        fig = px.bar(
            quantity,
            x="Food_Type",
            y="Quantity",
            color="Quantity",
            title="Quantity by Food Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col10:
        receiver_city = receivers.groupby("City").size().reset_index(name="Receivers")
        receiver_city = receiver_city.sort_values("Receivers", ascending=False).head(10)

        fig = px.bar(
            receiver_city,
            x="City",
            y="Receivers",
            color="Receivers",
            title="Top Receiver Cities"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- Row 6 ----------------
    col11, col12 = st.columns(2)

    with col11:
        provider_city = providers.groupby("City").size().reset_index(name="Providers")
        provider_city = provider_city.sort_values("Providers", ascending=False).head(10)

        fig = px.bar(
            provider_city,
            x="City",
            y="Providers",
            color="Providers",
            title="Top Provider Cities"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col12:
        fig = px.histogram(
            food,
            x="Quantity",
            nbins=20,
            title="Food Quantity Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Providers", len(providers))
    c2.metric("Receivers", len(receivers))
    c3.metric("Food Listings", len(food))
    c4.metric("Claims", len(claims))
    # ---------------- SQL Analysis ----------------
elif page == "📈 SQL Analysis":

    st.title("📈 SQL Analysis")

    query = st.selectbox(
        "Select SQL Query",
        [
            "1. Food Providers in Each City",
            "2. Food Receivers in Each City",
            "3. Provider Type Contribution",
            "4. Provider Contact Details",
            "5. Receivers Who Claimed the Most Food",
            "6. Total Quantity of Food Available",
            "7. City with Highest Food Listings",
            "8. Most Common Food Types",
            "9. Claims for Each Food Item",
            "10. Provider with Highest Successful Claims",
            "11. Claim Status Percentage",
            "12. Average Quantity Claimed Per Receiver",
            "13. Most Claimed Meal Type",
            "14. Quantity Donated by Each Provider",
            "15. Top Cities by Food Quantity"
        ]
    )   
    if query == "1. Food Providers in Each City":
     st.subheader("Query 1: Food Providers in Each City")
     sql = """
     SELECT City,
           COUNT(*) AS Total_Providers
     FROM providers
     GROUP BY City
     ORDER BY Total_Providers DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df,
        x="City",
        y="Total_Providers",
        color="Total_Providers",
        text="Total_Providers",
        title="Food Providers in Each City"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: This chart shows the cities having the highest number of registered food providers.")
    elif query == "2. Food Receivers in Each City":

     st.subheader("Query 2: Food Receivers in Each City")

     sql = """
     SELECT City,
           COUNT(*) AS Total_Receivers
     FROM receivers
     GROUP BY City
     ORDER BY Total_Receivers DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df,
        x="City",
        y="Total_Receivers",
        color="Total_Receivers",
        text="Total_Receivers",
        title="Food Receivers in Each City"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: This chart shows which cities have the highest number of registered food receivers.")
    elif query == "3. Provider Type Contribution":

     st.subheader("Query 3: Provider Type Contribution")

     sql = """
     SELECT Provider_Type,
           SUM(Quantity) AS Total_Quantity
     FROM food_listings
     GROUP BY Provider_Type
     ORDER BY Total_Quantity DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.pie(
        df,
        names="Provider_Type",
        values="Total_Quantity",
        hole=0.5,
        title="Food Contribution by Provider Type"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: This chart identifies which provider type contributes the most food.")
    elif query == "4. Provider Contact Details":

     st.subheader("Query 4: Provider Contact Details")

     city = st.selectbox(
        "Select City",
        pd.read_sql(
            "SELECT DISTINCT City FROM providers ORDER BY City",
            conn
        )["City"]
     )

     sql = f"""
     SELECT Name,
           Contact
     FROM providers
     WHERE City='{city}';
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df,
        x="Name",
        y=[1]*len(df),
        title=f"Providers in {city}"
     )

     fig.update_layout(
        showlegend=False,
        yaxis_visible=False,
        title_x=0.5
     )

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Displays all food providers and their contact details for the selected city.")
    elif query == "5. Receivers Who Claimed the Most Food":

     st.subheader("Query 5: Receivers Who Claimed the Most Food")

     sql = """
     SELECT
        r.Name,
        COUNT(c.Claim_ID) AS Total_Claims
     FROM receivers r
     JOIN claims c
     ON r.Receiver_ID=c.Receiver_ID
     GROUP BY r.Name
     ORDER BY Total_Claims DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df.head(10),
        x="Name",
        y="Total_Claims",
        color="Total_Claims",
        text="Total_Claims",
        title="Top 10 Receivers by Claims"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: This chart identifies the receivers who have claimed the highest amount of food.")
    elif query == "6. Total Quantity of Food Available":

     st.subheader("Query 6: Total Quantity of Food Available")

     sql = """
     SELECT SUM(Quantity) AS Total_Food_Quantity
     FROM food_listings;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.pie(
        values=df["Total_Food_Quantity"],
        names=["Available Food"],
        hole=0.5,
        title="Total Food Quantity Available"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Shows the total quantity of food currently available in the system.")
    elif query == "7. City with Highest Food Listings":

     st.subheader("Query 7: City with Highest Food Listings")

     sql = """
     SELECT
        Location,
        COUNT(*) AS Total_Listings
     FROM food_listings
     GROUP BY Location
     ORDER BY Total_Listings DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df,
        x="Location",
        y="Total_Listings",
        color="Total_Listings",
        text="Total_Listings",
        title="Food Listings by City"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Highlights the cities with the highest number of food listings.")
    elif query == "8. Most Common Food Types":

     st.subheader("Query 8: Most Common Food Types")

     sql = """
     SELECT
        Food_Type,
        COUNT(*) AS Total_Items
     FROM food_listings
     GROUP BY Food_Type
     ORDER BY Total_Items DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.pie(
        df,
        names="Food_Type",
        values="Total_Items",
        hole=0.5,
        title="Food Type Distribution"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Displays the distribution of different food types available.")
    elif query == "9. Claims for Each Food Item":

     st.subheader("Query 9: Claims for Each Food Item")

     sql = """
     SELECT
        f.Food_Name,
        COUNT(c.Claim_ID) AS Total_Claims
     FROM food_listings f
     LEFT JOIN claims c
     ON f.Food_ID = c.Food_ID
     GROUP BY f.Food_Name
     ORDER BY Total_Claims DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df.head(10),
        x="Food_Name",
        y="Total_Claims",
        color="Total_Claims",
        text="Total_Claims",
        title="Top 10 Claimed Food Items"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Shows which food items receive the highest number of claims.")
    elif query == "10. Provider with Highest Successful Claims":

     st.subheader("Query 10: Provider with Highest Successful Claims")

     sql = """
     SELECT
        p.Name,
        COUNT(c.Claim_ID) AS Successful_Claims
     FROM providers p
     JOIN food_listings f
        ON p.Provider_ID = f.Provider_ID
     JOIN claims c
        ON f.Food_ID = c.Food_ID
     WHERE c.Status='Completed'
     GROUP BY p.Name
     ORDER BY Successful_Claims DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df.head(10),
        x="Name",
        y="Successful_Claims",
        color="Successful_Claims",
        text="Successful_Claims",
        title="Top Providers by Successful Claims"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Displays the providers whose donated food resulted in the highest number of completed claims.")
    elif query == "11. Claim Status Percentage":

     st.subheader("Query 11: Claim Status Percentage")

     sql = """
     SELECT
        Status,
        COUNT(*) AS Total_Claims,
        ROUND(
            COUNT(*) * 100.0 /
            (SELECT COUNT(*) FROM claims), 2
        ) AS Percentage
     FROM claims
     GROUP BY Status;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.pie(
        df,
        names="Status",
        values="Percentage",
        hole=0.5,
        title="Claim Status Percentage"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Shows the percentage of completed, pending, and cancelled claims.")
    elif query == "12. Average Quantity Claimed Per Receiver":

     st.subheader("Query 12: Average Quantity Claimed Per Receiver")

     sql = """
     SELECT
        r.Name,
        ROUND(AVG(f.Quantity),2) AS Average_Quantity
     FROM receivers r
     JOIN claims c
        ON r.Receiver_ID = c.Receiver_ID
     JOIN food_listings f
        ON c.Food_ID = f.Food_ID
     GROUP BY r.Name
     ORDER BY Average_Quantity DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df.head(10),
        x="Name",
        y="Average_Quantity",
        color="Average_Quantity",
        text="Average_Quantity",
        title="Average Quantity Claimed Per Receiver"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Displays receivers who claim the highest average quantity of food.")
    elif query == "13. Most Claimed Meal Type":

     st.subheader("Query 13: Most Claimed Meal Type")

     sql = """
     SELECT
        Meal_Type,
        COUNT(*) AS Total_Claims
     FROM food_listings f
     JOIN claims c
        ON f.Food_ID = c.Food_ID
     GROUP BY Meal_Type
     ORDER BY Total_Claims DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df,
        x="Meal_Type",
        y="Total_Claims",
        color="Meal_Type",
        text="Total_Claims",
        title="Most Claimed Meal Type"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Shows which meal type is claimed most frequently.")
    elif query == "14. Quantity Donated by Each Provider":

     st.subheader("Query 14: Quantity Donated by Each Provider")

     sql = """
     SELECT
        p.Name,
        SUM(f.Quantity) AS Total_Donated
     FROM providers p
     JOIN food_listings f
        ON p.Provider_ID = f.Provider_ID
     GROUP BY p.Name
     ORDER BY Total_Donated DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df.head(10),
        x="Name",
        y="Total_Donated",
        color="Total_Donated",
        text="Total_Donated",
        title="Top 10 Providers by Donation Quantity"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Highlights the providers contributing the largest quantity of food.")
    elif query == "15. Top Cities by Food Quantity":

     st.subheader("Query 15: Top Cities by Food Quantity")

     sql = """
     SELECT
        Location,
        SUM(Quantity) AS Total_Quantity
     FROM food_listings
     GROUP BY Location
     ORDER BY Total_Quantity DESC;
     """

     df = pd.read_sql(sql, conn)

     st.write("### Output")
     st.dataframe(df, use_container_width=True)

     fig = px.bar(
        df,
        x="Location",
        y="Total_Quantity",
        color="Total_Quantity",
        text="Total_Quantity",
        title="Top Cities by Food Quantity"
     )

     fig.update_layout(title_x=0.5)

     st.plotly_chart(fig, use_container_width=True)

     st.info("Insight: Displays the cities with the highest total quantity of donated food.")
 # ---------------- CRUD Operations ----------------
elif page == "✏️ CRUD Operations":

    st.title("✏️ CRUD Operations")

    operation = st.selectbox(
        "Select Operation",
        ["Create", "Read", "Update", "Delete"]
    )

    # READ
    if operation == "Read":

        st.subheader("📋 View Food Listings")

        df = pd.read_sql(
            "SELECT * FROM food_listings",
            conn
        )

        st.dataframe(df, use_container_width=True)


    # CREATE
    elif operation == "Create":

        st.subheader("➕ Add New Food Listing")

        food_id = st.number_input("Food ID", step=1)
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", step=1)
        expiry_date = st.text_input("Expiry Date (YYYY-MM-DD)")
        provider_id = st.number_input("Provider ID", step=1)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("Location")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")

        if st.button("Add Record"):

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO food_listings
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    food_id,
                    food_name,
                    quantity,
                    expiry_date,
                    provider_id,
                    provider_type,
                    location,
                    food_type,
                    meal_type
                )
            )

            conn.commit()

            st.success("✅ Record Added Successfully!")


    # UPDATE
    elif operation == "Update":

        st.subheader("✏️ Update Quantity")

        food_id = st.number_input(
            "Enter Food ID",
            step=1,
            key="update_id"
        )

        new_quantity = st.number_input(
            "New Quantity",
            step=1,
            key="update_quantity"
        )

        if st.button("Update Record"):

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE food_listings
                SET Quantity = ?
                WHERE Food_ID = ?
                """,
                (new_quantity, food_id)
            )

            conn.commit()

            st.success("✅ Record Updated Successfully!")


    # DELETE
    elif operation == "Delete":

        st.subheader("🗑 Delete Food Listing")

        food_id = st.number_input(
            "Enter Food ID to Delete",
            step=1,
            key="delete_id"
        )

        if st.button("Delete Record"):

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM food_listings
                WHERE Food_ID = ?
                """,
                (food_id,)
            )

            conn.commit()

            st.success("✅ Record Deleted Successfully!")