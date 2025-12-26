#!/usr/bin/env python3
"""
HTML Sanitizer - Strip non-essential HTML to save tokens
"""

from bs4 import BeautifulSoup
import re

def sanitize_html(html_content):
    """Clean HTML for token efficiency while preserving strain data"""
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove non-essential elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'meta', 'link']):
        element.decompose()
    
    # Remove ads and tracking
    for element in soup.find_all(class_=re.compile(r'(ad|banner|tracking|cookie|social)')):
        element.decompose()
    
    # Keep only strain-relevant content
    strain_keywords = ['thc', 'cbd', 'flowering', 'height', 'yield', 'genetics', 'sativa', 'indica', 'effects', 'flavors']
    
    # Extract main content areas
    main_content = soup.find('main') or soup.find('body') or soup
    
    # Clean text while preserving structure
    cleaned_text = main_content.get_text(separator=' ', strip=True)
    
    # Remove excessive whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Limit to 3000 characters for token efficiency
    if len(cleaned_text) > 3000:
        cleaned_text = cleaned_text[:3000] + "..."
    
    return cleaned_text

def extract_tables(html_content):
    """Extract technical specification tables"""
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = []
    
    for table in soup.find_all('table'):
        table_data = []
        for row in table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if cells:
                table_data.append(cells)
        if table_data:
            tables.append(table_data)
    
    return tables