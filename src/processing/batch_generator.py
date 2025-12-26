#!/usr/bin/env python3
"""
Batch File Generator - Creates JSONL for Gemini Batch API
"""

import pandas as pd
import json
import requests
from html_sanitizer import sanitize_html
from master_system_prompt import MASTER_SYSTEM_PROMPT
import time
import os

def generate_batch_jsonl(csv_path, output_path, max_requests=None):
    """Generate JSONL file for Gemini Batch API processing"""
    
    print("=== BATCH FILE GENERATOR ===")
    
    # Load strain data
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} strains")
    
    if max_requests:
        df = df.head(max_requests)
        print(f"Limited to {max_requests} requests for testing")
    
    batch_requests = []
    processed = 0
    errors = 0
    
    for idx, (_, strain) in enumerate(df.iterrows()):
        try:
            strain_name = strain.get('strain_name_cleaned', f'strain_{idx}')
            source_url = strain.get('source_url', '')
            
            print(f"Processing {idx+1}/{len(df)}: {strain_name}")
            
            # Get HTML content
            html_content = fetch_html(source_url)
            if not html_content:
                print(f"  Failed to fetch HTML for {strain_name}")
                errors += 1
                continue
            
            # Sanitize HTML
            cleaned_html = sanitize_html(html_content)
            
            # Create batch request
            request_data = {
                "custom_id": f"strain_{idx}_{strain_name.replace(' ', '_')}",
                "method": "POST",
                "url": "/v1beta/models/gemini-2.5-flash:generateContent",
                "body": {
                    "contents": [{
                        "parts": [{
                            "text": f"{MASTER_SYSTEM_PROMPT}\n\nSTRAIN: {strain_name}\nURL: {source_url}\n\nHTML CONTENT:\n{cleaned_html}"
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0,
                        "maxOutputTokens": 1000
                    }
                }
            }
            
            batch_requests.append(request_data)
            processed += 1
            
            # Rate limiting for HTML fetching
            time.sleep(0.1)
            
        except Exception as e:
            print(f"  Error processing {strain_name}: {e}")
            errors += 1
    
    # Save JSONL file
    with open(output_path, 'w') as f:
        for request in batch_requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"\n=== BATCH FILE COMPLETE ===")
    print(f"Total requests: {len(batch_requests)}")
    print(f"Successfully processed: {processed}")
    print(f"Errors: {errors}")
    print(f"Output saved to: {output_path}")
    
    return output_path

def fetch_html(url):
    """Fetch HTML content from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"    HTML fetch error: {e}")
        return None

if __name__ == "__main__":
    # Test with first 10 strains
    csv_path = "../data/Cannabis_Database_Word_Method_Cleaned.csv"
    output_path = "../data/batch_requests.jsonl"
    
    generate_batch_jsonl(csv_path, output_path, max_requests=10)