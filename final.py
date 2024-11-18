import pandas as pd
import requests
import streamlit as st
from serpapi import GoogleSearch
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define your API keys
SERP_API_KEY = os.getenv("SERP_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define service account file path
SERVICE_ACCOUNT_FILE = "D:\\BreakoutAI Assessment\\service_account.json"

# Google Sheets Authentication with error handling
def authenticate_google_sheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Authentication Error: {str(e)}")
        return None

def load_google_sheet(sheet_url):
    try:
        gc = authenticate_google_sheets()
        if gc is None:
            return None, None, None
        
        # Extract sheet key from URL
        if '/d/' in sheet_url:
            sheet_key = sheet_url.split('/d/')[1].split('/')[0]
        else:
            st.error("Invalid Google Sheet URL format")
            return None, None, None
        
        sheet = gc.open_by_key(sheet_key)
        worksheet = sheet.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data), gc, worksheet
    except Exception as e:
        st.error(f"Error loading sheet: {str(e)}")
        return None, None, None

def update_google_sheet(worksheet, results_df):
    try:
        # Convert DataFrame to list of lists
        data = [results_df.columns.values.tolist()]
        data.extend(results_df.values.tolist())
        
        # Clear the worksheet
        worksheet.clear()
        
        # Update the sheet with new data
        worksheet.update('A1', data)
        
        return True, "Google Sheet updated successfully!"
    except Exception as e:
        detailed_error = f"Error updating sheet: {str(e)}"
        st.error(detailed_error)
        return False, detailed_error

# Fetch search results from SERP API
def get_search_results(query, prompt, api_key, column_name):
    col_name = column_name
    try:
        # Try the original column_name format
        search_query = prompt.format(column_name=query)
    except KeyError:
        # If that fails, just replace whatever placeholder is there
        search_query = prompt.replace("{col_name}", query).replace("{column_name}", query)
    params = {
        "engine": "google",
        "q": search_query,
        "num": 100,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    text_content = ""
    if "knowledge_graph" in results:
        knowledge = results["knowledge_graph"]
        text_content += f"{knowledge.get('title', '')}\n"
        text_content += f"{knowledge.get('type', '')}\n"
        text_content += f"{knowledge.get('website', '')}\n"
        text_content += f"{knowledge.get('founded', '')}\n"
        text_content += f"{knowledge.get('headquarters', '')}\n"
        text_content += f"{knowledge.get('revenue', '')}\n"
        text_content += f"{knowledge.get('social', '')}\n"
        text_content += f"{knowledge.get('mobile', '')}\n"
        text_content += f"{knowledge.get('phone', '')}\n"
        text_content += f"{knowledge.get('ceo', '\b')}\n"
        text_content += f"{knowledge.get('email', '')}\n"
        text_content += f"{knowledge.get('contact email', '')}\n"
        text_content += f"{knowledge.get('address', '')}\n"
        text_content += f"{knowledge.get('contact', '')}\n"
        text_content += f"{knowledge.get('call', '')}\n"
        text_content += f"{knowledge.get('chat', '')}\n"
        text_content += f"{knowledge.get('connect', '')}\n"
        text_content += f"{knowledge.get('write', '')}\n"
        text_content += f"{knowledge.get('twitter', '')}\n"
        text_content += f"{knowledge.get('instagram', '')}\n"
        text_content += f"{knowledge.get('facebook', '')}\n"
    for result in results.get("organic_results", []):
        text_content += f"{result.get('title', 'N/A')} - {result.get('snippet', 'N/A')}\n"

    return text_content

# Fetch specific information using GROQ API
def ask_groq_api(question, company, context, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    You are an AI assistant specialized in extracting specific information from any data. 
    From the context and question provided, extract only the feature which is asked in the question.
    Respond only with the asked feature, without any verbosity. Clean and exact answers only.

    Question: {question}
    Company: {company}
    Context: {context}
    """
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an assistant that extracts specific information from context."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        feature = response_json['choices'][0]['message']['content'].strip()
        return feature
    else:
        return f"Error: {response.status_code}, {response.text}"

def authenticate_and_update(sheet_url, df2):
    gc2 = gspread.service_account(filename="D:\BreakoutAI Assessment\service_account.json")
    # Step 2: Open Google Sheet
    spreadsheet = gc2.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1  # Select the first worksheet
    set_with_dataframe(worksheet, df2)  # Upload the DataFrame
    st.success("Data uploaded successfully!")





# Streamlit UI
st.title("BreakoutAI Data Extraction App")

# Initialize session state for update control
if 'update_triggered' not in st.session_state:
    st.session_state.update_triggered = False
if 'results_df' not in st.session_state:
    st.session_state.results_df = None

# Step 1: File upload or Google Sheet connection
upload_choice = st.radio("Load the data:", ["Upload CSV File", "Enter Google Sheet URL"])
df, gc, worksheet = None, None, None

if upload_choice == "Upload CSV File":
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df)

elif upload_choice == "Enter Google Sheet URL":
    sheet_url = st.text_input("Enter the Google Sheet URL")
    if sheet_url:
        df, gc, worksheet = load_google_sheet(sheet_url)
        if df is not None:
            st.write("Data Preview:", df)

# Step 2: Column selection and query input

if df is not None:
    col_list = list(df.columns)
    col_list.insert(0, "Select")
    column_name = st.selectbox("Select the column to search in", col_list)

    if column_name != "Select":
        custom_prompt = st.text_input(
            "Enter your custom prompt (use {column_name} as placeholder):"
        )

        if st.button("Search and Extract") and custom_prompt:
            with st.spinner("Processing..."):
                data_collect = {}
                progress_bar = st.progress(0)
                total_items = len(df[column_name])
                
                for idx, entity in enumerate(df[column_name]):
                    search_results = get_search_results(entity, custom_prompt, SERP_API_KEY, column_name)
                    extracted_info = ask_groq_api(custom_prompt, entity, search_results, GROQ_API_KEY)
                    data_collect[entity] = extracted_info
                    progress_bar.progress((idx + 1) / total_items)

                # Step 3: Display results
                if data_collect:
                    results_df = pd.DataFrame(data_collect.items(), columns=[column_name, "Extracted Information"])
                    st.session_state.results_df = results_df  # Store in session state
                    st.write("Extracted Results:", results_df)

                    # Store results in session state for updating Google Sheet
                    st.session_state['df2'] = results_df

                    # Step 4: Download results
                    csv = results_df.to_csv(index=False)
                    st.download_button("Download Results", csv, "extracted_results.csv", "text/csv")
                    # Step 5: Update Google Sheet with text input
        permit_update = st.selectbox("Update sheet or not ", ["select", "yes", "no"])
        if permit_update.lower() == "yes":
            st.write("Updating Google Sheet...")
            authenticate_and_update(sheet_url, st.session_state['df2'])
