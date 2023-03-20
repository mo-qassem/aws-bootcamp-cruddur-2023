# Week 0 — Billing and Architecture

### Homework Tasks

| VIDEOS                                                                                                                                    | WATCHED            |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| [Ashish's Week 0 - Security Considerations](https://www.youtube.com/watch?v=4EMWBYVggQI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=15) | :heavy_check_mark: |
| [Chirag's Week 0 - Spend Considerations](https://www.youtube.com/watch?v=OVw3RrlP-sI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=13)    | :heavy_check_mark: |

| TASKS                                                                                                                       | COMPLETED          |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| [Recreate Conceptual Diagram in Lucid Charts or on a Napkin](#1-recreate-conceptual-diagram-in-lucid-charts-or-on-a-napkin) | :heavy_check_mark: |
| [Recreate Logical Architectual Diagram in Lucid Charts.](#2-recreate-logical-architectual-diagram-in-lucid-charts)          | :heavy_check_mark: |
| [Create an Admin User](#3-create-an-admin-user)                                                                             | :heavy_check_mark: |
| [Use CloudShell](#4-use-cloudshell)                                                                                         | :heavy_check_mark: |
| [Installed AWS CLI](#5-installed-aws-cli)                                                                                   | :heavy_check_mark: |
| [Create a Billing Alarm](#6-create-a-billing-alarm)                                                                         | :heavy_check_mark: |
| [Create a Budget](#7-create-a-budget)                                                                                       | :heavy_check_mark: |

---

## 1. Recreate Conceptual Diagram in Lucid Charts or on a Napkin.

- Create a conceptual diagram to communicate the architecture to key stakeholders. [lucid.app link](https://lucid.app/lucidchart/528e2147-f727-422f-b5d2-7781c6539b58/edit?invitationId=inv_0b9d5529-b1f3-4ece-ae44-06c6bfce333f)

  ![conceptual diagram](/journal/screenshots/cruddur_conceptual_diagram.png)

## 2. Recreate Logical Architectual Diagram in Lucid Charts.

- Create a logical diagram to communicate the broad strokes of the technical architecture to engineers. [lucid.app link](https://lucid.app/lucidchart/a732e814-2839-48ee-9ddd-7fd5d9593d1a/edit?invitationId=inv_cb5556ca-c556-4848-ba34-02e9ad45cdb6)

  ![logical diagram](/journal/screenshots/cruddur_logical_digram.png)

## 3. Create an Admin User.

- Create a new **IAM User** with MFA enabled and access key for utilizing AWS CLI on Gitpod.
- Activate **IAM Access** to make IAM USER able to access billing information instead of using a root account.
- Enable MFA for the root account to add another security layer.
- Create **IAM Role** with administration access and assign this role to **IAM Group** with assigned user init.
- Change account password policy with more password strength rules and min 10 chars.

## 4. Use CloudShell.

- We are not able to launch cloudshell, we tried all the action from restart the cloudshell and delete home directory but without any luck.

![cloudshell](/journal/screenshots/week0_error.png)
![cloudshell](/journal/screenshots/week0_reload_cs.png)
![cloudshell](/journal/screenshots/week0_restart_cs.png)

## 5. Installed AWS CLI.

> [Direct to .gitpod.yml](/.gitpod.yml)

## 6. Create a Billing Alarm.

- We utlize AWS Console to create a cloudwatch billing alarm.

![billing alarm](/journal/screenshots/week0_cloudwatch_alarm.png)

## 7. Create a Budget.

- We utlize also AWS Console to create a budget.

![budget](/journal/screenshots/week0_budgets.png)

---

### Homework Challenges

| TASKS                                                                                                                                                                                                                              | COMPLETED          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| [Destroy your root account credentials, Set MFA, IAM role.](#1-destroy-your-root-account-credentials-set-mfa-iam-role)                                                                                                             | :heavy_check_mark: |
| [Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.](#2-use-eventbridge-to-hookup-health-dashboard-to-sns-and-send-notification-when-there-is-a-service-health-issue)   | :heavy_check_mark: |
| [Review all the questions of each pillars in the Well Architected Tool (No specialized lens).](#3-review-all-the-questions-of-each-pillars-in-the-well-architected-tool-no-specialized-lens)                                       | :heavy_check_mark: |
| [Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts.](#4-create-an-architectural-diagram-to-the-best-of-your-ability-the-cicd-logical-pipeline-in-lucid-charts)              | :heavy_check_mark: |
| [Research best practices of Dockerfiles and attempt to implement it in your Dockerfile.](#5-research-the-technical-and-service-limits-of-specific-services-and-how-they-could-impact-the-technical-path-for-technical-flexibility) | :heavy_check_mark: |
| [Open a support ticket and request a service limit.](#6-open-a-support-ticket-and-request-a-service-limit)                                                                                                                         | :heavy_check_mark: |

---

## 1. Destroy your root account credentials, Set MFA, IAM role.

- The screenshot from IAM Dashboard prove that we enabled MFA and no active access key for the Root Account plus the actions we took on "Create an Admin User" step.

![IAM](/journal/screenshots/iam.png)

## 2. Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue.

- Create eventbridge rule watching any event from AWS health Dashboard matching any service and any resource in AWS Reigon US-EAST-1.

![EventBridge](/journal/screenshots/week0_eventbridge.png)

## 3. Review all the questions of each pillars in the Well Architected Tool (No specialized lens).

- We answered the questions for Cost Optimization and Operational Excellence with the plan to check the other pillars when we have some workload for better recommendations.

![well_arichtect](/journal/screenshots/week0_well_archit.png)

## 4. Create an architectural diagram (to the best of your ability) the CI/CD logical pipeline in Lucid Charts.

- Create a logical diagram for CI/CD tools on AWS. [lucid.app link](https://lucid.app/lucidchart/f67ad73b-363b-47f3-b7a5-5b37801a4b9a/edit?invitationId=inv_a3360ace-38a6-47a2-93f0-b7e780647a14)

![logical diagram](/journal/screenshots/cruddur_cicd_pipeline.png)

## 5. Research the technical and service limits of specific services and how they could impact the technical path for technical flexibility.

- We did our research and we found Amazon Elastic Container Service does not have a free tier allowance and Amazon Elastic Container Registry has only 500MB which lead us to utilize Amazon Elastic Container Service in EC2 mode to employ the 750 hours included with free tier.

## 6. Open a support ticket and request a service limit.

![support ticket](/journal/screenshots/week0_service_case.png)
