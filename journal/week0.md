# Week 0 — Billing and Architecture
#### Tasks
* [x] Destroy your root account credentials, Set MFA, IAM role.
* [x] Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.
* [x] Review all the questions of each pillars in the Well Architected Tool (No specialized lens).
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
  1. create eventbridge rule watching any event from AWS health Dashboard matching any service any resouce (not created any resouce yet).

  ![EventBridge](/journal/screenshots/eventbridge.png)
  
  2. 
 
- **Review all the questions of each pillars in the Well Architected Tool (No specialized lens).**






- **Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts.**
  1. create conceptual diagram to discuss core services. [lucid.app link](https://lucid.app/lucidchart/528e2147-f727-422f-b5d2-7781c6539b58/edit?invitationId=inv_0b9d5529-b1f3-4ece-ae44-06c6bfce333f)
  ![conceptual diagram](/journal/screenshots/Cruddur - conceptual diagram.png)
  
  2. create logical digram for CI/CD tools on aws.  [lucid.app link](https://lucid.app/lucidchart/f67ad73b-363b-47f3-b7a5-5b37801a4b9a/edit?invitationId=inv_a3360ace-38a6-47a2-93f0-b7e780647a14)
  ![logical diagram](/journal/screenshots/Cruddur - CI_CD Pipeline.png)
    
  
