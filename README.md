# Healthfirst Data Case Study

Data information:  
CMS publishes synthetic claims and beneficiary data available for the public. Claims are generated whenever healthcare providers submit a request for payment to a health plan, proving information about the interactions between the patients, healthcare providers and insurers. The data includes information about the visit including diagnosis code, service dates, charged amount and national provider identifier (NPI). 
We have combined beneficiary demographic data with their respective claims. The data set contains beneficiary claims from 2021-2023. One beneficiary can have multiple claims. Each row represents a claim and the principal diagnosis code on the claim represents the diagnosis received by the member during their visit. 
A few useful column descriptions: 
-	BENE_ID: The unique identifier for a beneficiary 
-	Age: Age of the member as of the date of the claim. (Claim_from_date - Date_of_birth)
-	CLM_ID: The unique identifier for a claim
-	CLM_FROM_DT: Date of service 
-	CLM_THRU_DT: Service end date 
-	CLM_PMT_AMT: Amount paid on the claims
-	NCH_CARR_CLM_SBMTD_CHRG_AMT: The total charges submitted on the claim
-	NCH_CARR_CLM_ALOWD_AMT: The total allowed charges on the claim i.e., the maximum amount a plan will pay for a covered health service
-	RFR_PHYSN_NPI: The national provider identifier (NPI) number assigned to uniquely identify the referring physician 
-	PRNCPAL_DGNS_CD: The ICD 10 diagnosis code identifying the diagnosis, condition, problem, or other reason for the admission/encounter/visit shown in the medical record to be chiefly responsible for the services provided.
-	PRNCPAL_DGNS_DESC:  Principal diagnosis code description
-	ICD_DGNS_CD1: Additional diagnosis code on the claims for identifying the beneficiary's diagnosis.
-	ICD_DGNS_CD1_DESC: Diagnosis code 1 description

Background: According to a report from the centers of disease control and prevention, Americans living with chronic physical and mental health conditions account for 90% of the $3.3 trillion the U.S. spends each year on healthcare. Care management is a comprehensive approach to healthcare that aims to improve patient outcomes and reduce healthcare costs through coordinated and personalized care. It is a proactive approach to healthcare that emphasizes prevention, coordinated care and patient engagement, ultimately aiming to improve outcomes and reduce overall healthcare costs 
Goal: As a care plan, we want to infer the health status of the beneficiaries/members. Analyze claims data to infer health status of patients and identify high-cost areas. Propose a data driven solution and provide a recommendation of a care management program that will help improve patient outcomes, health, and reduce healthcare costs. 
Based on your findings and exploratory data analysis:
-	Propose an area that you might implement a care management program based on your analysis. 
-	What type of data driven solution would you recommend building to implement this program?
-	Be prepared to highlight any limitations.
-	What would you do if you had more time? 
