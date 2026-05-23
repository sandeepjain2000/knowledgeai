<!-- converted from BRD- PTL Multi-Student & Multi-Day Support.docx -->

Business Requirement Document
PTL Multi-Student & Multi-Day Support
1. Introduction
Multi-Student & Multi-Day PTL Support: This feature enhances the Permission to Leave (PTL) system to allow authorized staff to create leave requests for multiple students simultaneously and for durations spanning multiple days.
This is especially useful for boarding schools (e.g., Cistercian College) where groups of students may leave for weekends or events, and manually entering single requests for each student/day is inefficient.
This document outlines the business requirements for this feature, ensuring it integrates with the existing PTL module, enforcing strict validation against absenteeism records to maintain data integrity.
2. Objective
To provide a mechanism for school staff to efficiently manage bulk PTL entries. The system must strictly enforce absentee checks for every selected student across the entire date range to prevent conflicting attendance records.
3. Scope
In Scope:
Web Dashboard UI: Enhanced "Add PTL" sidesheet to support multi-student selection and date ranges.
• Backend Processing: API updates to handle arrays of student IDs (vswareIds) and multi-day logic
• Validation Logic: Strict server-side validation to block PTL creation if any selected student is already marked absent for the requested dates.
Data Storage: Creation of individual yii_permission_to_leave records for each student/date combination.
Out of Scope:
• Mobile App implementation (handled separately).
4. Actors & Roles

5. Functional Requirements
## 5.1 Inputs
- Students: List of vswareIds (Array of Integers).
- Date Range: fromTime and toTime (DateTime strings).
- Reason: reasonId (Integer) and reason text.
- Details: furtherInformation (String, max 500 chars).
- Context: yearId, classId (derived from selection).
## 5.2 Validation Rules
- Mandatory Fields: Student selection, Date Range, Reason.
- Date Order: fromTime must be before toTime.
- Absentee Conflict (CRITICAL): For every selected student, the system MUST check yii_absentee for the requested date range.
- Rule: If a student is marked absent (Status: AVAILABLE or NOT_IN_CLASS) on any of the selected dates, the ENTIRE request for that student must fail/be blocked.
- Time Limit: fromTime and toTime must be within the same day for single-day updates (Backend validation).
## 5.3 Business Logic & Processing
Rule Storage: PTL records are stored in yii_permission_to_leave.
- Processing Flow (Node.js addEditMultidayLeavePermission):
- Iterate Students: Loop through each provided vswareId.
- Date Parsing: Generate a list of all dates between fromTime and toTime.
- Conflict Check (Dynamic):
- Query yii_absentee for the specific student and date range.
- If absent: Throw Error ("Leave permission cannot be added as the student is marked absent on all selected dates.").
- Record Creation:
- If valid: Create a yii_permission_to_leave record for each date in the range (splitting multi-day into daily records).
- Set noteStatus = 1 (Confirmed).
- Set isWriteback = TO_BE_DONE.
- Save: Commit records to the database.
## 5.4 Error Handling
- Frontend: Display specific error messages returned by the API (e.g., "Student X is marked absent...").
- Backend: Atomic checks per student loop. If validation fails for a student, their records are not created.
6. Data Requirements
- Primary Table: yii_permission_to_leave (New rows per student/day).
- Reference Table: yii_absentee (Read-only for conflict checks).
- Audit Fields: addedBy (User ID), addedFrom (WEB).
7. Security & Permissions
- Access Control: Restricted to users with canAccessModule.leavePermission.
- Data Scope: All queries filtered by req.user.schoolId.
8. Non-Functional Requirements
- Performance: Bulk processing (e.g., 50 students) should complete in under 2 seconds.
- Scalability: Efficient handling of Promise.all for multiple database inserts.
9. Success Metrics
- Efficiency: Reduction in time spent entering PTLs for sports teams/boarding weekends.
- Data Integrity: Zero conflicting PTL/Absentee records created.
| Actor | Role/Responsibility |
| --- | --- |
| School Staff (Year Head/Admin) | Initiates the bulk PTL request. |
| System (Node.js Backend) | Validates the request, checks for absentee conflicts, and creates records. |
| Parent/Guardian | View-only access to the created PTLs via their app. |