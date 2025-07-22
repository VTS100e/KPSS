Of course, here is a `README.md` file for the provided Python script.

-----

# 📊 KPSS Stationarity Test App

A simple web application built with [Streamlit](https://streamlit.io/) to perform the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test on your time series data.

The KPSS test is a statistical test used to check for the stationarity of a time series. Stationarity is a key assumption in many time series forecasting models. This application provides an easy-to-use interface to upload your data, run the test, and interpret the results.

***Note:** The user interface of this application is in Indonesian.*

## ✨ Features

  - **CSV Upload:** Easily upload your time series data in a `.csv` file.
  - **Column Selection:** Choose the specific column from your data you wish to test.
  - **Test Configuration:**
      - Select the stationarity hypothesis:
          - **Level Stationary (`c`):** Tests for stationarity around a constant mean.
          - **Trend Stationary (`ct`):** Tests for stationarity around a deterministic trend.
      - Configure the number of lags (`nlags`):
          - **Automatic (`auto`):** Let the `statsmodels` library determine the optimal number of lags.
          - **Manual:** Set the number of lags manually, with a recommendation provided based on the Schwert formula.
  - **Clear Results:** Get the KPSS statistic, p-value, and the number of lags used.
  - **Simple Interpretation:** The application provides a clear conclusion on whether the data is likely stationary or not based on a 5% significance level.
  - **Critical Values:** View the critical values for the test statistic at different significance levels (10%, 5%, 2.5%, and 1%).

## 🔬 How the KPSS Test Works

The KPSS test is based on the following hypotheses:

  - **Null Hypothesis ($H\_0$):** The time series is stationary.
  - **Alternative Hypothesis ($H\_1$):** The time series has a unit root (is non-stationary).

A p-value below a chosen significance level (e.g., 0.05) indicates that we reject the null hypothesis, suggesting that the time series is **non-stationary**. Conversely, a p-value at or above the significance level means we fail to reject the null hypothesis, suggesting the data is **stationary**.

## ⚙️ Requirements

You will need the following Python libraries to run this application:

  - `streamlit`
  - `pandas`
  - `statsmodels`
  - `numpy`

You can install them all using pip:

```bash
pip install streamlit pandas statsmodels numpy
```

## 🚀 How to Run Locally

1.  **Save the Code:** Save the provided script as `main.py`.

2.  **Open Terminal:** Open your terminal or command prompt.

3.  **Navigate to Directory:** Navigate to the folder where you saved `main.py`.

4.  **Run the App:** Execute the following command in your terminal:

    ```bash
    streamlit run main.py
    ```

5.  Your web browser should open a new tab with the running application.

## 📋 Usage Guide

1.  **Upload Data:** Click on **"Pilih file CSV"** (Choose CSV file) to upload your time series data.
2.  **Preview Data:** A preview of the first few rows of your dataset will be displayed.
3.  **Configure Test:**
      - **Select Column:** From the dropdown menu (`Pilih kolom time series`), select the column containing the time series you want to test.
      - **Select Hypothesis:** Choose between **"Stasioner di sekitar rata-rata"** (Level Stationary) or **"Stasioner di sekitar tren"** (Trend Stationary).
      - **Set Lags:** Choose **"Otomatis"** (Automatic) or **"Manual"** to set the number of lags.
4.  **Run Test:** Click the **"Jalankan Tes KPSS"** (Run KPSS Test) button.
5.  **View Results:** The application will display the test statistics and a clear interpretation, stating whether your data is likely stationary or not. You can view the critical values in the expandable section.
