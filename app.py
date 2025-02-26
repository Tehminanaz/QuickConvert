import streamlit as st
import pandas as pd

def main():
    st.title("Advanced Unit Converter")
    st.write("Convert between different units of measurement with added features like multi-value conversion and conversion history.")
    
    # Sidebar for selecting conversion category
    category = st.sidebar.selectbox(
        "Select Conversion Category",
        ["Length", "Weight/Mass", "Temperature", "Area", "Volume", "Speed", "Time"]
    )
    
    # Define conversion factors and symbols/formulas for each category
    conversion_factors = {
        "Length": {
            "Meter": 1.0,
            "Kilometer": 0.001,
            "Centimeter": 100.0,
            "Millimeter": 1000.0,
            "Mile": 0.000621371,
            "Yard": 1.09361,
            "Foot": 3.28084,
            "Inch": 39.3701
        },
        "Weight/Mass": {
            "Kilogram": 1.0,
            "Gram": 1000.0,
            "Milligram": 1000000.0,
            "Metric Ton": 0.001,
            "Pound": 2.20462,
            "Ounce": 35.274,
            "Stone": 0.157473
        },
        "Temperature": {
            "Celsius": "C",
            "Fahrenheit": "F",
            "Kelvin": "K"
        },
        "Area": {
            "Square Meter": 1.0,
            "Square Kilometer": 0.000001,
            "Square Centimeter": 10000.0,
            "Square Millimeter": 1000000.0,
            "Square Mile": 3.861e-7,
            "Square Yard": 1.19599,
            "Square Foot": 10.7639,
            "Square Inch": 1550.0,
            "Acre": 0.000247105,
            "Hectare": 0.0001
        },
        "Volume": {
            "Cubic Meter": 1.0,
            "Cubic Centimeter": 1000000.0,
            "Liter": 1000.0,
            "Milliliter": 1000000.0,
            "Gallon (US)": 264.172,
            "Quart (US)": 1056.69,
            "Pint (US)": 2113.38,
            "Cup (US)": 4226.75,
            "Fluid Ounce (US)": 33814.0,
            "Cubic Inch": 61023.7,
            "Cubic Foot": 35.3147
        },
        "Speed": {
            "Meter per second": 1.0,
            "Kilometer per hour": 3.6,
            "Mile per hour": 2.23694,
            "Foot per second": 3.28084,
            "Knot": 1.94384
        },
        "Time": {
            "Second": 1.0,
            "Millisecond": 1000.0,
            "Microsecond": 1000000.0,
            "Minute": 1/60.0,
            "Hour": 1/3600.0,
            "Day": 1/86400.0,
            "Week": 1/604800.0,
            "Month (30 days)": 1/2592000.0,
            "Year (365 days)": 1/31536000.0
        }
    }
    
    # Get available units for the selected category
    units = list(conversion_factors[category].keys())
    
    # Option for multi-value conversion
    multi_value = st.checkbox("Convert multiple values (comma separated)?")
    if multi_value:
        input_str = st.text_input("Enter values separated by commas", "1.0")
        try:
            values = [float(val.strip()) for val in input_str.split(",")]
        except ValueError:
            st.error("Please enter valid numeric values separated by commas.")
            values = []
    else:
        value = st.number_input("Enter value", value=1.0)
        values = [value]
    
    # Two columns for 'from' and 'to' unit selection
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From", units, key="from_unit")
    with col2:
        to_unit = st.selectbox("To", units, key="to_unit")
    
    results = []
    # Process conversion for each entered value
    for val in values:
        if category == "Temperature":
            converted = convert_temperature(val, from_unit, to_unit)
        else:
            if from_unit == to_unit:
                converted = val
            else:
                factor_from = conversion_factors[category][from_unit]
                factor_to = conversion_factors[category][to_unit]
                # Convert to a base unit first, then to target unit
                base_val = val / factor_from if factor_from != 0 else 0
                converted = base_val * factor_to
        results.append(converted)
    
    # Display the conversion results
    st.subheader("Conversion Result")
    if multi_value:
        for original, converted in zip(values, results):
            st.write(f"{original} {from_unit} = {converted:.6g} {to_unit}")
    else:
        st.write(f"{values[0]} {from_unit} = {results[0]:.6g} {to_unit}")
    
    # Display the conversion formula (when applicable)
    st.subheader("Conversion Formula")
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            st.write("°F = (°C × 9/5) + 32")
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            st.write("°C = (°F - 32) × 5/9")
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            st.write("K = °C + 273.15")
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            st.write("°C = K - 273.15")
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            st.write("K = (°F - 32) × 5/9 + 273.15")
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            st.write("°F = (K - 273.15) × 9/5 + 32")
        else:
            st.write("No conversion needed")
    elif from_unit == to_unit:
        st.write("No conversion needed")
    else:
        if category != "Temperature":
            factor = conversion_factors[category][to_unit] / conversion_factors[category][from_unit]
            st.write(f"Multiply by {factor:.6g}")
    
    # Conversion history using Streamlit session state
    if "history" not in st.session_state:
        st.session_state.history = []
    
    conversion_record = {
        "Category": category,
        "From": f"{values} {from_unit}",
        "To": f"{results} {to_unit}"
    }
    
    if st.button("Add to History"):
        st.session_state.history.append(conversion_record)
    
    if st.session_state.history:
        st.subheader("Conversion History")
        df_history = pd.DataFrame(st.session_state.history)
        st.table(df_history)

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    if from_unit == to_unit:
        return value
    
    # Convert input value to Celsius
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:  # Already in Celsius
        celsius = value
    
    # Convert from Celsius to the target unit
    if to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        return celsius

if __name__ == "__main__":
    main()
