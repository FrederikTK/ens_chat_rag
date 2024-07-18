from utils.save_summary import save_summary
from src.data_ingestion.summarizer import summarize_urls

def process_urls(llm_type, urls_data):
    summaries = summarize_urls(urls_data, llm_type)
    
    for summary_meta in summaries:
        save_summary(summary_meta, summary_meta["id"])
        print(f"Saved summary for URL {summary_meta['id']} to {summary_meta['id']}.json")

    print(f"Completed processing of all URLs.")
