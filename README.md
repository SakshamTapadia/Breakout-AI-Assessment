# BreakoutAI Data Extraction App  

## Project Description  
The **BreakoutAI Data Extraction App** is a Streamlit-based application designed for extracting and processing data from various sources like Google Sheets or CSV files. Using advanced search and machine learning models, the app allows users to:  
- Fetch information via Google SERP API and GROQ AI API.  
- Extract targeted features based on custom prompts and search queries.  
- Update processed data directly to Google Sheets or download it as a CSV file.  

This app is ideal for automating data extraction, contextual information analysis, and streamlining workflows for researchers, analysts, and developers.  

---

## Setup Instructions  

### 1. Clone the Repository  
```bash  
git clone <repository-url>  
cd <repository-folder>  
```  

### 2. Install Dependencies  
First, ensure you have Python 3.8+ installed on your system. Then, run:  
```bash  
pip install -r requirements.txt  
```  

### 3. Configure API Keys and Service Account  
- **SERP API Key**: Register at [SERP API](https://serpapi.com/) and copy your API key.  
- **GROQ API Key**: Sign up for GROQ AI at [GROQ](https://groq.com/) and generate an API key.  
- **Google Service Account File**:  
  - Create a service account in Google Cloud Console with access to Google Sheets.  
  - Download the service account JSON file and place it in the project directory.  
  - Update the `SERVICE_ACCOUNT_FILE` path in the code.  

---

## Usage Guide  

### 1. Launch the Application  
Run the following command to start the Streamlit app:  
```bash  
streamlit run app.py  
```  

### 2. Load Data  
- **Upload CSV File**: Use the file uploader to load your dataset.  
- **Connect Google Sheets**: Enter the URL of your Google Sheet to fetch and process its data.  

### 3. Configure Search Queries  
- Select the column to search from the loaded data.  
- Enter a custom prompt using `{column_name}` as a placeholder.  

Example:  
```  
Extract detailed information about {column_name}, including its headquarters, CEO, and contact details.  
```  

### 4. Process Data  
- Click on **Search and Extract** to begin processing data.  
- Progress is displayed in real-time, and results appear in a table format once processing is complete.  

### 5. Save Results  
- **Download CSV**: Use the download button to save the results.  
- **Update Google Sheets**: Choose to update the results directly into your connected Google Sheet.  

---

## API Keys and Environment Variables  

### Required API Keys  
1. **SERP API Key**: Enter the key in the `SERP_API_KEY` variable.  
2. **GROQ API Key**: Enter the key in the `GROQ_API_KEY` variable.  

### Service Account JSON  
Ensure the path to the service account JSON file is updated in the `SERVICE_ACCOUNT_FILE` variable:  
```python  
SERVICE_ACCOUNT_FILE = "path_to_your_service_account.json"  
```  

---

## Optional Features  

### 1. Real-Time Updates to Google Sheets  
- Automatically update your processed data back to the Google Sheet with minimal effort.  

### 2. Customizable Prompts  
- Leverage highly customizable search prompts to tailor the information retrieval process to specific use cases.  

### 3. Flexible Data Sources  
- Easily switch between using CSV files or Google Sheets as the data source.  

---

## Notes  
- Ensure your service account has appropriate permissions for the connected Google Sheets.  
- Use unique and descriptive prompts to improve the quality of extracted data.  
- For troubleshooting, use the logs in Streamlit for detailed error messages.  

---

Feel free to contribute to this project by raising issues or submitting pull requests.  

***
Loom Video : https://www.loom.com/share/20ccfcb42280426ab560ed5295200f4b?sid=2ee8465c-4016-4a16-afdb-84cd7192e93a

**Happy Extracting!**  

---
