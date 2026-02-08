import os
import requests
import json
import streamlit as st

class AIAnalyst:
    def __init__(self, api_key=None, provider="Gemini"):
        self.provider = provider
        self.api_key = api_key
        # Gemini REST URL (using v1beta for latest features)
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    def generate_insight(self, context, task_type):
        """
        Generates insights based on data context and task type via REST API.
        This implementation avoids SDK dependency for maximum compatibility.
        """
        if not self.api_key:
             return "⚠️ API Key not found. Please provide a Google Gemini API key (Free Tier) in the settings."

        prompts = {
            "summary": f"Analyze this dataset summary and provide 3 top strategic insights. Dataset Stats: {context}",
            "story": f"Write a compelling data story (narrative) based on these findings. Explain the 'Why' behind the data. Context: {context}",
            "kpi": f"Suggest 5 Key Performance Indicators (KPIs) based on these columns and data types. Explain why each is important. Columns: {context}",
            "cleaning": f"Suggest data cleaning and validation rules for this dataset. Highlight potential quality issues. Data Info: {context}",
            "cohort": f"Recommend 3 customer/entity cohorts to analyze for better segmentation. Context: {context}"
        }
        
        prompt_text = prompts.get(task_type, f"Analyze this data: {context}")
        
        try:
            if self.provider == "Gemini":
                # Prepare REST payload
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt_text}]
                    }]
                }
                
                response = requests.post(f"{self.url}?key={self.api_key}", 
                                         headers=headers, 
                                         data=json.dumps(payload))
                
                if response.status_code == 200:
                    result = response.json()
                    # Extract text from response
                    try:
                        return result['candidates'][0]['content']['parts'][0]['text']
                    except (KeyError, IndexError):
                        return f"❌ Unexpected API Response Format: {result}"
                else:
                    return f"❌ AI API Error ({response.status_code}): {response.text}"
            
            return "Only Gemini provider is currently implemented via REST."
            
        except Exception as e:
            return f"❌ AI Insight Error: {str(e)}"

    def analyze_dataframe_head(self, df):
        """Converts head of DF to string context for AI."""
        return df.head(5).to_string() + f"\n\nColumns: {list(df.columns)}\nShape: {df.shape}"
