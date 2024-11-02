# Analisa Air Quality ✨

## Dataset 
PRSA_Data_Shunyi_20130301-20170228.csv

## Live Dashboard

### Setup Environment

1. **Python Environment**:
   - Conda (ensure [Conda](https://docs.conda.io/en/latest/) is installed):
     ```
     conda create --name aq-ds python=3.9
     conda activate aq-ds
     ```
   - venv (standard Python environment tool):
     ```
     python -m venv aq-ds
     source aq-ds/bin/activate  # On Windows use `aq-ds\Scripts\activate`
     ```

2. **Install Required Packages**:
   - Untuk menjalankan analisa dan dashboard:
     ```
     pip install pandas numpy matplotlib seaborn streamlit
     ```

     atau dengan
     ```
     pip install -r requirements.txt
     ```
### Menajalankan Dashboard

1. **Dashboard Directory**:
    ```
     cd dashboard 
    ```

2. **Run Streamlit App**:
    ```
    streamlit run dashboard.py
    ```