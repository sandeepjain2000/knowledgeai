<!-- converted from Shop - Allow multiple payments.docx -->

# Business Requirements Document (BRD)
## 1. Purpose
The purpose of this document is to define the business requirements for the Multi‑Payment Feature, which allows parents to make multiple payments against the same shop item while enabling schools to track payment progress, statuses, and related orders clearly and consistently.

## 2. Background & Problem Statement
Currently, the system supports single payment flows. Schools require the ability to allow parents to pay for the same item multiple times while maintaining:
- Clear visibility of payment progress
- Accurate order records for each payment
- Controlled closure of payments by schools

## 3. Scope
### In Scope
- Multi‑payment handling for a single shop item
- Status lifecycle for multi‑payments
- Order number generation per payment
- UI indicators and tooltips for payment status
- Parent warning prompt for repeat payments
## 4. Actors / Stakeholders
- Parent: Makes one or more payments for the same item
- School / Admin: Creates items, monitors payment status, closes payments
- System: Manages statuses, order records, and validations

## 5. Functional Requirements
### 5.1 Payment Status Lifecycle
Rules:

- There will be a checkbox in shop add/edit form “Allow multiple payments”
- “Allow multiple payments” will only be available for standard item type and full payment type
- Status initially starts as Unpaid
- On first successful payment: Unpaid → Ongoing
- Once full payment requirements are met: Ongoing → Paid
- If no payment is ever made, status remains Unpaid
- When the item is unpublished by the school:
- If at least one payment exists: Ongoing → Paid
- If no payments exist: status remains Unpaid
- If one or more orders are refunded while others remain valid, status becomes Partially Refunded
- Status remains Ongoing until it is either marked Paid, Cancelled, or unpublished by the school

### 5.2 Status Tooltip (Hover Information)
On hover over the payment status, the system should display an informational tooltip explaining the status meaning:
- Ongoing
Open payment. Parents can pay multiple times until closed by the school.
- Paid
Payment completed. No further payments are required.
- Unpaid
No payments have been made yet. Full balance is outstanding.
- Partially Refunded
One or more payments were refunded. Remaining paid amount is retained.
Additional status descriptions may be added in the future if required.

### 5.3 Order Generation
- An order number must be generated every time a parent makes a payment
- Each payment results in a separate order record in Orders
- Existing Orders logic remains unchanged
- Multiple order numbers must be displayed against the same item record
Example:
Order Numbers: 1010, 1011, 1012

### 5.4 Parent Warning Prompt
If a parent attempts to pay again for the same item:
System Prompt:
“You have already paid for this item. Are you sure you want to pay again?”
- Parent must explicitly confirm before proceeding

## 6. Business Rules
- Multiple payments are allowed only while status is Ongoing
- Unpaid items must contribute to the outstanding balance shown in the Find Student portal
- Paid items must not contribute to the outstanding balance
- Ongoing items must not contribute to the outstanding balance
- Unpublishing an item:
- Marks Ongoing → Paid for users who have paid
- Leaves status as Unpaid for users who have not paid
- Once status is Paid, no further payments are allowed
- Refunding a single order does not invalidate other completed orders
- If at least one order is refunded and others remain successful, status becomes Partially Refunded
- Each payment must be traceable via a unique order number
- Status visibility and clarity is mandatory for schools


## 8. Assumptions & Dependencies
- Schools manually control when a payment is closed/unpublished
- Parent payments are not automatically scheduled

## 9. Acceptance Criteria
- Status transitions occur exactly as defined
- Multiple orders are created for multiple payments on the same item
- Tooltips display correct status explanations
- Parent warning prompt appears on repeat payments
- Existing Orders functionality remains unaffected

| Stage | Description |
| --- | --- |
| Unpaid | Default status when students are added to a payment and no payment has been made. Remains Unpaid if no payments are ever made. |
| Ongoing | Status after at least one successful payment. Allows multiple payments until closed by the school. |
| Paid | All required payments completed and payment is considered fully settled. |
| Partially Refunded | One or more orders have been refunded, but at least one successful payment still exists. |
| Refunded | All orders have been reunfded |