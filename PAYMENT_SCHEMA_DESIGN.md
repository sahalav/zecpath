# Payment Schema Design

## Objective

Design a payment and subscription management system for the Zecpath hiring platform.

## Database Entities

### SubscriptionPlan

Stores available subscription plans.

Fields:

* id
* name
* price
* duration_days
* max_job_posts
* description

### UserSubscription

Stores user subscription details.

Fields:

* id
* user
* plan
* start_date
* end_date
* is_active

### PaymentTransaction

Stores payment transaction information.

Fields:

* id
* user
* amount
* payment_id
* status
* created_at

### BillingHistory

Stores billing and invoice records.

Fields:

* id
* user
* transaction
* invoice_number
* generated_at

## Entity Relationship

User
│
├── UserSubscription
│         │
│         └── SubscriptionPlan
│
├── PaymentTransaction
│
└── BillingHistory
