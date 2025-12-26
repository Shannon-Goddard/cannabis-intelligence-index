#!/usr/bin/env python3
"""
Data Extractor - HTML parsing and cannabis strain data extraction
Implements the Bronze layer extraction with zero interpretation
"""

from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple

class CannabisDataExtractor:
    """
    Extracts cannabis strain data from HTML content
    Follows the Bronze layer principle: zero interpretation, verbatim extraction
    """
    
    def __init__(self):
        self.extraction_stats = {
            'tables_found': 0,
            'descriptions_found': 0,
            'patterns_matched': 0,
            'images_processed': 0
        }
    
    def extract_strain_data(self, html_content: str, source_url: str) -> Dict:
        """
        Main extraction method that applies all extraction techniques
        Returns Bronze layer data (verbatim, zero interpretation)
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        extracted_data = {
            'source_url': source_url,
            'extraction_timestamp': self._get_timestamp(),
            'raw_data': {}
        }
        
        # Extract from structured tables (highest priority)
        table_data = self._extract_from_tables(soup)
        if table_data:
            extracted_data['raw_data'].update(table_data)
            self.extraction_stats['tables_found'] += 1
        
        # Extract from product descriptions
        desc_data = self._extract_from_descriptions(soup)
        if desc_data:
            extracted_data['raw_data'].update(desc_data)
            self.extraction_stats['descriptions_found'] += 1
        
        # Extract using pattern matching
        pattern_data = self._extract_with_patterns(soup)
        if pattern_data:
            extracted_data['raw_data'].update(pattern_data)
            self.extraction_stats['patterns_matched'] += 1
        
        # Extract from images and icons
        image_data = self._extract_from_images(soup)
        if image_data:
            extracted_data['raw_data'].update(image_data)
            self.extraction_stats['images_processed'] += 1
        
        # Extract metadata
        meta_data = self._extract_metadata(soup)
        if meta_data:
            extracted_data['raw_data'].update(meta_data)
        
        return extracted_data
    
    def _extract_from_tables(self, soup: BeautifulSoup) -> Dict:
        """
        Extract data from HTML tables - highest priority source
        Returns verbatim text as found in tables
        """
        table_data = {}
        
        # Find all tables
        tables = soup.find_all('table')
        
        for table_idx, table in enumerate(tables):
            # Look for specification tables
            if self._is_specification_table(table):
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        # Extract key-value pairs verbatim
                        key_cell = cells[0].get_text(strip=True)
                        value_cell = cells[1].get_text(strip=True)
                        
                        if key_cell and value_cell:
                            # Map to standard field names while preserving original text
                            field_name = self._map_table_field(key_cell)
                            if field_name:
                                table_data[f"{field_name}_raw"] = value_cell
                                table_data[f"{field_name}_source"] = f"Table {table_idx + 1}"
        
        return table_data
    
    def _extract_from_descriptions(self, soup: BeautifulSoup) -> Dict:
        """
        Extract data from product descriptions and text content
        Preserves original text formatting and context
        """
        desc_data = {}
        
        # Common selectors for product descriptions
        description_selectors = [
            '.product-description',
            '.strain-description',
            '.description',
            '.product-details',
            '.strain-info',
            '.product-content',
            '[class*=\"description\"]',
            '[class*=\"details\"]'
        ]
        
        all_descriptions = []
        
        for selector in description_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(separator=' ', strip=True)
                if text and len(text) > 20:  # Filter out very short text
                    all_descriptions.append(text)
        
        if all_descriptions:
            # Combine all descriptions while preserving original text
            full_description = ' '.join(all_descriptions)
            desc_data['description_raw'] = full_description
            desc_data['description_source'] = 'Product descriptions'
            
            # Extract specific mentions while preserving context
            desc_data.update(self._extract_contextual_mentions(full_description))
        
        return desc_data
    
    def _extract_with_patterns(self, soup: BeautifulSoup) -> Dict:
        """
        Use regex patterns to find specific data points
        Extracts verbatim matches with surrounding context
        """
        pattern_data = {}\n        page_text = soup.get_text(separator=' ', strip=True)\n        \n        # Define extraction patterns with context preservation\n        patterns = {\n            'thc_content': [\n                r'THC:?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'(?:THC|thc)\\s*(?:content|level|percentage)?:?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'([0-9]+(?:\\.[0-9]+)?(?:\\s*-\\s*[0-9]+(?:\\.[0-9]+)?)?\\s*%\\s*THC)'\n            ],\n            'cbd_content': [\n                r'CBD:?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'(?:CBD|cbd)\\s*(?:content|level|percentage)?:?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'([0-9]+(?:\\.[0-9]+)?(?:\\s*-\\s*[0-9]+(?:\\.[0-9]+)?)?\\s*%\\s*CBD)'\n            ],\n            'flowering_time': [\n                r'(?:flowering|flower)\\s+(?:time|period):?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'(?:blooms?|flowers?)\\s+(?:in|for|after)\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'([0-9]+(?:\\s*-\\s*[0-9]+)?\\s*(?:weeks?|days?|wks?)\\s*(?:flowering|flower|bloom))'\n            ],\n            'height': [\n                r'(?:height|tall|grows?):?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'(?:reaches|up to|grows to)\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'([0-9]+(?:\\s*-\\s*[0-9]+)?\\s*(?:cm|feet?|ft|inches?|in)\\s*(?:tall|high|height))'\n            ],\n            'yield': [\n                r'(?:yield|harvest|produces?):?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'(?:up to|around|approximately)\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'([0-9]+(?:\\s*-\\s*[0-9]+)?\\s*(?:g|grams?|oz|ounces?)\\s*(?:per|/|m2|plant))'\n            ],\n            'genetics': [\n                r'(?:genetics|lineage|cross|bred from):?\\s*([^\\n\\.]+?)(?:\\.|\\n|$)',\n                r'([0-9]+\\s*%\\s*(?:sativa|indica)(?:\\s*[^\\n\\.]*?)?)(?:\\.|\\n|$)',\n                r'(?:hybrid|cross)\\s+(?:of|between)\\s*([^\\n\\.]+?)(?:\\.|\\n|$)'\n            ]\n        }\n        \n        for field_name, field_patterns in patterns.items():\n            for pattern in field_patterns:\n                matches = re.finditer(pattern, page_text, re.IGNORECASE | re.MULTILINE)\n                for match in matches:\n                    if match.group(1).strip():\n                        # Store the verbatim match\n                        pattern_data[f\"{field_name}_raw\"] = match.group(1).strip()\n                        pattern_data[f\"{field_name}_source\"] = \"Pattern matching\"\n                        break  # Take first match for each field\n            \n            if f\"{field_name}_raw\" in pattern_data:\n                continue  # Move to next field if we found a match\n        \n        return pattern_data\n    \n    def _extract_from_images(self, soup: BeautifulSoup) -> Dict:\n        \"\"\"\n        Extract data from images, icons, and visual elements\n        Describes visual elements as text for Bronze layer\n        \"\"\"\n        image_data = {}\n        \n        # Look for rating icons/stars\n        rating_elements = soup.find_all(['img', 'span', 'div'], \n                                       class_=re.compile(r'(star|rating|score)', re.I))\n        \n        for element in rating_elements:\n            # Describe visual ratings\n            if element.name == 'img':\n                alt_text = element.get('alt', '')\n                src = element.get('src', '')\n                if 'star' in alt_text.lower() or 'rating' in alt_text.lower():\n                    image_data['rating_visual_raw'] = f\"[Image: {alt_text}]\"\n                    image_data['rating_visual_source'] = \"Image alt text\"\n            else:\n                # Count visual elements like star spans\n                stars = element.find_all(class_=re.compile(r'star', re.I))\n                if stars:\n                    image_data['rating_visual_raw'] = f\"[Visual: {len(stars)} star elements]\"\n                    image_data['rating_visual_source'] = \"Visual elements\"\n        \n        # Look for difficulty/complexity indicators\n        difficulty_elements = soup.find_all(class_=re.compile(r'(difficulty|easy|hard|beginner)', re.I))\n        for element in difficulty_elements:\n            text = element.get_text(strip=True)\n            if text:\n                image_data['difficulty_raw'] = text\n                image_data['difficulty_source'] = \"Visual indicator\"\n                break\n        \n        return image_data\n    \n    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:\n        \"\"\"\n        Extract metadata from HTML head and structured data\n        \"\"\"\n        meta_data = {}\n        \n        # Extract from meta tags\n        meta_description = soup.find('meta', attrs={'name': 'description'})\n        if meta_description:\n            content = meta_description.get('content', '')\n            if content:\n                meta_data['meta_description_raw'] = content\n                meta_data['meta_description_source'] = \"HTML meta tag\"\n        \n        # Extract from title tag\n        title_tag = soup.find('title')\n        if title_tag:\n            title_text = title_tag.get_text(strip=True)\n            if title_text:\n                meta_data['page_title_raw'] = title_text\n                meta_data['page_title_source'] = \"HTML title tag\"\n        \n        # Look for JSON-LD structured data\n        json_ld_scripts = soup.find_all('script', type='application/ld+json')\n        for script in json_ld_scripts:\n            try:\n                import json\n                structured_data = json.loads(script.string)\n                if isinstance(structured_data, dict):\n                    # Extract relevant product information\n                    if 'name' in structured_data:\n                        meta_data['structured_name_raw'] = structured_data['name']\n                        meta_data['structured_name_source'] = \"JSON-LD structured data\"\n                    if 'description' in structured_data:\n                        meta_data['structured_description_raw'] = structured_data['description']\n                        meta_data['structured_description_source'] = \"JSON-LD structured data\"\n            except (json.JSONDecodeError, AttributeError):\n                continue\n        \n        return meta_data\n    \n    def _is_specification_table(self, table) -> bool:\n        \"\"\"\n        Determine if a table contains strain specifications\n        \"\"\"\n        table_text = table.get_text().lower()\n        spec_keywords = ['thc', 'cbd', 'flowering', 'height', 'yield', 'genetics', 'sativa', 'indica']\n        \n        keyword_count = sum(1 for keyword in spec_keywords if keyword in table_text)\n        return keyword_count >= 2  # At least 2 cannabis-related keywords\n    \n    def _map_table_field(self, key_text: str) -> Optional[str]:\n        \"\"\"\n        Map table header text to standard field names\n        \"\"\"\n        key_lower = key_text.lower().strip()\n        \n        field_mappings = {\n            'thc': ['thc', 'thc content', 'thc level', 'thc %', 'thc percentage'],\n            'cbd': ['cbd', 'cbd content', 'cbd level', 'cbd %', 'cbd percentage'],\n            'flowering_time': ['flowering time', 'flowering period', 'flower time', 'bloom time', 'flowering'],\n            'height': ['height', 'plant height', 'size', 'grows to', 'tall'],\n            'yield': ['yield', 'harvest', 'production', 'output'],\n            'genetics': ['genetics', 'genetic background', 'lineage', 'breeding', 'cross'],\n            'effects': ['effects', 'effect', 'high', 'buzz'],\n            'flavors': ['flavor', 'flavour', 'taste', 'aroma', 'smell']\n        }\n        \n        for field_name, keywords in field_mappings.items():\n            if any(keyword in key_lower for keyword in keywords):\n                return field_name\n        \n        return None\n    \n    def _extract_contextual_mentions(self, text: str) -> Dict:\n        \"\"\"\n        Extract mentions of strain characteristics with surrounding context\n        \"\"\"\n        contextual_data = {}\n        \n        # Extract sentences containing key terms\n        sentences = re.split(r'[.!?]+', text)\n        \n        for sentence in sentences:\n            sentence = sentence.strip()\n            if not sentence:\n                continue\n            \n            sentence_lower = sentence.lower()\n            \n            # Look for effect mentions\n            effect_keywords = ['relaxing', 'euphoric', 'uplifting', 'energetic', 'creative', 'focused', 'happy', 'sleepy']\n            if any(keyword in sentence_lower for keyword in effect_keywords):\n                if 'effects_context_raw' not in contextual_data:\n                    contextual_data['effects_context_raw'] = sentence\n                    contextual_data['effects_context_source'] = \"Description context\"\n            \n            # Look for flavor mentions\n            flavor_keywords = ['citrus', 'lemon', 'berry', 'sweet', 'earthy', 'pine', 'diesel', 'fruity']\n            if any(keyword in sentence_lower for keyword in flavor_keywords):\n                if 'flavors_context_raw' not in contextual_data:\n                    contextual_data['flavors_context_raw'] = sentence\n                    contextual_data['flavors_context_source'] = \"Description context\"\n            \n            # Look for growing information\n            growing_keywords = ['indoor', 'outdoor', 'hydro', 'soil', 'climate', 'temperature']\n            if any(keyword in sentence_lower for keyword in growing_keywords):\n                if 'growing_context_raw' not in contextual_data:\n                    contextual_data['growing_context_raw'] = sentence\n                    contextual_data['growing_context_source'] = \"Description context\"\n        \n        return contextual_data\n    \n    def _get_timestamp(self) -> str:\n        \"\"\"\n        Get current timestamp for extraction tracking\n        \"\"\"\n        from datetime import datetime\n        return datetime.utcnow().isoformat() + 'Z'\n    \n    def get_extraction_stats(self) -> Dict:\n        \"\"\"\n        Return statistics about the extraction process\n        \"\"\"\n        return self.extraction_stats.copy()\n\ndef main():\n    \"\"\"Example usage of the Cannabis Data Extractor\"\"\"\n    \n    extractor = CannabisDataExtractor()\n    \n    # Example HTML content (simplified)\n    sample_html = \"\"\"\n    <html>\n    <head>\n        <title>Blue Dream Cannabis Seeds - Premium Genetics</title>\n        <meta name=\"description\" content=\"Blue Dream is a sativa-dominant hybrid with 18-24% THC\">\n    </head>\n    <body>\n        <div class=\"product-description\">\n            <p>Blue Dream is a legendary sativa-dominant hybrid with uplifting and euphoric effects. \n               This strain produces citrus and berry flavors with sweet undertones.</p>\n        </div>\n        <table class=\"specifications\">\n            <tr><th>THC Content</th><td>18-24%</td></tr>\n            <tr><th>CBD Content</th><td>0.1-0.2%</td></tr>\n            <tr><th>Flowering Time</th><td>9-10 weeks</td></tr>\n            <tr><th>Height</th><td>120-180cm</td></tr>\n        </table>\n    </body>\n    </html>\n    \"\"\"\n    \n    # Extract data\n    extracted_data = extractor.extract_strain_data(sample_html, \"https://example.com/blue-dream\")\n    \n    print(\"=== CANNABIS DATA EXTRACTOR EXAMPLE ===\")\n    print(f\"Source URL: {extracted_data['source_url']}\")\n    print(f\"Extraction Time: {extracted_data['extraction_timestamp']}\")\n    print(\"\\nExtracted Raw Data:\")\n    \n    for key, value in extracted_data['raw_data'].items():\n        print(f\"  {key}: {value}\")\n    \n    # Print extraction statistics\n    stats = extractor.get_extraction_stats()\n    print(f\"\\nExtraction Statistics:\")\n    for stat_name, count in stats.items():\n        print(f\"  {stat_name}: {count}\")\n\nif __name__ == \"__main__\":\n    main()