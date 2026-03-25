import streamlit as st
import requests
API_URL=st.secrets["API_URL"]
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
        response=requests.post(API_URL,json=payload)
        result=response.json()[0]

        anomaly=result["Anomaly"]
        prob=result["Failure Probability"]
        score=result["Final Score"]
        maintenance=result["Maintenance"]
        decision=result["decision"]

        if score> 0.6:
            st.error("#### HIGH RISK")
        elif score > 0.4:
            st.warning("#### MEDIUM RISK")
        else:
            st.success("#### LOW RISK")

        st.divider()
        if "no anomaly" in anomaly.lower():
            st.success("#### No Anomaly Detected")
        else:
            st.error("#### Anomaly Detected")
        

        st.divider()
        c1,c2,c3=st.columns(3)

        
        with c1:
            st.markdown("#### Failure Risk")
            st.metric("",f"{prob*100:.2f}%")
        with c2:
            st.markdown("#### Maintenance")
            st.metric("",maintenance)
        with c3:
            st.markdown("#### Score")
            st.metric("",f"{score:.2f}")

        st.divider()
        st.subheader("Recommended Action")
        st.write(f"#### {decision}")
        st.markdown("---")
        st.markdown("Built By **Omari Kwache Justus Junior**")