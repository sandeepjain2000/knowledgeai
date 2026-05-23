<!-- converted from BRD-Web Ticketing System (1).docx -->

# WEB TICKETING SYSTEM
# BUSINESS REQUIREMENTS DOCUMENT (BRD)`
Version: 1.0
 Prepared By: Product & Architecture Team
 Date: 12-02-2026
# 1. DOCUMENT OVERVIEW
## 1.1 Purpose
This Business Requirements Document (BRD) defines the business objectives, functional requirements, operational workflows, constraints, and non-functional expectations for the Web Ticketing System.
The document serves as the single authoritative source of business requirements and defines what the system must achieve from a business perspective. It does not describe technical implementation details.

## 1.2 Scope
The Web Ticketing System will:
Enable schools (clients) to submit structured website change requests.
Allow internal teams to manage, assign, track, review, and complete requests.
Support multi-school data isolation.
Provide SLA tracking and reporting.
Enable structured communication between client and internal teams.
Provide auditability and transparency of request lifecycle.

## 1.3 Out of Scope
The following are not covered within this document:
Technical architecture decisions
Database schema definitions
Authentication implementation details
Infrastructure and hosting design
UI styling specifications (colors, fonts, layout)
Code-level constraints or technology stack decisions

## 1.4 Definitions & Terminology

# 2. BUSINESS OBJECTIVES
The Web Ticketing System aims to:
Centralize all website change requests into a structured platform.
Eliminate email-based request management.
Improve transparency between schools and the web team.
Provide measurable SLA tracking.
Enable reporting on workload and performance.
Improve accountability through assignment and audit tracking.
Standardize request lifecycle and approval flow.
## 2.1 Success Criteria
The success of the Web Ticketing System shall be measured by:
Reduction in email-based change requests by at least 80%
100% of website changes logged through the system
SLA compliance visibility across all schools
Reduction in request turnaround time
Clear assignment accountability for every ticket
Measurable reporting for management decision-making

# 3. STAKEHOLDERS

# 4. USER ROLES & ACCESS LEVELS
## 4.1 Client
Clients shall be able to:
Create tickets
Save tickets as draft
Submit tickets
Add request items
Upload attachments
View their own tickets
Reply to tickets
Reopen completed tickets
View ticket status
Clients shall not be able to:
Assign developers
View internal notes
View internal priority
View internal links
Modify SLA values

## 4.2 Admin
Admins shall be able to:
View all tickets within their school
Assign and reassign developers
Change ticket status
Set ticket priority
Request additional information
Approve or reject reopen requests
Send tickets for peer review
View SLA breaches
Generate reports

## 4.3 Developer
Developers shall be able to:
View assigned tickets
Update ticket status
Mark request items complete
Add internal notes
Reply to clients
Reopen tickets (if needed)
Developers shall not be able to:
Assign tickets to themselves
Access tickets from other schools

## 4.4 Reviewer
Reviewers shall be able to:
Review assigned tickets
Provide feedback at request item level
Mark items as reviewed
Reviewer feedback is informational and does not block completion.
## 4.5 Role Boundaries & Data Ownership
Each user belongs to exactly one school.
Users shall only access tickets belonging to their school.
Admin users operate only within their assigned school.
Clients may access only tickets they created.
Developers may access all tickets as well as tickets assigned to them.
Reviewers may access all tickets as well as tickets assigned for review.
Management access (if enabled) shall be read-only.

# 5. SYSTEM OVERVIEW
(Insert High-Level System Context Diagram Here)
The system supports multiple schools operating independently. Each school’s users can only access data belonging to their organization.
Tickets serve as containers that may include multiple request items.
Each ticket follows a structured lifecycle.
The system enforces strict school-level data isolation to ensure no cross-school data visibility.

# 6. FUNCTIONAL REQUIREMENTS
FR-1: Ticket Creation & Submission
## FR-1.1 Create Ticket
The system shall allow a Client to create a new ticket.
### FR-1.1.1 Ticket Header Information
The ticket shall capture:
Title (mandatory)
Priority flag (optional)
Auto-generated reference number (generated only upon submission)
Creation date (system generated)
Requester identity (system derived)
### FR-1.1.2 Validation Rules
Title must be between defined character limits.
Ticket must contain at least one request item before submission.
Ticket cannot be submitted if required fields are incomplete.

## FR-1.2 Request Item Creation
Each ticket shall support multiple request items.
### FR-1.2.1 Request Item Attributes
Each request item shall include:
Request type (mandatory)
Title (mandatory)
Description (mandatory)
Optional page URL
Optional attachments
### FR-1.2.2 Item Numbering
Each item shall have a unique sequence number within the ticket.
Item numbering shall be auto-generated and incremental.

## FR-1.3 Ticket Submission
Upon submission:
The system shall generate a unique reference number.
The ticket status shall change from Draft to New.
Submission date shall be recorded.
Notification shall be sent to Admin users of the same school.

# FR-2: Draft Management
## FR-2.1 Save as Draft
Clients shall be able to save tickets without submitting.
Drafts shall not generate reference numbers.
Drafts shall not be visible to internal users.
## FR-2.2 Draft Editing
Clients may edit draft tickets indefinitely until submission.
Draft validation rules shall apply only upon submission.

# FR-3: Ticket Lifecycle Management
The system shall enforce a structured lifecycle.
The ticket lifecycle ensures:
Structured progression of work
Clear ownership at every stage
Transparent communication
Prevented accidental completion
Controlled reopen behavior
Full audit traceability
Lifecycle states cannot be bypassed or skipped unless authorized by Admin override.

## FR-3.1 Lifecycle States
The system shall support:
Draft
New
In Progress
Info Needed
Peer Review
Completed
Reopened
(Insert Lifecycle State Diagram Here)

## FR-3.2 State Transitions
The system shall allow only predefined state transitions.

Triggered by Client submission.

Triggered by Admin starting work.

Triggered when clarification required from Client.

Triggered after clarification received and manually cleared.

Triggered when ticket sent for review.

Completion is allowed only when all request items are completed AND (if reviewers assigned) all items reviewed.

Triggered by Client, Admin, or Developer.

Triggered after Admin approval.

Triggered if Admin rejects reopen request.
### FR-3.2.10 Transition Guard Rules
The system shall enforce the following guard conditions:
A ticket cannot move to Completed unless all request items are completed.
If reviewers are assigned, all items must be reviewed before completion.
A Draft cannot transition directly to In Progress.
A Completed ticket cannot transition directly to New.
Reopened tickets must receive Admin decision before work resumes.
Status changes must be recorded in history

# FR-4: Assignment Management
## FR-4.1 Developer Assignment
Tickets shall be assigned at ticket level only.
Only one developer may be assigned per ticket.
Assignment shall be performed by Admin.
Assignment date shall be recorded.
### FR-4.1.1 Assignment Accountability
Every submitted ticket must have clear ownership.
A ticket without assignment shall be considered unallocated.
Management reporting shall identify unassigned tickets.
Assignment timestamp shall be recorded for SLA accountability.
## FR-4.2 Reassignment
Admin may reassign tickets.
Previous assignment shall remain historically traceable.
## FR-4.3 Assignment Restrictions
Developer must belong to same school.
Developer must have Developer role.
Developers shall not self-assign.

# FR-5: Request Item Management
## FR-5.1 Item Completion
Each request item shall be independently marked complete.
Completion shall record timestamp and user identity.
### FR-5.1.1 Definition of Completion
A request item shall be considered completed when:
Work has been implemented.
Internal verification has been performed.
Completion timestamp has been recorded.
Completion does not automatically imply ticket closure unless all items satisfy completion rules.
## FR-5.2 Item Modification Rules
Request type cannot be modified after submission.
Description updates shall be allowed.
Items cannot be physically deleted after submission.
Items may be deactivated if required.

# FR-6: Peer Review Management
## FR-6.1 Reviewer Assignment
Multiple reviewers may be assigned to a ticket.
Reviewers must belong to same school.
Assigned developer cannot act as reviewer.
### FR-6.1.1 Review Governance
Peer review is optional.
However, if reviewers are assigned to a ticket:
Completion eligibility requires all assigned reviewers to review all items.
Review feedback is advisory and does not prevent closure unless Admin intervenes.

## FR-6.2 Item-Level Review
Each reviewer shall:
Review each request item.
Mark item as reviewed.
Provide optional feedback:
Positive
Neutral
Needs Attention

## FR-6.3 Completion Eligibility
The system shall determine ticket eligibility for completion only when:
All items are marked complete
AND if reviewers assigned, all items are reviewed
Reviewer feedback shall be informational only.

# FR-7: Reopen Workflow
## FR-7.1 Reopen Request
Completed tickets may be reopened.
Reopen shall change status to Reopened.
Notification shall be sent to Admin.
### FR-7.1.1 Reopen Intent
Reopen functionality exists to:
Address missed changes
Correct implementation issues
Continue work related to original scope
Rejected reopen requests require submission of a new ticket to preserve audit clarity.
## FR-7.2 Reopen Decision
Admin shall:


Reopen rejection shall notify the Client.

# FR-8: Messaging & Communication
## FR-8.1 Client Communication
Clients shall be able to post messages on tickets.
Clients shall see only non-internal messages.
## FR-8.2 Internal Notes
Internal users may post internal-only notes.
Internal notes shall not be visible to Clients.
## FR-8.3 Completion Reply Behavior
If Client replies after ticket completion, system shall trigger reopen process.

# FR-9: Attachment Handling
## FR-9.1 Upload Capability
Users may upload attachments during ticket creation or messaging.
Attachments may relate to ticket, request item, or message.
## FR-9.2 File Restrictions
File size limits shall apply.
Allowed file types shall be restricted.
Total ticket attachment size may be capped.
### FR-9.2.1 Attachment Governance
Attachments must belong to a specific ticket context.
Attachments cannot exist independently.
Attachments may not be permanently deleted after submission.
Attachment visibility follows ticket-level access control.
## FR-9.3 Security
Files shall be securely stored.
Files shall be downloadable only by authorized users.

# FR-10: SLA Management
## FR-10.1 SLA Definition
SLA shall be defined per request type.
SLA may vary by school.
### FR-10.1.1 SLA Measurement Logic
SLA represents the expected resolution time for a request item.
SLA measurement:
Starts when ticket moves to In Progress.
Is calculated per request item.
Continues running during Info Needed status.
Stops when item is marked complete.
SLA performance shall be measurable for reporting purposes.
## FR-10.2 SLA Start Trigger
SLA shall begin when ticket moves to In Progress.
## FR-10.3 SLA Continuity
SLA shall continue running during Info Needed state.
## FR-10.4 SLA Breach
System shall flag breached items.
Notifications may be sent upon breach.

# FR-11: Notifications
## FR-11.1 Event Notifications
System shall generate notifications for:
Ticket submission
Assignment
Status change
Info Needed
Peer Review request
Completion
Reopen
SLA breach
### FR-11.1.1 Notification Governance
Notifications shall:
Be event-driven.
Respect user notification preferences.
Be visible in-app.
Be optionally sent via email.
Be logged for audit purposes.
## FR-11.2 Notification Channels
In-app notifications
Email notifications
Users may configure preferences where applicable.

# 7. NON-FUNCTIONAL REQUIREMENTS
## 7.1 Security
Role-based access control
School-level data isolation
Audit logging of critical actions
## 7.2 Performance
Ticket list should load within acceptable enterprise standards.
SLA detection must operate reliably.
## 7.3 Availability
System expected to support business-hour availability.
## 7.4 Auditability
Status changes must be recorded.
Assignment changes must be recorded.
Reopen actions must be logged.
## 7.5 Data Retention
Tickets shall not be physically deleted.
Historical data shall be retained for minimum of 3 years.
Audit logs shall be retained for compliance review.

## 7.6 Scalability
The system shall support:
Multiple schools operating concurrently.
Concurrent ticket creation.
Enterprise-grade user load.

# 8. BUSINESS RULES
One developer per ticket (Phase 1).
Peer review is optional but mandatory if reviewers are assigned.
No physical deletion of submitted records.
Draft status is separate from lifecycle states.
Multi-school isolation enforced.
Item completion is determined by completion timestamp and not by status flag.
A ticket is considered eligible for completion only when all request items are completed and (if reviewers are assigned) all review conditions are satisfied.
Reopen requires administrative control.

# 9. ASSUMPTIONS & CONSTRAINTS
Phase 1 does not support multi-developer assignment.
No cross-school administrative visibility.
No item-level assignment in Phase 1.
Peer review is informational only.
Academic year logic for reference number generation is handled at application layer.

# 10. GOVERNANCE & CONTROL
All lifecycle transitions must be auditable.
All assignment changes must be recorded.
Reopen decisions must be documented.
Role changes must be controlled.
Business rule violations must be prevented through system validation.

# 11. Reporting
The system shall provide reporting capability for:
Tickets by status
Tickets by priority
Tickets per school
Resolution time metrics
SLA breach count
Developer workload
Reopen frequency
Reports shall support date range filtering.

# 12. FUTURE ENHANCEMENTS (OPTIONAL)
Multi-developer assignment
Item-level assignment
Mandatory approval-based review
Cross-school administrative roles

# 13. ACCEPTANCE CRITERIA
Each functional requirement shall be validated against:
Role-based access behavior
Correct lifecycle enforcement
Correct SLA calculation
Correct notification triggering
Proper audit logging
School-level isolation enforcement
System acceptance requires validation of all defined functional and non-functional requirements.

# 14. APPROVALS


| Term | Definition |
| --- | --- |
| School | A client organization using the system |
| Ticket | A container representing a website change request |
| Request Item | An individual change within a ticket |
| Client | School user submitting tickets |
| Admin | Internal user managing tickets |
| Developer | Internal user assigned to execute work |
| Reviewer | Internal user providing peer review feedback |
| SLA | Service Level Agreement target time |
| Draft | Unsubmitted ticket visible only to client |
| Info Needed | Status indicating clarification required from client |
| Reopened | Status when completed ticket is reopened |
| Stakeholder | Role |
| --- | --- |
| School Clients | Submit and track website requests |
| Web Team Developers | Execute assigned changes |
| Internal Admin Team | Manage lifecycle and assignments |
| Reviewers | Provide quality validation |
| Management | Monitor reports and performance |
| Role | Name | Signature | Date |
| --- | --- | --- | --- |
| Product Manager |  |  |  |
| Technical Lead |  |  |  |
| Project Manager |  |  |  |