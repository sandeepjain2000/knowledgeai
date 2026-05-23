<!-- converted from Business_Requirements_Document_(BRD)_for_Teams_Manager_Application_23Feb_(1).docx -->


# Business Requirements Document (BRD) for Teams Manager Application

## 1. Introduction
The Teams Manager application is designed for schools and colleges to efficiently manage sports teams, fixtures, training schedules, results, and team member roles. The system provides a centralized platform for team administration, allowing staff members, coaches, and students to interact seamlessly.

## 2. Business Objectives
Provide an intuitive web-based platform for managing sports teams.
Streamline team creation, player assignment, and fixture scheduling.
Enable real-time tracking of match results and team performance.
Support integration with the existing school CMS for staff and student data.
Facilitate communication via notifications and social media integration.
Provide data export capabilities for all tabular data.
Incorporate advanced filtering, sorting, and search functionalities for efficient data retrieval.
Generate monetisation opportunities through virtual sponsorships, branded event elements, and custom ads.

## 3. Scope
The Teams Manager application will include the following key features:
Sports Management: Define and manage sports (with configuration fields such as active status, icons, default team size, number of substitutes, individual sport flag, coach name, number of teams, and notes) as a prerequisite for team creation.
Team Management: Create, edit, and deactivate teams; assign staff in charge (including roles such as Manager, Chef d’Equipe, and Manager child(ren)); manage team rosters with fields like Created date, Active flag, Team name, Type, Members, Next training, and Next fixture.
Fixture Management: Schedule, edit, and track match fixtures. Support home/away game types, playing team selection (with role assignment such as Goalkeeper, Striker, Midfielder for soccer; Bowler, Batsman, Wicketkeeper for cricket), match reports, and a points system.
Training Management: Create recurring and one-time training sessions, track attendance, and confirm player availability.
Player Management: Assign players to teams with specific roles and track individual performance and match history.
Results & Statistics: Record and analyze match results using a point-based system, and generate performance reports.
Social Media Integration: Allow customizable templates for posting content (e.g., virtual sponsorship logos on jerseys, branded event badges, custom ads on fixtures, and sponsored pop-ups) and include sponsor logos in social shares.
User Roles & Permissions: Define roles for teachers, coaches, students, external coaches, and super admins.
Dashboard: Provide an overview of key metrics, including upcoming fixtures, training sessions, recent results, leaderboards, notifications.
News Module Integration: Display news content from the CMS News module within the sports manager application.
Mobile App Support: Extend the existing mobile application for parents with dedicated sports screens.

## 4. User Roles & Permissions
Administrator: Full access to all modules.
Coaches/Staff In Charge: Manage teams, schedule fixtures, record results, and send notifications/invites.
Students/Players: View schedules, match results, training sessions, and communicate with coaches.
External Coaches: Limited access for coaching assignments.
Super Admin: Responsible for setting up schools, sports, and managing system-wide configurations (including monetisation and reporting).

## 5. Screens and Corresponding Contents
UI Guidelines -
- Date- dd-mm-yy and wherever possible day, dd-mm-yy.

### Dashboard
Components:
Overview Panel: Key team statistics (total points, wins, losses) and Total Active Players.
Upcoming Events: Fixtures and training sessions.
Recent Results Summary: Latest match outcomes and points standings.
Leaderboards: Top teams and players.
Notification Panel: Reminders for fixtures (e.g., eve-of-match reminders set by coaches), announcements, and social media post updates.
Filters/Sorting: Options to sort data by date, team, sport, or points.
### Sports Management Screen (Admin & Super Admin)
Summary at the top:
Number Of Sports
Number of coaches
Etc.
Fields/Columns:
Active: Status indicator (active/inactive).
Sports: Sport name (e.g., Cricket, Soccer, Rugby).
Icon: Visual icon representing the sport.
Number on Team: Default number of players on the team.
Number Subs: Default number of substitutes.
Individual: Flag indicating if it is an individual sport.
Coach Name: Default coach (can be pre-populated from the school CMS).
No Of Teams: Number of teams participating in that sport.
Notes: Additional configuration or remarks.
Common UI Elements:
Filters: Filter by sport name, active status.
Sorting: Sort alphabetically or by number of teams.
Export Data: Option to export sports data.
Search Bar: For quick lookup.


### Teams Screen
Summary at the top:
Number of teams
Number of Active teams
Numer of Inactive Teams
- Header Section Action Buttons:
- Create Team (Refer attached screenshot)
- There is existing system and players and managers will be picked from system like below.

Fields/Columns:
Created: Date when the team was created.
Sports Icon: Sport played by Team.
Active: Status indicator (active/inactive).
Team Name: Name of the team.
Type: Category or sport type of the team.
Manager: Assigned manager (selected from teachers/parents in the CMS).
Chef d’Equipe: Head coach or equivalent role.
Manager Child(ren): Names of manager’s children (if applicable).
Members: Number of players on the team (roster count with details available on click).
Next Training: Date/time for the next training session.
Next Fixture: Date/time for the upcoming match.
Common UI Elements:
Filters: Filter teams by sport, coach, active status.
Sorting: Alphabetical sorting or sort by points.
Search Bar & Pagination: For efficient navigation.
Export Data: Option to export team data.
### Fixtures Screen
Summary at the top:
Next Fixture
Summary of Results Matches(Played,Won,Loss,Draw), Points(Against,For,Difference)
Editing Fixture – Summary of fixture(Away/home,number on team,subs,individuals,players selected, positions,location)
Components:
Fixture Details: Date, time, game type (home/away), venue (with Google Maps API link), opponent, result, points.Sports Name
Playing Team Selection (Refer to attached screenshot): Interface to select players for a fixture; displays count of selected players at the top (to ensure team numbers match requirements).\n -
Role Assignment (Refer to attached screenshot): When selecting players, the UI allows specifying roles (e.g., for soccer: Goalkeeper, Striker, Midfielder; for cricket: Bowler, Batsman, Wicketkeeper).\n -

Match Report: Field for the coach to submit a match report after the game.\n - Point System: Integrated points calculation for match results.\n -
Notifications & Reminders: Reminders set by the coach for fixture eve; ability to send match invites.\n-
Common UI Elements:
Filters: Filter fixtures by date, team, opponent, status.\n -
Sorting: By date, team, or fixture status.\n -
Export Data & Search Bar.
### Training Sessions Screen
Summary at the top:
Next Training
Components:
Session Details: Date, start and end time, venue, equipment requirements.\n -
Attendance & Availability: Fields to mark attendance and confirm player availability.\n-
Common UI Elements:
Filters: Filter by date, team, attendance status.\n - Export Data, Sorting, and Search Bar.
### Reports Screen
Components:
Performance Reports: Data on team and player performance, historical results, points tallies.\n- Common UI Elements:
Filters: Filter by date range, sport, team.\n - Export Data, Sorting, and Search Bar.
### News Screen
Components:
News Feed: Aggregated sports-related news from the CMS News module, including event announcements and updates.\n- Common UI Elements:
Filters: Filter by category, date, or school.\n - Search Bar.
### Contacts Screen
- Summary (Top of Screen)
- Total Number of Contacts
- Number of Coaches/Staff
- Components
- Name: Full name of the contact.
- Role: Designation or title (e.g., Head Coach, Assistant Coach).
- Contact: Primary contact information (phone, email) with an option to view details.
- Team: (Optional) The team the contact belongs to.
- Common UI Elements
- Filters: Filter by name, role, or active status.
- Sorting: Sort contacts alphabetically or by role.
- Search Bar: Quick lookup for contacts.
- Export Data: Option to export contacts data (e.g., CSV).

### Settings Screen (School Admin)
Components:
User Roles & Permissions: Manage users and their roles.\n -
Notification Preferences: Configure how and when notifications are sent.\n -
School-Level Sports Configurations: Define default parameters (e.g., point systems, default team sizes).\n-
- Common UI Elements:
Filters & Sorting: For lists of users or configurations.\n - Export Options.
### Super Admin Settings (Application Provider Team)
Components:
School Setup: Configure schools, assign access rights.\n - Sports & System Configurations: Define available sports and system-wide settings.\n - System Health Monitoring: View and export configuration reports.\n- Common UI Elements:
Filters, Sorting, and Export Data Options.

## 6. Common UI Elements Across Screens
Filters & Sorting:
Applicable on fixtures, teams, players, sports, training sessions, and reports screens.
Example fields: Date, active status, team name, sport, coach, role, points, etc.
Search Bar:
Available in all major modules for quick data lookup.
Export Data:
Ability to export table data (teams, players, fixtures, training sessions, reports) in multiple formats (CSV, Excel, PDF).
Pagination:
Implemented for all tables displaying large datasets.
Responsive Design:
Ensure UI elements are mobile-friendly, especially for the parent mobile app screens.

## 7. Non-Functional Requirements
Performance:
The system should handle multiple concurrent users efficiently.
Scalability:
Support multiple schools with independent team structures.
Security:
Implement role-based access control and data encryption.
Integration:
Seamless connection with the existing school CMS and student databases.
Automated Conflict Checks:
Prevent scheduling overlaps for students.
Exporting:
Allow data export in multiple formats.

## 8. Assumptions & Constraints
Schools will provide accurate player and staff data for system integration.
External coaches can be manually added as free-form text.
The application will be primarily web-based with potential mobile app expansion.
Schools can define and manage their own sports categories and match types.

## 9. Dependencies
Integration with the existing school CMS for user authentication and data synchronization.
Third-party mapping services (e.g., Google Maps API) for venue selection.
Secure cloud storage for data backup and retrieval.
Future expansion to include automated team assignment based on performance.

## 10. Monetisation Strategy
Virtual Sponsorship on Team Jerseys & Player Cards:
When users view a team’s lineup, each player's virtual jersey displays a small sponsor logo (e.g., "Nike" or "Adidas").
Player profile cards include a “Sponsored by Gatorade” badge, and social media posts include sponsor logos.
Branded Event Badges & Trophies:
Digital trophies and certificates (e.g., “Winner – Powered by Red Bull”) are branded with sponsor logos.
Custom Ads on Match Fixtures & Schedules:
Sponsor logos are subtly integrated into fixture lists and calendar views (e.g., “Match of the Day – Presented by Decathlon”).
Sponsored Pop-ups & Interactive Gamification:
Pop-ups after matches (e.g., “Your team scored 5 goals! Powered by Powerade”) to enhance user engagement.
Branded Leaderboards & Live Scores:
Leaderboards and live score screens display sponsor logos (e.g., “Sponsored by Adidas”).
Sponsored Challenges & Training Modules:
Fitness tests and training modules feature sponsor branding (e.g., “Speed Test Certified by Asics”).

## School Website

Below content will be posted on School Website

- Sports Home: The landing page offers quick access to recent fixtures, results, news, and updates.
- Sports & Teams Fixtures & Results: Detailed schedules and outcomes of various sports teams' matches.
- Sports Calendar: An interactive calendar displaying upcoming sports events and fixtures.
- News:
- Sports News: Latest announcements and updates related to school sports.
- Match Reports: In-depth analyses and summaries of recent games.
- Competitions & Events: Information about ongoing and upcoming sports competitions and special events.
- Photos & Videos:
- Team Photos: Group photos of various sports teams.
- Action Photos: Snapshots capturing live sports action.
- Videos: Recorded footage of matches, highlights, and other sports-related content.
- On Tour: Details about teams' tours, including itineraries and related news.
- In-House Sport: Information on internal sports activities and competitions within the school.
- Sports History: A look into the legacy and past achievements of the school's sports teams.
- Resources:
- Downloads: Access to downloadable content such as forms, guidelines, and schedules.
- Club Links: Connections to affiliated sports clubs and organizations.
- Useful Links: Additional resources and external links related to sports.
- Sports Map: Visual representation of sports facilities and event locations.
- Opponent Maps & Links: Information and directions to venues of opposing teams.
- Sports Contacts: Contact details of sports administrators and coaches.
- School Website: Direct link to the main ESMS school website.

