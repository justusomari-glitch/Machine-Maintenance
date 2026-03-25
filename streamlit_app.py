import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Machine Maintenance Control Panel")
left,right=st.columns([1,2])

with left:
    st.subheader("Inputs")
    machine_age =st.number_input("Machine Age (days)",min_value=0)
    temperature=st.number_input("Temperature ")
    vibration =st.number_input("Vibration")
    pressure =st.number_input("Pressure")
    section= st.selectbox("Section",['Kiln','Cement Mill','Crusher'])
    component= st.selectbox("Component",['Ball Mill','Roller Press','Vertical Mill'])
    subcomponent= st.selectbox("Subcomponent",['Gearbox','Hydraulic System','Mill Bearing','Motor'])
    run=st.button("Analyze")

with right:
    st.subheader("Result")
    if run :
        payload={
            "machine_age_days":machine_age,
            "temperature":temperature,
            "vibration":vibration,
            "pressure":pressure,
            "component":component,
            "subcomponent":subcomponent,
            "section":section
        }
        response=requests.post("https://machine-maintenance-6t6v.onrender.com/predict",json=payload)
        result=response.json()[0]

        anomaly=result["Anomaly"]
        prob=result["Failure Probability"]
        score=result["Final Score"]
        maintenance=result["Maintenance"]
        decision=result["decision"]

        if score> 0.6:
            st.error("HIGH RISK")
        elif score > 0.4:
            st.warning("MEDIUM RISK")
        else:
            st.success("LOW RISK")

        st.divider()
        st.subheader("Anomaly Indication")
        st.write(anomaly)

        st.divider()
        c1,c2,c3=st.columns(3)

        
        c1.metric("Faiure Risk",f"{prob*100:.1f}%")
        c2.metric("Maintenance",maintenance)
        c3.metric("Score",f"{score:.2f}")

        st.divider()
        st.subheader("Recommended Action")
        st.write(decision)