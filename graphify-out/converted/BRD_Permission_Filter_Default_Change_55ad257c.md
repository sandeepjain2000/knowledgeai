<!-- converted from BRD_Permission_Filter_Default_Change.docx -->

# Business Requirements Document (BRD)

Project: YHD -> Permission to Leave Module
Feature: Update Default Permission Filter – Leave Tab
Date: 19 Feb 2026
Prepared By: Vivek Jadhav

1. Background
In the current Leave/Permission module, the “Permission to Leave” tab defaults to the filter “Pending Year to Date.”
Users have reported that this default does not align with daily operational workflows, where the most relevant data is permissions pending for the current day.

2. Problem Statement
Users must manually change the filter from “Pending Year to Date” to “Pending Today” each time they access the Leave tab.
This creates unnecessary clicks and slows down daily processing of leave permissions.

3. Objective
Change the default filter setting in the Permission to Leave tab from:
Current: Pending Year to Date
Proposed: Pending Today
This ensures users immediately see the most relevant actionable permissions.

4. Scope
In Scope:
- Update default filter selection for Permission to Leave tab
- Apply change on initial page load, tab navigation, and page refresh
- Maintain existing filter options

Out of Scope:
- Changes to filter logic or API behavior
- UI redesign
- Other tabs or modules

5. Business Requirements
BR-01: System shall default the Permission to Leave tab filter to Pending Today
BR-02: System shall load data corresponding to today’s pending permissions on tab open
BR-03: Users shall still be able to manually change filter to other options
BR-04: System shall retain user-selected filter during session navigation (if currently supported)
BR-05: No change shall occur to other tabs’ default filters

6. Functional Requirements
- When user opens Permission to Leave tab → filter auto-selected = Pending Today
- API request parameter → filter = pending_today (or equivalent existing value)
- UI label remains unchanged
- Existing filters available in dropdown

7. User Story
As a staff member managing student permissions
I want the Permission to Leave tab to show permissions pending today by default
So that I can immediately process today’s requests without changing filters

8. Acceptance Criteria
- Default filter = Pending Today on first load
- Data displayed = only today’s pending permissions
- Changing filter works as before
- Refreshing page keeps Pending Today as default
- No regression in other filters

9. Impact Analysis
Users impacted: Admin staff, House staff, Leave/Detention managers
Systems impacted: Leave/Permission UI, Filter default state logic
Risk: Low (configuration/default change only)

10. Assumptions
- “Pending Today” filter already exists
- Backend supports today filter parameter
- No reporting dependency on default filter

11. Success Metrics
- Reduced filter change actions per session
- Faster permission processing time
- Positive user feedback
