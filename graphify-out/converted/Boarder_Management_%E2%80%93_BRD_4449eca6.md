<!-- converted from Boarder_Management_%E2%80%93_BRD.docx -->

# Business Requirements Document (BRD)
## 1. Introduction
### 1.1 Purpose
The purpose of this document is to define the business requirements for the Boarders Management System, a solution designed to help hostel/school staff efficiently manage boarder students, their daily movements, house allocation, and attendance.
### 1.2 Scope
The system will be used by hostel staff through a single Boarder Manager per school/hostel to:
Manage boarder student records
Track daily sign-in and sign-out (On-Campus / Off-Campus)
Assign students to hostel houses
Take and manage attendance based on houses
### 1.3 Stakeholders
School Management
Hostel Administration
Boarder Manager
Hostel Staff
IT / Support Team

## 2. Business Objectives
Provide a centralized system to manage boarder students
Improve visibility and accuracy of student movement (in/out of campus)
Enable house-based student grouping and attendance
Reduce manual registers and errors
Ensure accountability and student safety

## 3. User Roles
### 3.1 Boarder Manager
One Boarder Manager per school/hostel
Full access to manage students, houses, and attendance
### 3.2 Parents/Guardian
A Leave Note is required to take a student off-campus for sign-out.

## 4. Functional Requirements
### 4.1 Student Management
Add, update, and deactivate boarder students
Store student details (Name, ID, Class, House, Status)
Assign or reassign students to houses
### 4.2 House Management
Create and manage hostel houses
Assign students to one house at a time
View students grouped by house
### 4.3 Daily Sign-In / Sign-Out Management
Record student sign-out (Off-Campus)
Record student sign-in (On-Campus)
Capture date, time, and status
Prevent duplicate or conflicting entries
View daily and historical movement logs
### 4.4 Campus Status Tracking
Maintain real-time status of students:
On-Campus
Off-Campus
Display current campus status at student and house level
### 4.5 Attendance Management
Take attendance based on houses
Mark attendance for all students within a house
Support daily attendance records
View attendance summaries by date and house
### 4.6 Reports & Logs
Daily sign-in/sign-out report
Attendance report by house and date
Student movement history

## 5. Non-Functional Requirements
### 5.1 Security
Role-based access control
Only authorized users can update records
### 5.2 Performance
System should support concurrent usage by hostel staff
Attendance and movement updates should reflect in real time
### 5.3 Availability
System should be available during hostel operational hours
### 5.4 Audit & Traceability
Maintain audit logs for sign-in/sign-out and attendance changes

## 6. Assumptions
Each school/hostel has exactly one Boarder Manager
Each student can belong to only one house at a time
Attendance is taken daily
Internet connectivity is available during operations

## 7. Constraints
System must align with existing school data standards
Data privacy and student safety must be maintained

## 8. Success Metrics
Reduction in manual attendance errors
Accurate real-time visibility of student campus status
Improved efficiency in hostel operations
Positive feedback from hostel staff and management

## 9. Future Enhancements (Out of Scope)
Parent notifications for sign-in/out
Mobile app support
Integration with external attendance systems
Automated alerts for missing sign-ins

