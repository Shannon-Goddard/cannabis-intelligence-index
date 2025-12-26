#!/usr/bin/env python3
"""
Outlier Detection - Quality validation for cannabis strain data
Identifies impossible values and potential AI hallucinations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class CannabisOutlierDetector:
    """
    Detects outliers and impossible values in cannabis strain data
    Implements scientific validation rules for botanical accuracy
    """
    
    def __init__(self):
        # Define realistic ranges for cannabis characteristics
        self.validation_rules = {
            'thc_percentage': {'min': 0, 'max': 45, 'typical_max': 35},
            'cbd_percentage': {'min': 0, 'max': 30, 'typical_max': 25},
            'height_cm': {'min': 30, 'max': 300, 'typical_range': (60, 200)},
            'flowering_days': {'min': 35, 'max': 120, 'typical_range': (49, 84)},  # 7-12 weeks
            'yield_grams_per_m2': {'min': 50, 'max': 1000, 'typical_range': (300, 600)},
            'sativa_percentage': {'min': 0, 'max': 100},
            'indica_percentage': {'min': 0, 'max': 100},
            'confidence_score': {'min': 1, 'max': 5}
        }
        
        self.outlier_stats = {
            'total_records': 0,
            'outliers_found': 0,
            'critical_outliers': 0,
            'warnings': 0
        }
    
    def detect_outliers(self, df: pd.DataFrame) -> Dict:
        """
        Main outlier detection method
        Returns comprehensive outlier analysis
        """
        self.outlier_stats['total_records'] = len(df)
        
        outlier_results = {
            'critical_outliers': [],
            'warnings': [],
            'impossible_values': [],
            'suspicious_patterns': [],
            'summary': {}
        }
        
        # Check each validation rule
        for field, rules in self.validation_rules.items():
            if field in df.columns:
                field_outliers = self._check_field_outliers(df, field, rules)
                if field_outliers:
                    outlier_results['critical_outliers'].extend(field_outliers)
        
        # Check for impossible combinations
        combination_outliers = self._check_impossible_combinations(df)
        outlier_results['impossible_values'].extend(combination_outliers)
        
        # Check for suspicious patterns
        pattern_outliers = self._check_suspicious_patterns(df)
        outlier_results['suspicious_patterns'].extend(pattern_outliers)
        
        # Generate summary statistics
        outlier_results['summary'] = self._generate_summary(outlier_results)
        
        return outlier_results
    
    def _check_field_outliers(self, df: pd.DataFrame, field: str, rules: Dict) -> List[Dict]:
        """Check individual field for outliers"""
        outliers = []
        
        # Handle min/max fields (e.g., thc_percentage_min, thc_percentage_max)
        min_field = f"{field}_min"
        max_field = f"{field}_max"
        
        fields_to_check = []
        if min_field in df.columns:
            fields_to_check.append(min_field)
        if max_field in df.columns:
            fields_to_check.append(max_field)
        if field in df.columns:
            fields_to_check.append(field)
        
        for check_field in fields_to_check:
            if check_field not in df.columns:
                continue
                
            # Check minimum values
            if 'min' in rules:
                min_violations = df[df[check_field] < rules['min']].index.tolist()
                for idx in min_violations:
                    outliers.append({
                        'row_index': idx,
                        'field': check_field,
                        'value': df.loc[idx, check_field],
                        'violation_type': 'below_minimum',
                        'expected_min': rules['min'],
                        'severity': 'critical',
                        'strain_name': df.loc[idx].get('strain_name', 'Unknown')\n                    })\n            \n            # Check maximum values\n            if 'max' in rules:\n                max_violations = df[df[check_field] > rules['max']].index.tolist()\n                for idx in max_violations:\n                    outliers.append({\n                        'row_index': idx,\n                        'field': check_field,\n                        'value': df.loc[idx, check_field],\n                        'violation_type': 'above_maximum',\n                        'expected_max': rules['max'],\n                        'severity': 'critical',\n                        'strain_name': df.loc[idx].get('strain_name', 'Unknown')\n                    })\n            \n            # Check typical range warnings\n            if 'typical_range' in rules:\n                typical_min, typical_max = rules['typical_range']\n                \n                # Below typical range\n                below_typical = df[\n                    (df[check_field] >= rules.get('min', 0)) & \n                    (df[check_field] < typical_min)\n                ].index.tolist()\n                \n                for idx in below_typical:\n                    outliers.append({\n                        'row_index': idx,\n                        'field': check_field,\n                        'value': df.loc[idx, check_field],\n                        'violation_type': 'below_typical',\n                        'typical_range': rules['typical_range'],\n                        'severity': 'warning',\n                        'strain_name': df.loc[idx].get('strain_name', 'Unknown')\n                    })\n                \n                # Above typical range\n                above_typical = df[\n                    (df[check_field] <= rules.get('max', float('inf'))) & \n                    (df[check_field] > typical_max)\n                ].index.tolist()\n                \n                for idx in above_typical:\n                    outliers.append({\n                        'row_index': idx,\n                        'field': check_field,\n                        'value': df.loc[idx, check_field],\n                        'violation_type': 'above_typical',\n                        'typical_range': rules['typical_range'],\n                        'severity': 'warning',\n                        'strain_name': df.loc[idx].get('strain_name', 'Unknown')\n                    })\n        \n        return outliers\n    \n    def _check_impossible_combinations(self, df: pd.DataFrame) -> List[Dict]:\n        \"\"\"Check for impossible combinations of values\"\"\"\n        impossible_values = []\n        \n        # Check if min > max for any field\n        min_max_pairs = [\n            ('thc_percentage_min', 'thc_percentage_max'),\n            ('cbd_percentage_min', 'cbd_percentage_max'),\n            ('height_cm_min', 'height_cm_max'),\n            ('flowering_days_min', 'flowering_days_max'),\n            ('yield_grams_per_m2_min', 'yield_grams_per_m2_max')\n        ]\n        \n        for min_field, max_field in min_max_pairs:\n            if min_field in df.columns and max_field in df.columns:\n                violations = df[df[min_field] > df[max_field]].index.tolist()\n                for idx in violations:\n                    impossible_values.append({\n                        'row_index': idx,\n                        'violation_type': 'min_greater_than_max',\n                        'fields': [min_field, max_field],\n                        'min_value': df.loc[idx, min_field],\n                        'max_value': df.loc[idx, max_field],\n                        'severity': 'critical',\n                        'strain_name': df.loc[idx].get('strain_name', 'Unknown')\n                    })\n        \n        # Check if sativa + indica != 100%\n        if 'sativa_percentage' in df.columns and 'indica_percentage' in df.columns:\n            genetics_violations = df[\n                (df['sativa_percentage'].notna()) & \n                (df['indica_percentage'].notna()) &\n                (abs(df['sativa_percentage'] + df['indica_percentage'] - 100) > 1)  # Allow 1% tolerance\n            ].index.tolist()\n            \n            for idx in genetics_violations:\n                sativa = df.loc[idx, 'sativa_percentage']\n                indica = df.loc[idx, 'indica_percentage']\n                total = sativa + indica\n                \n                impossible_values.append({\n                    'row_index': idx,\n                    'violation_type': 'genetics_not_100_percent',\n                    'sativa_percentage': sativa,\n                    'indica_percentage': indica,\n                    'total_percentage': total,\n                    'severity': 'warning' if abs(total - 100) <= 5 else 'critical',\n                    'strain_name': df.loc[idx].get('strain_name', 'Unknown')\n                })\n        \n        # Check for impossible THC + CBD combinations (very high both)\n        if 'thc_percentage_max' in df.columns and 'cbd_percentage_max' in df.columns:\n            high_both = df[\n                (df['thc_percentage_max'] > 20) & \n                (df['cbd_percentage_max'] > 15)\n            ].index.tolist()\n            \n            for idx in high_both:\n                impossible_values.append({\n                    'row_index': idx,\n                    'violation_type': 'high_thc_and_cbd',\n                    'thc_max': df.loc[idx, 'thc_percentage_max'],\n                    'cbd_max': df.loc[idx, 'cbd_percentage_max'],\n                    'severity': 'warning',\n                    'strain_name': df.loc[idx].get('strain_name', 'Unknown'),\n                    'note': 'Rare but possible - verify source data'\n                })\n        \n        return impossible_values\n    \n    def _check_suspicious_patterns(self, df: pd.DataFrame) -> List[Dict]:\n        \"\"\"Check for suspicious patterns that might indicate AI hallucination\"\"\"\n        suspicious_patterns = []\n        \n        # Check for too many perfect round numbers\n        numeric_fields = ['thc_percentage_min', 'thc_percentage_max', 'cbd_percentage_min', 'cbd_percentage_max']\n        \n        for field in numeric_fields:\n            if field in df.columns:\n                # Count values that are perfect multiples of 5\n                round_values = df[df[field] % 5 == 0][field].count()\n                total_values = df[field].notna().sum()\n                \n                if total_values > 0:\n                    round_percentage = (round_values / total_values) * 100\n                    \n                    if round_percentage > 80:  # More than 80% are round numbers\n                        suspicious_patterns.append({\n                            'pattern_type': 'too_many_round_numbers',\n                            'field': field,\n                            'round_percentage': round_percentage,\n                            'total_values': total_values,\n                            'severity': 'warning',\n                            'note': 'High percentage of round numbers may indicate AI estimation'\n                        })\n        \n        # Check for duplicate impossible combinations\n        if len(df) > 100:  # Only check for larger datasets\n            # Look for exact duplicates in key fields\n            key_fields = ['thc_percentage_max', 'cbd_percentage_max', 'flowering_days_max']\n            available_fields = [f for f in key_fields if f in df.columns]\n            \n            if len(available_fields) >= 2:\n                duplicates = df.duplicated(subset=available_fields, keep=False)\n                duplicate_count = duplicates.sum()\n                \n                if duplicate_count > len(df) * 0.1:  # More than 10% duplicates\n                    suspicious_patterns.append({\n                        'pattern_type': 'high_duplicate_rate',\n                        'duplicate_count': duplicate_count,\n                        'total_records': len(df),\n                        'duplicate_percentage': (duplicate_count / len(df)) * 100,\n                        'severity': 'warning',\n                        'note': 'High duplicate rate in key fields may indicate data quality issues'\n                    })\n        \n        return suspicious_patterns\n    \n    def _generate_summary(self, outlier_results: Dict) -> Dict:\n        \"\"\"Generate summary statistics for outlier detection\"\"\"\n        total_outliers = (\n            len(outlier_results['critical_outliers']) + \n            len(outlier_results['impossible_values'])\n        )\n        \n        critical_count = sum(\n            1 for outlier in outlier_results['critical_outliers'] \n            if outlier.get('severity') == 'critical'\n        ) + sum(\n            1 for outlier in outlier_results['impossible_values']\n            if outlier.get('severity') == 'critical'\n        )\n        \n        warning_count = sum(\n            1 for outlier in outlier_results['critical_outliers']\n            if outlier.get('severity') == 'warning'\n        ) + sum(\n            1 for outlier in outlier_results['impossible_values']\n            if outlier.get('severity') == 'warning'\n        )\n        \n        self.outlier_stats['outliers_found'] = total_outliers\n        self.outlier_stats['critical_outliers'] = critical_count\n        self.outlier_stats['warnings'] = warning_count\n        \n        return {\n            'total_records': self.outlier_stats['total_records'],\n            'total_outliers': total_outliers,\n            'critical_outliers': critical_count,\n            'warnings': warning_count,\n            'clean_records': self.outlier_stats['total_records'] - total_outliers,\n            'outlier_percentage': (total_outliers / self.outlier_stats['total_records'] * 100) if self.outlier_stats['total_records'] > 0 else 0,\n            'data_quality_score': max(0, 100 - (total_outliers / self.outlier_stats['total_records'] * 100)) if self.outlier_stats['total_records'] > 0 else 0\n        }\n    \n    def generate_report(self, outlier_results: Dict) -> str:\n        \"\"\"Generate a human-readable outlier detection report\"\"\"\n        report = []\n        report.append(\"=== CANNABIS STRAIN DATA OUTLIER DETECTION REPORT ===\")\n        report.append(\"\")\n        \n        summary = outlier_results['summary']\n        report.append(f\"Total Records Analyzed: {summary['total_records']}\")\n        report.append(f\"Clean Records: {summary['clean_records']} ({100 - summary['outlier_percentage']:.1f}%)\")\n        report.append(f\"Total Outliers: {summary['total_outliers']} ({summary['outlier_percentage']:.1f}%)\")\n        report.append(f\"  - Critical: {summary['critical_outliers']}\")\n        report.append(f\"  - Warnings: {summary['warnings']}\")\n        report.append(f\"Data Quality Score: {summary['data_quality_score']:.1f}/100\")\n        report.append(\"\")\n        \n        # Critical outliers section\n        if outlier_results['critical_outliers']:\n            report.append(\"CRITICAL OUTLIERS (Impossible Values):\")\n            for outlier in outlier_results['critical_outliers'][:10]:  # Show first 10\n                if outlier.get('severity') == 'critical':\n                    strain = outlier.get('strain_name', 'Unknown')\n                    field = outlier.get('field', 'Unknown')\n                    value = outlier.get('value', 'Unknown')\n                    violation = outlier.get('violation_type', 'Unknown')\n                    report.append(f\"  - {strain}: {field} = {value} ({violation})\")\n            \n            if len(outlier_results['critical_outliers']) > 10:\n                report.append(f\"  ... and {len(outlier_results['critical_outliers']) - 10} more\")\n            report.append(\"\")\n        \n        # Impossible combinations section\n        if outlier_results['impossible_values']:\n            report.append(\"IMPOSSIBLE VALUE COMBINATIONS:\")\n            for outlier in outlier_results['impossible_values'][:5]:  # Show first 5\n                strain = outlier.get('strain_name', 'Unknown')\n                violation = outlier.get('violation_type', 'Unknown')\n                report.append(f\"  - {strain}: {violation}\")\n            \n            if len(outlier_results['impossible_values']) > 5:\n                report.append(f\"  ... and {len(outlier_results['impossible_values']) - 5} more\")\n            report.append(\"\")\n        \n        # Suspicious patterns section\n        if outlier_results['suspicious_patterns']:\n            report.append(\"SUSPICIOUS PATTERNS:\")\n            for pattern in outlier_results['suspicious_patterns']:\n                pattern_type = pattern.get('pattern_type', 'Unknown')\n                note = pattern.get('note', '')\n                report.append(f\"  - {pattern_type}: {note}\")\n            report.append(\"\")\n        \n        report.append(\"=== END REPORT ===\")\n        \n        return \"\\n\".join(report)\n\ndef main():\n    \"\"\"Example usage of the Cannabis Outlier Detector\"\"\"\n    \n    # Create sample data with outliers\n    sample_data = {\n        'strain_name': ['Blue Dream', 'Impossible Strain', 'Normal Strain', 'Suspicious Strain'],\n        'thc_percentage_min': [18, 60, 15, 20],  # 60% is impossible\n        'thc_percentage_max': [24, 70, 20, 20],  # 70% is impossible\n        'cbd_percentage_min': [0.1, 0.1, 1.0, 0.5],\n        'cbd_percentage_max': [0.3, 0.2, 2.0, 1.0],\n        'height_cm_min': [120, 500, 80, 100],  # 500cm is impossible\n        'height_cm_max': [180, 600, 120, 150],  # 600cm is impossible\n        'flowering_days_min': [56, 200, 49, 63],  # 200 days is impossible\n        'flowering_days_max': [70, 250, 63, 70],  # 250 days is impossible\n        'sativa_percentage': [60, 70, 50, 60],\n        'indica_percentage': [40, 20, 50, 40],  # Second strain: 70+20=90% (not 100%)\n        'confidence_score': [4, 2, 5, 3]\n    }\n    \n    df = pd.DataFrame(sample_data)\n    \n    detector = CannabisOutlierDetector()\n    outlier_results = detector.detect_outliers(df)\n    \n    # Generate and print report\n    report = detector.generate_report(outlier_results)\n    print(report)\n\nif __name__ == \"__main__\":\n    main()