# Week 0 — Billing and Architecture
### Homework Tasks
- [x] Recreate Conceptual Diagram in Lucid Charts or on a Napkin.
- [x] Recreate Logical Architectual Diagram in Lucid Charts.
- [x] Create an Admin User
- [x] Installed AWS CLI
- [x] Create a Billing Alarm
- [x] Create a Budget
---
### 1. Recreate Conceptual Diagram in Lucid Charts or on a Napkin.
- Create conceptual diagram to communicate the architecture to key stakeholders. [lucid.app link](https://lucid.app/lucidchart/528e2147-f727-422f-b5d2-7781c6539b58/edit?invitationId=inv_0b9d5529-b1f3-4ece-ae44-06c6bfce333f)
 
  ![conceptual diagram](/journal/screenshots/cruddur_conceptual_diagram.png)
  
### 2. Recreate Logical Architectual Diagram in Lucid Charts.
- Create logical digram to communicate the broad strokes  of the technical architecture to engineers. [lucid.app link](https://lucid.app/lucidchart/a732e814-2839-48ee-9ddd-7fd5d9593d1a/edit?invitationId=inv_cb5556ca-c556-4848-ba34-02e9ad45cdb6)

  ![logical diagram](/journal/screenshots/cruddur_logical_digram.png)
  
### 3. Create an Admin User.
- Create new **IAM User** with MFA enabled and access key for utilizing AWS CLION Gitpod.
- Activate **IAM Access** to enable IAM USER able to access billing informations insted of using root account.
- Enable MFA for root account to add another secuirty layer.
- Create **IAM Role** with administartion access and assign this role to **IAM Group** with assigned user init.
- Change account password policy with more password strength rules and min 10 chars.

### 4. Installed AWS CLI.

> [Direct to .gitpod.yml](/.gitpod.yml)

### 5. Create a Billing Alarm.
- We utlize AWS Console to create cloudwatch billing alarm.

![billing alarm](/journal/screenshots/week0_cloudwatch_alarm.png)

### 6. Create a Budget.
- We utlize AWS Console to create budget also.

![budget](/journal/screenshots/week0_budgets.png)

---

###  Homework Challenges
- [x] Destroy your root account credentials, Set MFA, IAM role.
- [x] Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
- [x] Review all the questions of each pillars in the Well Architected Tool (No specialized lens).
- [ ] Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts.
- [ ] Research the technical and service limits of specific services and how they could impact the technical path for technical flexibility. 
- [ ] Open a support ticket and request a service limit.
---
### 1. Destroy your root account credentials, Set MFA, IAM role.

![IAM](/journal/screenshots/iam.png)
   
  
 

### 2. Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
  - Create eventbridge rule watching any event from AWS health Dashboard matching any service any resouce (not created any resouce yet).

  ![EventBridge](/journal/screenshots/eventbridge.png)
  
 
### 3. Review all the questions of each pillars in the Well Architected Tool (No specialized lens).
- We 





### 4. Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts.  
  - Create logical digram for CI/CD tools on aws.  [lucid.app link](https://lucid.app/lucidchart/f67ad73b-363b-47f3-b7a5-5b37801a4b9a/edit?invitationId=inv_a3360ace-38a6-47a2-93f0-b7e780647a14)

  ![logical diagram](/journal/screenshots/cruddur_cicd_pipeline.png)
  
### 5. Research the technical and service limits of specific services and how they could impact the technical path for technical flexibility. 
### 6. Open a support ticket and request a service limit.
  

  
