import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


# LLM (Model)
llm = ChatGroq(groq_api_key=st.secrets["GROQ_API_KEY"], model="llama3-8b-8192")
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()

# Page Configuration
st.set_page_config(
    page_title="Sales Agent - Powered by Groq",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
    body {
        background-color: #a810d6;
        font-family: 'Arial', Comic Sans MS;
    }
    .main-title {
        color: #531CB3;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        color: #944BBB;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 40px;
    }
    .about-app {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        color: #531CB3;
    }
    .form-header {
        color: #944BBB;
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .company-insights {
        color: #070eba;
        font-size: 1.2em;
        background: #f1f1f1;
        padding: 15px;
        border-radius: 5px;
    }
    .footer {
        text-align: center;
        font-size: 0.8em;
        color: #6c757d;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout with Columns
left_col, right_col = st.columns([1, 3])  # Adjust the column width ratio

# About the App Section
with left_col:
    st.markdown("<div class='about-app'><h3>About the App</h3>", unsafe_allow_html=True)
    st.markdown(
        "This is to help sales assistant agent prototype to help sales reps gain insights into prospective accounts, competitors, and company strategy.",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Main Section in Right Column
with right_col:
    # Page Header
    st.markdown("<div class='main-title'>Sales Agent</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>Sales Agent leveraging on AI to craft winning sales strategies. Powered by Groq.</div>",
        unsafe_allow_html=True,
    )

    # Form Header
    st.markdown("<div class='form-header'>Enter Company Information</div>", unsafe_allow_html=True)

    # Data collection/inputs
    with st.form("company_info", clear_on_submit=True):
        product_name = st.text_input("Product Name (What product are you selling?)")
        company_url = st.text_input("Company URL (The URL of the company you are targeting)")
        product_category = st.text_input("Product Category (e.g., 'Clothing' or 'Shoes & Accessories')")
        competitors_url = st.text_input("Competitor's URL (e.g., https://usa.tommy.com)")
        value_proposition = st.text_input("Value Proposition (Summarize the product’s value)")
        target_customer = st.text_input("Target Customer (Name of the person you are trying to sell to)")
        file_upload = st.file_uploader("Upload Product Overview Document", type=["pdf", "docx"])

        company_insights = ""

        if st.form_submit_button("Generate Insights"):
            if product_name and company_url:
                with st.spinner("Generating insights... Please wait."):
                    try:
                        # Use search tool to retrieve company information
                        company_information = search.invoke(company_url)

                        if not company_information:
                            st.warning(
                                "Could not retrieve any information from the provided company URL. Please check the URL and try again."
                            )
                        else:
                            prompt = """
                            As a sales director of the marketing department, your role is to generate marketing strategies that will outsmart the competitors.
                            Below is the information to use as a guide:

                            - Company Info: {company_information}
                            - Product Name: {product_name}
                            - Competitor's URL: {competitors_url}
                            - Product Category: {product_category}
                            - Value Proposition: {value_proposition}
                            - Target Customer: {target_customer}

                            Provide actionable insights and strategies in bullet points.
                            """
                            prompt_template = ChatPromptTemplate.from_template(prompt)

                            # Chain execution to process the data
                            chain = prompt_template | llm | parser
                            company_insights = chain.invoke(
                                {
                                    "company_information": company_information,
                                    "product_name": product_name,
                                    "competitors_url": competitors_url,
                                    "product_category": product_category,
                                    "value_proposition": value_proposition,
                                    "target_customer": target_customer,
                                }
                            )

                            # Display the insights
                            st.markdown(
                                "<div class='form-header'>Generated Company Insights</div>",
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f"<div class='company-insights'>{company_insights}</div>",
                                unsafe_allow_html=True,
                            )
                    except Exception as e:
                        st.error(f"An error occurred while generating insights: {str(e)}")
            else:
                st.warning("Please fill in both the Product Name and Company URL fields.")

# Include Font Awesome CDN in your app
st.markdown(
    """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Footer with Font Awesome copyright icon
st.markdown(
    """
    <div class='footer'>
        <span><i class="fas fa-copyright"></i> 2024 Sales Agent - Powered by Groq and Streamlit</span>
    </div>
    """,
    unsafe_allow_html=True
)
