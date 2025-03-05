import streamlit as st
import time
import requests

# Set page config as the very first command
st.set_page_config(page_title="Unit Converter App", layout="wide")

# Sidebar: Conversion History initialization and display
if "history" not in st.session_state:
    st.session_state.history = []
st.sidebar.header("Conversion History")
if st.session_state.history:
    for entry in st.session_state.history:
        st.sidebar.markdown(f"- {entry}")
else:
    st.sidebar.markdown("No conversions yet.")

# Apply default light theme CSS
st.markdown("""
<!-- External CSS Libraries for animations and icons -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />

<style>
    body {
        background: linear-gradient(135deg, #e2e8f0, #edf2f7);
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding-bottom: 150px; /* Space for fixed footer */
        margin: 0;
    }
    .stApp {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px;
    }
    h1 {
        text-align: center;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .header-icon {
        font-size: 1.1em;
        margin-right: 8px;
        color: #3498db;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: #fff;
        border: none;
        border-radius: 6px;
        font-size: 1em;
        padding: 10px 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease, text-shadow 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.08);
        background: linear-gradient(135deg, #2980b9, #3498db);
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .stSelectbox>div, .stNumberInput>div>div>input {
        border-radius: 6px;
        padding: 8px;
        border: 1px solid #ccc;
        transition: border-color 0.3s ease, transform 0.3s ease;
    }
    .stSelectbox>div:hover, .stNumberInput>div>div>input:hover {
        border-color: #3498db;
        transform: scale(1.01);
    }
    [data-testid='stHorizontalBlock'] > div { margin-right: 8px; }
    .result-container {
        text-align: center;
        font-size: 1.6em;
        font-weight: 600;
        margin-top: 20px;
        color: #3498db;
        padding: 15px;
        border: 1px solid #3498db;
        border-radius: 8px;
        background: #ecf6fd;
        animation: fadeInUp 1s;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #fff; /* Solid white */
        padding: 15px;
        text-align: center;
        box-shadow: 0 -2px 6px rgba(0,0,0,0.1);
        border-top: 1px solid #ddd;
    }
    .powered-by, .developer-name {
        color: #2c3e50;
        font-size: 0.95em;
    }
    .animate-footer .powered-by, .animate-footer .developer-name {
        opacity: 0;
        animation: fadeIn 1s ease forwards;
    }
    .animate-footer .powered-by { animation-delay: 1s; }
    .animate-footer .developer-name { animation-delay: 1.5s; }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @media screen and (max-width: 768px) {
        h1 { font-size: 2em; margin-bottom: 15px; }
        .stApp { margin: 5px; padding: 15px; }
        .stButton>button { font-size: 0.95em; padding: 8px 16px; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='animate__animated animate__fadeInDown'><i class='fas fa-exchange-alt header-icon'></i>Unit Converter App</h1>", unsafe_allow_html=True)

# Conversion functions
def convert_units(value, from_unit, to_unit, conversion_dict):
    if from_unit in conversion_dict and to_unit in conversion_dict:
        return value * (conversion_dict[from_unit] / conversion_dict[to_unit])
    return None

def get_currency_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data['rates']
    except:
        return None

# Conversion UI and Logic
categories = {
    "Length": {"Meter": 1, "Kilometer": 1000, "Centimeter": 0.01, "Inch": 0.0254, "Foot": 0.3048, "Mile": 1609.34},
    "Weight": {"Kilogram": 1, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495},
    "Temperature": "temperature",
    "Speed": {"Meters per second": 1, "Kilometers per hour": 3.6, "Miles per hour": 2.23694},
    "Time": {"Seconds": 1, "Minutes": 60, "Hours": 3600},
    "Area": {"Square Meter": 1, "Square Kilometer": 1e6, "Square Foot": 0.092903, "Acre": 4046.86},
    "Volume": {"Cubic Meter": 1, "Liter": 0.001, "Milliliter": 1e-6, "Gallon": 0.00378541},
    "Energy": {"Joule": 1, "Calorie": 4.184, "Kilowatt-hour": 3600000},
    "Data Storage": {"Byte": 1, "Kilobyte": 1024, "Megabyte": 1048576, "Gigabyte": 1073741824, "Terabyte": 1099511627776},
}
category_options = list(categories.keys()) + ["Currency"]
category = st.selectbox("Select Category", category_options)

if category == "Temperature":
    temp_value = st.number_input("Enter Temperature", value=0.0)
    cols = st.columns(2)
    with cols[0]:
        temp_from = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"], key="temp_from")
    with cols[1]:
        temp_to = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"], key="temp_to")
    if st.button("Convert"):
        with st.spinner("Converting..."):
            time.sleep(1)
        result = None
        if temp_from == temp_to:
            result = temp_value
        elif temp_from == "Celsius" and temp_to == "Fahrenheit":
            result = (temp_value * 9/5) + 32
        elif temp_from == "Celsius" and temp_to == "Kelvin":
            result = temp_value + 273.15
        elif temp_from == "Fahrenheit" and temp_to == "Celsius":
            result = (temp_value - 32) * 5/9
        elif temp_from == "Fahrenheit" and temp_to == "Kelvin":
            result = (temp_value - 32) * 5/9 + 273.15
        elif temp_from == "Kelvin" and temp_to == "Celsius":
            result = temp_value - 273.15
        elif temp_from == "Kelvin" and temp_to == "Fahrenheit":
            result = (temp_value - 273.15) * 9/5 + 32
        conversion_text = f"{temp_value} {temp_from} = {result:.2f} {temp_to}"
        st.markdown(f"<div class='result-container'>Converted Value: {result:.2f} {temp_to}</div>", unsafe_allow_html=True)
        st.session_state.history.append(conversion_text)
        
elif category == "Currency":
    rates = get_currency_rates()
    if rates:
        value = st.number_input("Enter Value", value=1.0)
        cols = st.columns(2)
        with cols[0]:
            from_currency = st.selectbox("From", list(rates.keys()), key="from_currency")
        with cols[1]:
            to_currency = st.selectbox("To", list(rates.keys()), key="to_currency")
        if st.button("Convert"):
            with st.spinner("Fetching exchange rates..."):
                time.sleep(1)
            converted_value = value * (rates[to_currency] / rates[from_currency])
            conversion_text = f"{value} {from_currency} = {converted_value:.4f} {to_currency}"
            st.markdown(f"<div class='result-container'>Converted Value: {converted_value:.4f} {to_currency}</div>", unsafe_allow_html=True)
            st.session_state.history.append(conversion_text)
    else:
        st.error("Failed to fetch currency rates. Try again later.")
        
else:
    units = categories[category]
    value = st.number_input("Enter Value", value=1.0)
    cols = st.columns(2)
    with cols[0]:
        from_unit = st.selectbox("From", list(units.keys()), key="from_units")
    with cols[1]:
        to_unit = st.selectbox("To", list(units.keys()), key="to_units")
    if st.button("Convert"):
        with st.spinner("Converting..."):
            time.sleep(1)
        converted_value = convert_units(value, from_unit, to_unit, units)
        if converted_value is not None:
            conversion_text = f"{value} {from_unit} = {converted_value:.4f} {to_unit}"
            st.markdown(f"<div class='result-container'>Converted Value: {converted_value:.4f} {to_unit}</div>", unsafe_allow_html=True)
            st.session_state.history.append(conversion_text)
        else:
            st.error("Conversion not possible")
            
# Render fixed footer
if "footer_loaded" not in st.session_state:
    st.session_state.footer_loaded = True
    footer_html = """
    <div class="fixed-footer animate-footer">
        <div class="powered-by"><i class="fas fa-bolt"></i> Powered By:</div>
        <div class="developer-name">Syed Muhammad Raza Zaidi</div>
    </div>
    """
else:
    footer_html = """
    <div class="fixed-footer">
        <div class="powered-by" style="opacity:1;"><i class="fas fa-bolt"></i> Powered By:</div>
        <div class="developer-name" style="opacity:1;">Syed Muhammad Raza Zaidi</div>
    </div>
    """
st.markdown(footer_html, unsafe_allow_html=True)