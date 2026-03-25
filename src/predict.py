import pandas as pd
import joblib
from fastapi import FastAPI
from src.schema import MachineInputs
import numpy as np
from sklearn.preprocessing import MinMaxScaler

anomaly_model=joblib.load("models/anomaly_pipeline.pkl")
days_model=joblib.load("models/failure_days.pkl")
maintenance_model=joblib.load("models/maintenance_type_prediction.pkl")
threshold=joblib.load("models/threshold.pkl")

app=FastAPI(title="Machine Maintenance System")

@app.get('/')
def home():
    return{"message":"Welcome to Machine Maintenance System"}

MAINT_WEIGHTS={
    "Corrective":1.0,
    "Preventive":0.7,
    "Planned":0.5
}


def decision_label(row):
    if row["Final Score"]>0.6:
        return "Immediate Action Needed. Shut down Equipment"
    elif row["Final Score"]>0.4:
        return "Shedule Maintenance Soon"
    elif row["Anomaly"]==1:
        return "Inspection Needed"
    else:
        return "Normal Operations"
        




@app.post("/predict")
def maintenance_prediction(data:MachineInputs):
    
    input_dict=data.model_dump()
    df=pd.DataFrame([input_dict])
    anomaly=anomaly_model.predict(df)
    proba=days_model.predict_proba(df)[:,1]
    maintenance=maintenance_model.predict(df)
    anomaly_binary=np.where(anomaly==-1,1,0)
    maint_score=np.array([MAINT_WEIGHTS[m] for m in maintenance])
    criteria=np.column_stack([anomaly_binary,proba,maint_score])

    weights=np.array([0.2,0.6,0.2])
    final_score=np.dot(criteria,weights)

    if anomaly_binary ==1:
        answer= "An anomalie in operation has been detected"
    else:
        answer="There is no anomaly detected"




    results=pd.DataFrame({
        "Anomaly":answer,
        "Failure Probability":proba,
        "Maintenance":maintenance,
        "Maintenance Score":maint_score,
        "Final Score":final_score
    })
    results["Final Score"]=results["Final Score"].round(2)
    results["Failure Probability"]=results["Failure Probability"].round(2)
    results['decision']=results.apply(decision_label,axis=1)
    return results.to_dict(orient="records")
