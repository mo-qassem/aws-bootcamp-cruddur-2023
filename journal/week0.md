# Week 0 — Billing and Architecture
#### Tasks
* [x] Destroy your root account credentials, Set MFA, IAM role.
* [x] Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
* [ ] Review all the questions of each pillars in the Well Architected Tool (No specialized lens).
* [ ] Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts.
* [ ] Research the technical and service limits of specific services and how they could impact the technical path for technical flexibility. 
* [ ] Open a support ticket and request a service limit.

---
- **Destroy your root account credentials, Set MFA, IAM role.**
  1. Create new **IAM User** with MFA enabled and access key for utilizing AWS CLI. 
  2. Activate **IAM Access** to enable IAM USER able to access billing informations insted of using root account.
  3. Enable MFA for root account to add another secuirty factor.
  4. Change account password policy with more password strength rules and min 10 chars.
  5. Create **IAM Role** with administartion access and assign this role to **IAM Group** with assigned user init.
  

- **Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.**
  1. create eventbridge rule watching any event from AWS health Dashboard matching any service any resouce (not create any resouce yet).
  ![EventBridge](/aws-bootcamp-cruddur-2023/journal/screenshots/eventbridge.png)

    
  
