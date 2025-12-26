#!/usr/bin/env python3
"""
Medallion Processor - Implements Bronze-to-Gold transformation
Part of the Tri-Model AI Synthesis architecture
"""

import json
import pandas as pd
from typing import Dict, Any, Optional

class MedallionProcessor:
    """
    Processes Bronze (raw) data into Gold (standardized) format
    Implements the Data Architect's Manifesto for scientific auditability
    """
    
    def __init__(self):
        self.conversion_rules = {
            'height': {
                'Short': 80,
                'Medium': 120, 
                'Tall': 180,
                'feet_to_cm': 30.48
            },
            'flowering': {
                'weeks_to_days': 7
            }
        }
    
    def process_bronze_to_gold(self, bronze_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform Bronze (source truth) to Gold (standardized) data
        
        Args:
            bronze_data: Raw extracted data with verbatim strings
            
        Returns:
            Dict containing both bronze and gold layers
        """
        
        gold_data = {
            'height_cm_min': self._extract_height_range(bronze_data.get('height_raw')),
            'height_cm_max': self._extract_height_range(bronze_data.get('height_raw'), max_val=True),
            'flowering_days_min': self._extract_flowering_range(bronze_data.get('flowering_time_raw')),
            'flowering_days_max': self._extract_flowering_range(bronze_data.get('flowering_time_raw'), max_val=True),
            'thc_percentage_min': self._extract_percentage_range(bronze_data.get('thc_content_raw')),
            'thc_percentage_max': self._extract_percentage_range(bronze_data.get('thc_content_raw'), max_val=True),
            'cbd_percentage_min': self._extract_percentage_range(bronze_data.get('cbd_content_raw')),
            'cbd_percentage_max': self._extract_percentage_range(bronze_data.get('cbd_content_raw'), max_val=True),
            'sativa_percentage': self._extract_genetics(bronze_data.get('genetics_raw'), 'sativa'),
            'indica_percentage': self._extract_genetics(bronze_data.get('genetics_raw'), 'indica'),
            'effects_standardized': self._standardize_effects(bronze_data.get('effects_raw')),
            'flavors_standardized': self._standardize_flavors(bronze_data.get('flavors_raw')),
            'confidence_score': self._calculate_confidence(bronze_data)
        }
        
        return {
            'bronze': bronze_data,
            'gold': gold_data
        }
    
    def _extract_height_range(self, height_raw: Optional[str], max_val: bool = False) -> Optional[float]:
        """Extract height in cm from raw text"""
        if not height_raw:
            return None
            
        # Handle descriptive heights
        height_lower = height_raw.lower()
        if 'short' in height_lower:
            return self.conversion_rules['height']['Short']
        elif 'medium' in height_lower:
            return self.conversion_rules['height']['Medium']
        elif 'tall' in height_lower:
            return self.conversion_rules['height']['Tall']
        
        # Extract numeric ranges (e.g., "80-120cm", "3-4 feet")
        import re
        
        # Look for cm measurements
        cm_pattern = r'(\d+(?:\.\d+)?)\s*-?\s*(\d+(?:\.\d+)?)?\s*cm'
        cm_match = re.search(cm_pattern, height_raw, re.IGNORECASE)
        if cm_match:
            min_val = float(cm_match.group(1))
            max_val_found = cm_match.group(2)
            if max_val_found and max_val:
                return float(max_val_found)
            return min_val
        
        # Look for feet measurements
        feet_pattern = r'(\d+(?:\.\d+)?)\s*-?\s*(\d+(?:\.\d+)?)?\s*(?:feet|ft)'
        feet_match = re.search(feet_pattern, height_raw, re.IGNORECASE)
        if feet_match:
            min_val = float(feet_match.group(1)) * self.conversion_rules['height']['feet_to_cm']
            max_val_found = feet_match.group(2)
            if max_val_found and max_val:
                return float(max_val_found) * self.conversion_rules['height']['feet_to_cm']
            return min_val
        
        return None
    
    def _extract_flowering_range(self, flowering_raw: Optional[str], max_val: bool = False) -> Optional[int]:
        """Extract flowering time in days from raw text"""
        if not flowering_raw:
            return None
            
        import re
        
        # Look for week patterns (e.g., "8-9 weeks", "7 wks")
        week_pattern = r'(\d+)\s*-?\s*(\d+)?\s*(?:weeks?|wks?)'
        week_match = re.search(week_pattern, flowering_raw, re.IGNORECASE)
        if week_match:
            min_weeks = int(week_match.group(1))
            max_weeks = week_match.group(2)
            if max_weeks and max_val:
                return int(max_weeks) * self.conversion_rules['flowering']['weeks_to_days']
            return min_weeks * self.conversion_rules['flowering']['weeks_to_days']
        
        # Look for day patterns
        day_pattern = r'(\d+)\s*-?\s*(\d+)?\s*days?'
        day_match = re.search(day_pattern, flowering_raw, re.IGNORECASE)
        if day_match:
            min_days = int(day_match.group(1))
            max_days = day_match.group(2)
            if max_days and max_val:
                return int(max_days)
            return min_days
        
        return None
    
    def _extract_percentage_range(self, percentage_raw: Optional[str], max_val: bool = False) -> Optional[float]:
        """Extract percentage values from raw text"""
        if not percentage_raw:
            return None
            
        import re
        
        # Look for percentage patterns (e.g., "15-20%", "18%", "up to 25%")
        percent_pattern = r'(\d+(?:\.\d+)?)\s*-?\s*(\d+(?:\.\d+)?)?\s*%'
        percent_match = re.search(percent_pattern, percentage_raw)
        if percent_match:
            min_val = float(percent_match.group(1))
            max_val_found = percent_match.group(2)
            if max_val_found and max_val:
                return float(max_val_found)
            return min_val
        
        return None
    
    def _extract_genetics(self, genetics_raw: Optional[str], genetics_type: str) -> Optional[int]:
        """Extract sativa/indica percentages from raw genetics text"""
        if not genetics_raw:
            return None
            
        import re
        
        # Look for percentage patterns (e.g., "60% Sativa", "40% Indica")
        pattern = rf'(\d+)\s*%\s*{genetics_type}'
        match = re.search(pattern, genetics_raw, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        return None
    
    def _standardize_effects(self, effects_raw: Optional[str]) -> Optional[str]:
        """Standardize effect descriptions"""
        if not effects_raw:
            return None
            
        # Common effect mappings
        effect_mappings = {
            'relaxing': 'Relaxed',
            'euphoric': 'Euphoric', 
            'uplifting': 'Uplifted',
            'energetic': 'Energetic',
            'creative': 'Creative',
            'focused': 'Focused',
            'happy': 'Happy',
            'sleepy': 'Sleepy'
        }
        
        standardized_effects = []
        effects_lower = effects_raw.lower()
        
        for raw_effect, standard_effect in effect_mappings.items():
            if raw_effect in effects_lower:
                standardized_effects.append(standard_effect)
        
        return ', '.join(standardized_effects) if standardized_effects else None
    
    def _standardize_flavors(self, flavors_raw: Optional[str]) -> Optional[str]:
        """Standardize flavor descriptions"""
        if not flavors_raw:
            return None
            
        # Common flavor mappings
        flavor_mappings = {
            'citrus': 'Citrus',
            'lemon': 'Lemon',
            'orange': 'Orange',
            'berry': 'Berry',
            'sweet': 'Sweet',
            'earthy': 'Earthy',
            'pine': 'Pine',
            'diesel': 'Diesel',
            'skunk': 'Skunk',
            'fruity': 'Fruity'
        }
        
        standardized_flavors = []
        flavors_lower = flavors_raw.lower()
        
        for raw_flavor, standard_flavor in flavor_mappings.items():
            if raw_flavor in flavors_lower:
                standardized_flavors.append(standard_flavor)
        
        return ', '.join(standardized_flavors) if standardized_flavors else None
    
    def _calculate_confidence(self, bronze_data: Dict[str, Any]) -> int:
        """Calculate confidence score (1-5) based on data completeness"""
        
        # Weight different fields by importance
        field_weights = {
            'height_raw': 2,
            'flowering_time_raw': 3,
            'thc_content_raw': 3,
            'cbd_content_raw': 2,
            'genetics_raw': 2,
            'effects_raw': 1,
            'flavors_raw': 1
        }
        
        total_possible = sum(field_weights.values())
        actual_score = 0
        
        for field, weight in field_weights.items():
            if bronze_data.get(field) and len(str(bronze_data[field]).strip()) > 2:
                actual_score += weight
        
        # Convert to 1-5 scale
        percentage = (actual_score / total_possible) * 100
        
        if percentage >= 90:
            return 5
        elif percentage >= 70:
            return 4
        elif percentage >= 50:
            return 3
        elif percentage >= 30:
            return 2
        else:
            return 1

def main():
    """Example usage of the Medallion Processor"""
    
    processor = MedallionProcessor()
    
    # Example Bronze data
    sample_bronze = {
        'height_raw': '80-120cm indoor, up to 180cm outdoor',
        'flowering_time_raw': '8-9 weeks',
        'thc_content_raw': '18-22% THC',
        'cbd_content_raw': 'Low CBD <1%',
        'genetics_raw': '60% Sativa, 40% Indica hybrid',
        'effects_raw': 'Euphoric, uplifting, creative energy',
        'flavors_raw': 'Citrus, lemon, sweet berry notes'
    }
    
    # Process to Gold
    result = processor.process_bronze_to_gold(sample_bronze)
    
    print("=== MEDALLION PROCESSOR EXAMPLE ===")
    print("\nBRONZE (Source Truth):")
    for key, value in result['bronze'].items():
        print(f"  {key}: {value}")
    
    print("\nGOLD (Standardized):")
    for key, value in result['gold'].items():
        if value is not None:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()