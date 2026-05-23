<!-- converted from BRD_Not_Signed_Out_List_Update.docx -->

Business Requirements Document (BRD)
# Document Information
Project Name: Student Sign-In/Out Management
Feature: Not Signed Out List Enhancement
Prepared For: Development Team
Prepared By: ChatGPT
Date: March 6, 2026
# 1. Background
Currently, the 'Not Signed Out' list only displays students whose PTL (Permission to Leave) status is Approved.
However, students who have created a PTL request but whose status is still Pending are not included in this list.
This causes inaccurate tracking of students who are still outside or have not completed the sign-out process.
# 2. Business Problem
The system only considers Approved PTL requests when generating the 'Not Signed Out' list.
As a result, students with Pending PTL status who have not signed out are not visible in the list.
This can lead to incomplete monitoring and operational confusion for administrators or wardens.
# 3. Business Objective
Enhance the 'Not Signed Out' list to include PTL requests with Pending status in addition to Approved status,
so administrators can track all students who have not yet signed out regardless of approval status.
# 4. Scope
In Scope:
- Update the logic of the 'Not Signed Out' list.
- Include PTL records with status = Pending.
- Continue showing PTL records with status = Approved.

Out of Scope:
- Any change to PTL approval workflow.
- Changes to PTL creation or editing functionality.
# 5. Functional Requirements
FR1: The system shall display students in the 'Not Signed Out' list if their PTL status is Approved.
FR2: The system shall also display students in the 'Not Signed Out' list if their PTL status is Pending.
FR3: The list should continue to exclude PTL records with status Rejected or Cancelled.
FR4: The system should maintain current filters, pagination, and sorting behavior.
# 6. Acceptance Criteria
1. When a student has an Approved PTL and has not signed out, they appear in the 'Not Signed Out' list.
2. When a student has a Pending PTL and has not signed out, they also appear in the list.
3. PTL requests with Rejected status should not appear.
4. The list should update correctly without affecting other modules.
# 7. Impacted Modules
- Student Sign-In/Out Module
- PTL (Permission to Leave) Module
- Dashboard / Tracking Views
# 8. Assumptions
- PTL statuses include Approved, Pending, Rejected, and possibly others.
- Existing UI for the 'Not Signed Out' list will remain unchanged.
- Only backend filtering logic requires modification.
# 9. Risks
- Incorrect filtering logic may lead to duplicate or incorrect entries.
- Any changes in PTL status definitions may affect the functionality in future.