import csv
import os
from datetime import datetime

machine_maintenance = "logs.csv"

def log_data(Payload,results):
    file_exists=os.path.isfile(machine_maintenance)

    with open(machine_maintenance,mode="a",newline="")as file:
        writer=csv.writer(file)
        if not file_exists:
            writer.writerow([
                "timestamp",
                "temperature",
                "vibration",
                "pressure",
                "component",
                "subcomponent",
                "section",
                "failure_probability",
                "maintenance",
                "maint_score",
                "final_score",
                "anomaly"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(Payload["temperature"],2),
            round(Payload["vibration"],2),
            round(Payload["pressure"],2),
            Payload["component"],
            Payload["subcomponent"],
            Payload["section"],
            results["Failure Probability"],
            results["Maintenance"],
            results["Maintenance Score"],
            results["Final Score"],
            results["Anomaly"]

        ])
