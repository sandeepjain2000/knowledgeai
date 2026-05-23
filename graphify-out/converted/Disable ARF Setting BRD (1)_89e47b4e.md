<!-- converted from Disable ARF Setting BRD (1).docx -->

Business Requirement Document: Disable ARF Setting
Introduction Disable Absent Notifications: Use this option to temporarily turn off absent notifications for selected dates and specific year groups or classes. When enabled, parents will not receive any absence messages during the chosen period.
This is especially useful during exam weeks, or any time when you do not want absence notifications to be sent out automatically.
This document outlines the business requirements for this feature, ensuring it integrates with the centralized cron jobs for Tyro and Wonde to strictly suppress ARF generation based on these configurations.
Objective To provide a mechanism for authorized school personnel (Principal/Deputy Principal and users with Attendance/Absentee module access) to configure "blocked dates" or "blocked groups" (Year/Class) for ARF generation. The system must strictly enforce these rules across all automated ARF generation pipelines (Tyro and Wonde) to prevent accidental notifications to parents.
Scope In Scope:
Configuration UI: A settings interface in the Dashboard to View, Add, and Delete "Disable ARF" rules.
Granularity: Blocking by Date(s), Whole School, Specific Year Groups, or Specific Classes.
Backend Enforcement (Dashboard): Node.js API to manage the yii_arf_disabled_dates table.
Backend Enforcement (Tyro): Node.js Cron integration (
arfGeneration,
syncArfFromSession) to check rules.
Backend Enforcement (Wonde): PHP/Laravel Console Command (ArfGenerationTraits) to check rules.
Handling Existing Records: Logic to "Skip" or "Ignore" pending attendance records that match a disable rule.
Out of Scope:
Manual ARF creation bypass (this controls automated generation only).
Actors & Roles
School Admin (Principal/Deputy Principal/Attendance Officer): Configures the settings.
System (Tyro Node Backend): Enforces rules for Tyro schools.
System (Wonde PHP Backend): Enforces rules for Wonde schools.
Parent/Guardian: Indirectly affected (does not receive notifications for disabled dates).
Functional Requirements 5.1 Inputs
Date Range: Start and End Date for the disable rule.
Target Audience: Whole School, Specific Year(s), or Specific Class(es).
School Context: The rule applies only to the authenticated school.
5.2 Validation Rules
Date Validity: Start Date cannot be after End Date.
Conflict Checks: Prevent duplicate rules for the same target on the same date.
Access Control: User must have permission to access the Attendance Settings.
5.3 Business Logic & Processing
Rule Storage: All rules are stored in yii_arf_disabled_dates.
Tyro Integration (Node.js):
arfGeneration cron: Checks yii_arf_disabled_dates. If a student matches:
Marks the staging record as SKIPPED (Status 3).
Does not create an ARF.
syncArfFromSession cron: Checks rules. If disabled:
Inserts a "Ghost ARF" with request_form = SKIPPED (Status 3) into yii_absence_import_data to prevent future re-processing.
Wonde Integration (PHP):
ArfGenerationTraits: Checks ArfDisabledDates::isARFDisabled. If disabled:
Marks the staging record (wondes_session_attendance_data) as SKIPPED (Status 3).
Logs the skip action and continues to the next student.
5.4 Error Handling
Frontend: Clear alerts providing detailed feedback on success/failure of rule creation.
Backend: Graceful handling of DB connection issues; Cron jobs log "Skipped due to Disable Rule" for audit purposes.
Data Requirements
Configuration Table: yii_arf_disabled_dates
Tyro Staging: yii_tyro_session_attendance_data (Uses Status 3 for Skipped).
Wonde Staging: wondes_session_attendance_data (Uses Status 3 for Skipped).
ARF Table: yii_absence_import_data (Uses request_form = 3 or similar flag for skipped records).
Security & Permissions
Configuration Access: Restricted to authorized users (Principal/Admin).
Data Isolation: Rules are strictly scoped to school_id.
