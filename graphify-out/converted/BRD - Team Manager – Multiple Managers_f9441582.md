<!-- converted from BRD - Team Manager – Multiple Managers.docx -->

# Business Requirements Document (BRD)
Project: Team Manager – Multiple Managers per Team (School Context)
 Prepared By: Harsh
 Date: 15 Jan 2026

## 1. Background
The Team Manager module manages sports activities inside a school.
 Each school has:
Sports
Coaches (staff linked to sports)
Teams (linked to sports)
Managers (staff members responsible for teams)
Previously, each team allowed only one manager, creating operational bottlenecks.
 The system must now support multiple managers per team, fully managed within the school environment.

## 2. Objective
Enable multiple managers per team inside a school, allowing:
A manager to assign other managers.
A coach to assign managers to teams.
All changes to remain restricted within the same school.

## 3. Scope
### In Scope
Assign multiple managers to a team.
Managers & coaches inside the same school can add/remove managers.
Access control is limited strictly to the school context.
### Out of Scope
Cross-school team management.
Role hierarchy (Lead vs Assistant).

## 4. Stakeholders

## 5. Current Behaviour

## 6. Proposed Behaviour
A team can now have multiple managers.
### Assignment Rules



## 7. Functional Requirements
### 7.1 Team Manager Assignment

### 7.2 Permissions

## 8. UI / UX



## 9. API Behaviour

## 10. Validation Rules
User performing action must belong to the same school.
User must be coach or existing manager.
Last manager cannot be removed.

## 11. Migration
Move existing team.manager_id into school_team_managers.
All existing teams will have one manager after migration.

## 12. Acceptance Criteria
Managers & coaches inside school can assign managers.
Multiple managers can operate the same team.
Last manager removal is blocked.
All assignments are restricted to the same school.

## 13. Risks

| Role | Responsibility |
| --- | --- |
| School Admin | Overall staff access control |
| Coach | Assign managers to teams |
| Team Manager | Assign/remove managers |
| Engineering | Implementation |
| QA | Testing |
| Feature | Behaviour |
| --- | --- |
| Team Manager | Only one manager allowed |
| Assignment Rights | Only admin can assign |
| Context | All records tied to school |
| Action | Allowed By |
| --- | --- |
| Add manager to team | Existing Team Manager or Coach |
| Remove manager from team | Existing Team Manager or Coach |
| Remove last manager | ❌ Not allowed |
| ID | Requirement |
| --- | --- |
| FR-01 | A team must support multiple managers. |
| FR-02 | A team manager can assign another staff member as manager. |
| FR-03 | A coach can assign managers to teams related to their sport. |
| FR-04 | System must restrict assignment within the same school. |
| FR-05 | System must prevent removal of the last manager. |
| ID | Requirement |
| --- | --- |
| FR-06 | All assigned managers have equal rights on that team. |
| FR-07 | Managers can manage fixtures, training, attendance, reports. |
| FR-08 | Coaches can assign managers but do not automatically become managers unless assigned. |
| ID | Requirement |
| --- | --- |
| FR-09 | Team page shows list of managers. |
| FR-10 | “Add Manager” opens searchable staff dropdown (school staff only). |
| FR-11 | Remove action requires confirmation dialog. |
| Endpoint | Logic |
| --- | --- |
| POST /schools/{schoolId}/teams/{teamId}/managers | Add manager |
| DELETE /schools/{schoolId}/teams/{teamId}/managers/{userId} | Remove manager |
| GET /schools/{schoolId}/teams/{teamId} | Return managers[] |
| Risk | Mitigation |
| --- | --- |
| Unauthorized assignment | Strict school_id validation |
| Data migration errors | Backup + dry-run migration |
| UI confusion | Role-based tooltips |