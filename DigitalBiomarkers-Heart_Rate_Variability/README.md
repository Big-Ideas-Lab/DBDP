# Heart Rate Variability

**Objectives:**
Heart rate variability (HRV) is the physiological phenomenon of the variation in the time interval between consecutive heartbeats in milliseconds. Higher HRV has been found to be associated with reduced morbidity and mortality and improved psychological well-being and quality of life. HRV is regulated by the autonomic nervous system and is thus an important indicator of nervous system function. HRV is a potential digital biomarker for a number of diseases and conditions.

**Input:**
RR intervals (ECG) or IBI intervals (wearable watch)

**Output:**
HRV (time domain and frequency domain) metrics, validated by Kubios, the clinical HRV standard

#### Code Available Now:
***

* *E4FileFormatter.ipynb* - Python Notebook that takes as input files from a longitudinal study with an Empatica E4 and compiles data into .csv files for each sensor with timestamps (ISO 8601) adjusted for time zone.
