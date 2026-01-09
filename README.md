Identity & Access Review System

Overview

This project is a **Python-based simulation of an enterprise Identity & Access Management (IAM) and Identity Governance (IGA) system**, designed to demonstrate how organizations manage user access, enforce least privilege, and conduct access reviews beyond basic role-based authentication.

The system focuses on **identity lifecycle management, governance, auditability, and Zero Trust controls**, rather than UI or scale.



Key Objectives

* Simulate **enterprise IAM workflows** in a controlled environment
* Demonstrate **access review and governance concepts**
* Model **risk-aware access decisions**
* Understand how **IAM failures lead to security incidents**



High-Level Architecture

```
+--------------------+
|      Login UI      |
|  (Username + MFA)  |
+---------+----------+
          |
          v
+--------------------+
| Authentication     |
| - Password Check   |
| - TOTP MFA         |
| - Lockout Control  |
+---------+----------+
          |
          v
+-----------------------------+
| Identity Store (users.json) |
| - Users                     |
| - Roles                     |
| - Entitlements              |
| - JIT Access                |
| - Account State             |
+---------+-------------------+
          |
          v
+-----------------------------+
| Governance & Review Engine  |
| - Access Reviews            |
| - Entitlement Risk          |
| - JIT Expiry Detection      |
| - SoD Violation Detection  |
+---------+-------------------+
          |
          v
+-----------------------------+
| Audit Logging               |
| - Auth Events               |
| - Role Changes              |
| - Access Decisions          |
+-----------------------------+
```

Core Features of this project

Authentication & Zero Trust

* Username & password authentication
* **TOTP-based MFA (RFC-6238 compatible)**
* Per-user MFA secrets (Authenticator compatible)
* **Account lockout after repeated MFA failures**
* User-visible lockout messaging with timestamp


Identity Lifecycle Management (JML)

* **Joiner**: New user onboarding
* **Mover**: Role changes and access updates
* **Leaver**: Account disable instead of delete
* Rehire supported via account reactivation


Identity Governance & Access Reviews

* Role-based access reviews
* **Entitlement-based access reviews**
* Detection of **high-risk entitlements**
* **Just-In-Time (JIT) access expiry detection**
* Policy-driven **Separation of Duties (SoD)** violation detection
* Read-only **CISO dashboard** for security oversight


Separation of Duties (SoD)

The system detects policy violations such as:

* Developer assigned privileged administrative roles
* HR and finance-related conflicts
* Privilege escalation risks

SoD policies are defined explicitly and evaluated during access reviews.


Audit & Compliance

Audit logs for:

  * Authentication attempts
  * MFA failures
  * Account lockouts
  * Role changes
  * Access review actions
* Supports traceability and compliance validation


Project Structure

```
IAM/
├── auth/
│   ├── login.py
│   └── mfa.py
├── gui/
│   ├── main.py
│   ├── ceo_dashboard.py
│   └── ciso_dashboard.py
├── governance/
│   ├── sod_rules.py
│   ├── sod_engine.py
│   └── entitlements.py
├── audit/
│   └── audit_log.json
├── data/
│   └── users.json
└── README.md
```
IAM Concepts Demonstrated

* Role-Based Access Control (RBAC)
* Entitlement-Based Access Control
* Least Privilege Enforcement
* Zero Trust Authentication
* Identity Lifecycle (JML)
* Separation of Duties (SoD)
* Just-In-Time (JIT) Access
* Access Certification & Review
* Auditability & Compliance

