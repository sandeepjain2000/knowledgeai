<!-- converted from BRD - Tusla PN (All Absences Management)-2.docx -->

# Business Requirements Document (BRD)
## Project: Tusla PN - All Absences Management
Author: Harshwardhan
### 1. Project Overview
The goal of this project is to create a new tab in the attendance management system that displays all student absences since the beginning of the academic year. The tab will provide filtering options and sorting capabilities to help administrators track cumulative absences, identify students requiring a Tusla PN (Parent Notification), and send notifications accordingly.
### 2. Objectives
- Display all absences from the start of the academic year.
- Provide filtering options by year groups, classes, and other relevant parameters.
- Enable sorting by cumulative absence count (highest first) and student name.
- Identify students with more than 10 absences where a Tusla PN has not been sent.
- Allow administrators to select students and trigger the sending of a Tusla 10-day PN.
- Provide an option to generate an A4 letter for all selected students in a group and compile these into a single PDF for email distribution.
- Log the sending of the Tusla PN with date and time stamps.
### 3. Scope
In Scope:
- Implementing a new tab in the attendance management system.
- Displaying cumulative absences per student.
- Filtering absences by year groups, classes, etc.
- Sorting data by cumulative absences (highest first) and student name.
- Identifying students who have exceeded 10 absences and have not received a Tusla PN.
- Implementing a selection mechanism for sending Tusla 10-day PN.
- Generating an A4 letter for selected students.
- Compiling selected letters into a single PDF and enabling email sending.
- Logging the date and time when a Tusla PN is sent.
Out of Scope:
- Changes to existing attendance recording mechanisms.
- Direct integration with postal or external mailing services.
- Modifying attendance APIs for Vsware and Tyro.
### 4. Functional Requirements
4.1 Absence Data Display
- A new tab will display all absences from the start of the academic year.
- Each student’s cumulative absence count will be shown.
- Filtering options include:
- Year groups
- Classes
- Other custom parameters
- Sorting options include:
- Highest absences first
- Alphabetically by student name
4.2 Identification of Tusla PN Eligibility
- The system will flag students with more than 10 absences where a Tusla PN has not been sent.
- A filter option will allow users to quickly find this set of students.
- Users can select individual or multiple students from this list.
4.3 Sending Tusla 10-day PN
- Administrators can tap/select students to trigger the sending of a Tusla 10-day PN.
- The system will log the date and time of when the notification is sent.
4.4 A4 Letter Generation & PDF Compilation
- Generate an A4 letter for each selected student.
- Compile all letters into a single PDF.
- Send the PDF via email to the logged-in user.
- The recipient can then forward the PDF to the office for processing.
### 5. Non-Functional Requirements
- Performance: The system should efficiently process large attendance datasets.
- Scalability: The solution should support multiple schools and large numbers of students.
- Security: Only authorized users can access, filter, and send Tusla notifications.
- Usability: The interface should be intuitive and allow for quick identification and action on student absences.
### 6. Assumptions and Constraints
- The system relies on accurate and up-to-date attendance data from Vsware and Tyro.
- Users have the necessary permissions to send Tusla PNs and generate reports.
- Absence records follow the standard school year format.
- The email sending mechanism will use the existing email service integrated with the system.
### 7. Dependencies
- Attendance data from Vsware (Wonde API) and Tyro (Tyro API).
- Existing database storing student attendance records.
- PDF generation and email-sending services.
- User authentication and authorization mechanisms.
### 8. Success Metrics
- The new tab accurately displays and filters absence records.
- Users can efficiently sort and identify students exceeding 10 absences.
- Tusla PNs are sent and logged correctly.
- A4 letters are generated and compiled into a single PDF successfully.
- The email feature works as expected and delivers the PDF to the logged-in user.

This document defines the requirements for implementing the Tusla PN - All Absences Management feature. Let me know if any modifications are needed!
