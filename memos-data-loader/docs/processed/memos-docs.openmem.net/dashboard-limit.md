---
source_url: https://memos-docs.openmem.net/dashboard/limit
section: Dashboard
scraped_date: 2025-10-16
title: Limits
has_images: yes
has_tables: yes
---

# Limits
 [ MemOS provides each developer with free quota to quickly experience and validate its memory capabilities. 
## 1. Free Quota
 
[The MemOS Cloud Service currently provides all developers with the following free development quotas for the APIs, calculated based on **number of calls**. Different APIs consume quota differently, as shown in the table below:]
 
<table><thead><tr><th>API Name</th><th>Consumption Type</th><th>Description</th><th>Free Quota (Calls)</th></tr></thead><tbody><tr><td>addMessage</td><td>Number of calls</td><td>Each successful request consumes 1 call</td><td>5,000</td></tr><tr><td>searchMemory</td><td>Number of calls</td><td>Each successful request consumes 1 call</td><td>1,000</td></tr><tr><td>getMessage</td><td>Number of calls</td><td>Each successful request consumes 1 call</td><td>5,000</td></tr></tbody></table> **Note** 
- [The free quota is provided per **developer account** and is shared across all projects under that account.]
- [Failed requests (authentication failure, parameter error, exceeding limits, etc.) **do not consume quota**.] ## 2. Resource Limits
 
[To ensure stable and secure service, MemOS Cloud Service enforces the following limits on API calls, calculated at the account level:]
 
<table><thead><tr><th>API Name</th><th>Max Input per Request</th><th>Max Output per Request</th><th>Total Call Limit</th></tr></thead><tbody><tr><td>addMessage</td><td>4,000 tokens</td><td>-</td><td>5,000</td></tr><tr><td>searchMemory</td><td>4,000 tokens</td><td>10 memories</td><td>1,000</td></tr><tr><td>getMessage</td><td>-</td><td>50 messages</td><td>5,000</td></tr></tbody></table> **Note** 
- [Requests exceeding the per-call limit will return the corresponding error code without deducting quota.]
- [Additionally, we recommend a maximum QPS â¤ 10 (i.e., up to 10 requests per second). This is not a strict limit, but high concurrency may be affected by platform capacity, so control request frequency according to actual needs.] ## 3. Usage Monitoring
 
[You can view the remaining quota for each API through the **API Console**, with filters for project, API key, and date to facilitate tracking and managing usage.] ![image](./IMAGES/dashboard-limit-49cddd25-6fbf-40d4-a750-58c3b2ac5547-1) ## 4. Obtaining More Quota
 
[To help developers quickly try and validate features while considering resource costs, each developer is provided a **limited free quota**. When usage exceeds the free quota, the system will block excess requests and provide a prompt, ensuring platform stability.]
 
[If you need more API calls, simply scan the QR code below with your personal WeChat app (no need to install WeCom/Enterprise WeChat) to reach our support team and receive extra free quota.
Not using WeChat? Scan the Discord QR code in the Contact Us section below to join our channel and get additional quota.]
 
[[ [ ]]]
