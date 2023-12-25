{
    "name": "HMS Module",
    "depends": ["base", "mail"],

    "data": [

        "security/hms_security.xml",
        "security/ir.model.access.csv",
        "views/hms_patient_views.xml",
        "views/customer_views.xml",
        "views/hms_doctor_views.xml",
        "views/hms_department_views.xml",
        "report/hms_patient_template.xml",
        "report/hms_reports.xml",
        "data/hms_patient.xml",
        "data/patient_data.xml",
    ],


    "author": "HMS Patient",
    "description": "lab module containing hms patient",
}