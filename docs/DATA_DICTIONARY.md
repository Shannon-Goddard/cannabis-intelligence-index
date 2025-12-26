## 📖 Data Dictionary: Index Architecture 
This file defines the schema for both the **Bronze (Source of Truth)** and **Gold (Standardized) layers**.  


| Field Name         | Layer  | Data Type | Description                                                                 |
|--------------------|--------|-----------|-----------------------------------------------------------------------------|
| strain_name        | Both   | String    | The common name of the cultivar as listed by the breeder.                    |
| height_raw         | Bronze | String    | Verbatim height description from the HTML source.                           |
| height_cm_avg      | Gold   | Integer   | Standardized height in cm. (Mean of ranges; "Tall" mapped to 180cm).        |
| flower_days_avg    | Gold   | Integer   | Total flowering duration in days. (Weeks converted to Days).                 |
| thc_pct_max        | Gold   | Float     | The highest reported THC percentage (0.00 format).                          |
| anomaly_notes      | Gold   | String    | Log of conflicts (e.g., Table vs. Text) and AI reasoning for the chosen value. |
| confidence_score   | Gold   | Integer   | 1-5 rating of data quality based on source detail and internal consistency. |

