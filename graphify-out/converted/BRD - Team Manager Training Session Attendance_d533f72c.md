<!-- converted from BRD - Team Manager Training Session Attendance.docx -->

# Business Requirements Document (BRD)
## Project Name
Team Manager – Training Session Attendance

## 1. Purpose
The purpose of this document is to define the business requirements for implementing a robust Training Session Attendance Management System within the Team Manager platform. This module will enable coaches and team managers to record attendance of players for each training session and send Private Notifications (PN) to students based on attendance outcomes.

## 2. Background
The Team Manager platform currently manages:
Sports
Teams under each sport
Fixtures
Training sessions for teams within date ranges
Students enrolled as players in teams
Training sessions are scheduled for specific date ranges at fixed times. Players may or may not attend each session. However, there is currently no structured mechanism to:
Track attendance for each player per session
Categorize attendance (Present / Absent / Excused)
Send attendance-based PN messages manually
This module aims to fill this operational gap.

## 3. Objectives
Enable session-wise attendance tracking for all players in a team.
Support attendance statuses: Present, Absent, Excused.
Allow authorized staff (coach or team manager) to mark attendance.
Allow manual sending of PN messages using attendance-specific PN templates.
Maintain historical audit logs for attendance and PN activity.

## 4. Scope
### In Scope
Attendance management for training sessions.
Player attendance statuses.
Role-based access for coaches and team managers.
PN template integration for attendance.
Manual PN dispatch.
Reporting & audit logging.
### Out of Scope
Automated PN triggers (future phase).
Attendance for fixtures/matches.
Biometric or third-party attendance systems.

## 5. Stakeholders

## 6. User Roles & Permissions

## 7. Functional Requirements
### 7.1 Training Session Attendance

### 7.2 PN Template Management

### 7.3 Sending Private Notifications (PN)

### 7.4 Audit & Reporting

## 8. Non-Functional Requirements

## 9. Business Rules

## 10. Success Metrics

## 11. Risks & Mitigations

## 12. Dependencies
PN Template module
Team & Training Session Management modules
Role-Based Access Control (RBAC) system

| Role | Responsibility |
| --- | --- |
| School Admin | Configure PN templates |
| Coach | Mark attendance for sport teams |
| Team Manager | Mark attendance for managed teams |
| System Admin | Maintain access control & audit logs |
| Role | Permissions |
| --- | --- |
| Coach | View assigned teams, mark attendance, send PN |
| Team Manager | View managed teams, mark attendance, send PN |
| School Admin | Create/edit PN templates |
| System Admin | Full system access |
| ID | Requirement |
| --- | --- |
| FR-01 | System shall display all training sessions for a team by date. |
| FR-02 | System shall list all registered players for the selected session. |
| FR-03 | Default attendance state shall be Excused. |
| FR-04 | Users can mark each player as Present, Absent, or Excused. |
| FR-05 | Bulk attendance update shall be supported. |
| FR-06 | Attendance can be updated multiple times before session is locked. |
| ID | Requirement |
| --- | --- |
| FR-07 | System shall allow School Admin to create PN templates specific to attendance. |
| FR-08 | Templates shall support placeholders (student name, team name, session date). |
| ID | Requirement |
| --- | --- |
| FR-09 | Users can manually send PN for selected students. |
| FR-10 | Only templates tagged as “Attendance” shall be selectable. |
| FR-11 | PN sending shall log sender, timestamp, session ID, and template ID. |
| ID | Requirement |
| --- | --- |
| FR-12 | System shall store historical attendance data. |
| FR-13 | System shall track PN history for each player. |
| FR-14 | Attendance change history shall be logged. |
| Category | Requirement |
| --- | --- |
| Performance | Attendance page must load within 3 seconds for 100+ players. |
| Security | Only authorized roles can modify attendance. |
| Usability | UI must support bulk actions and mobile-friendly layout. |
| Reliability | Attendance updates must be transactional and idempotent. |
| Rule ID | Description |
| --- | --- |
| BR-01 | Attendance can only be taken for scheduled training sessions. |
| BR-02 | PN cannot be sent unless an Attendance PN Template exists. |
| BR-03 | Only coaches of the sport or managers of the team can mark attendance. |
| BR-04 | Default attendance state is Excused until updated. |
| Metric | Target |
| --- | --- |
| Attendance Completion Rate | ≥ 95% of sessions recorded |
| PN Usage Adoption | ≥ 70% of attendance PN used within 3 months |
| Error Rate | < 1% data inconsistency |
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Users forget to mark attendance | High | Dashboard reminders |
| PN template misconfiguration | Medium | Validation and preview |
| Unauthorized access | High | Strict RBAC |