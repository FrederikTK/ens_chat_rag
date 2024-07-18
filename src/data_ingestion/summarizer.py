# src/data_ingestion/summarizer.py
from src.utils.llm_interface import call_llm_api
from config.config import get_llm_config
from src.utils.num_tokens import num_tokens_from_string

def summarize_text(text, llm_type="gpt3"):
    llm_config = get_llm_config(llm_type)
    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
    summary = call_llm_api(llm_config, {"content": prompt})
    return summary

def summarize_documents(documents, llm_type="gpt3"):
    summaries = []
    for doc in documents:
        summary = summarize_text(doc['content'], llm_type)
        summaries.append({
            "id": doc['id'],
            "url": doc['url'],
            "summary": summary,
            "original_content": doc['content']
        })
    return summaries

def summarize_urls(urls_data, llm_type="gpt3"):
    llm_config = get_llm_config(llm_type)
    summaries = []

    for data in urls_data:
        if 'content' in data and data['content']:
            try:
                summary_text = call_llm_api(llm_config, {"content": data['content']})
            except Exception as e:
                summary_text = f"Error processing data: {str(e)}"
        else:
            summary_text = "No content available to summarize."

        summaries.append({
            "id": data['id'],
            "url": data['url'],
            "summary": summary_text,
            "title": data['title'],
            "time_requested": data['time_requested'],
            "error": data.get('error', 'None'),
            "num_tokens_in": data.get('num_tokens', 0),
            "num_tokens_out": num_tokens_from_string(summary_text, "cl100k_base"),
            "estimated_input_cost_gpt4": data.get('num_tokens', 0) * 0.00001,
            "estimated_output_cost_gpt4": data.get('num_tokens', 0) * 0.00003,
            "estimated_input_cost_gpt3": data.get('num_tokens', 0) * 0.0000005,
            "estimated_output_cost_gpt3": data.get('num_tokens', 0) * 0.0000015,
            "used_model": llm_config['model']
        })
    
    return summaries
