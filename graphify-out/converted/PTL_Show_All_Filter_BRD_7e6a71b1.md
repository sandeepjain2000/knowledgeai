<!-- converted from PTL_Show_All_Filter_BRD.docx -->

Business Requirements Document (BRD)
# Project Title
Add 'Show All' Option to PTL Review Status Filter under Attendance Overview
# Background
Currently, within the Attendance Overview under the PTL (Permission to Leave) tab, users must switch between different review status filters such as 'Pending' and 'Approved' to view PTL records. This process requires repeated toggling between filters and makes it difficult for users to quickly see a complete list of PTL requests.
# Problem Statement
Users are required to manually switch between 'Pending' and 'Approved' status filters in order to review PTL records. This creates unnecessary navigation and reduces efficiency when monitoring PTL activities.
# Objective
Introduce a 'Show All' option within the review status multiselect filter under the PTL tab in Attendance Overview so that users can view all PTL records (Pending, Approved, Rejected, etc.) without switching between individual filters.
# Scope
In Scope:
- Add a 'Show All' option in the review status multiselect filter under the PTL tab.
- Selecting 'Show All' should display PTL records for all available review statuses.
- Ensure compatibility with existing filtering functionality.

Out of Scope:
- Changes to other modules outside the Attendance Overview PTL tab.
- Changes to PTL approval workflows.
# Functional Requirements
1. The PTL tab under Attendance Overview must include a 'Show All' option in the review status multiselect filter.
2. When 'Show All' is selected, the system must display PTL records regardless of their review status.
3. The filter should still allow users to select individual statuses if needed.
4. If 'Show All' is selected, it should override individual status selections.
5. The system should maintain existing pagination and sorting behavior.
# User Story
As a user reviewing PTL records in Attendance Overview,
I want a 'Show All' option in the review status filter,
So that I can see all PTL records without switching between Pending and Approved filters.
# Acceptance Criteria
- A 'Show All' option is visible in the review status multiselect filter under the PTL tab.
- When 'Show All' is selected, all PTL records appear in the list.
- Users can still manually filter by individual statuses.
- The feature does not impact existing filtering logic for other modules.
- The system performs without noticeable performance degradation.
# Dependencies
- Existing review status filter implementation.
- Backend API supporting multiple or no status filters.
# Assumptions
- PTL records already include a review status field.
- The backend API can support returning records across multiple statuses.