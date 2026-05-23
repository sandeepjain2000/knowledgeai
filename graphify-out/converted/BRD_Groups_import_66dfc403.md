<!-- converted from BRD_Groups_import.docx -->


## BRD :- Groups Import

## Purpose
The purpose of this feature is to allow users to:
Import students from CSV files
Validate each student against the existing database
Automatically add valid students to a created group
Handle mismatches, missing students, or duplicate matches safely
Allow users to review and resolve issues before final submission
This functionality reduces manual data entry, minimizes errors, and speeds up the process of creating student groups.

Background & Problem Statement
Currently, adding students to groups requires manual searching and assignment. This is time-consuming and prone to mistakes, especially when onboarding many students at once.
Users need a bulk import mechanism that:
Accepts standardized CSV formats from different systems (VsWare, Tyro)
Ensures imported students match correctly with existing database records
Clearly shows errors or uncertain matches for manual review

3. SCOPE
### 3.1 In Scope
Upload CSV file
Support two CSV formats:
VsWare: vsWare Id/Department Id, Full Name, Class
Tyro: Name, Base Class
Validate students against database
Automatically add valid students to group
Show unresolved or failed students in a temporary partially rendered review screen
Allow exporting failed/invalid records
Handle duplicate matches (Tyro imports)
Allow users to manually resolve duplicates and submit


## 4.  Functional Requirements
### 4.1 File Upload
FR-01: The system must allow users to upload a CSV file.
FR-02: The system must detect which format is being uploaded:
VsWare format with both the header types
Tyro format
FR-03: If headers do not match expected formats, the system must show an error message.

### 4.2 Validation Rules
FR-04: For each uploaded record:
Validate required fields are present
Validate file row structure
Match student in the database using defined keys (see below)

VsWare Matching
Match using:
vsWare Id/Department Id, FullName , Class

Tyro Matching
Match using:
Name
Base Class


### 4.3 Handling Results
4.3.1 Successful Matches
FR-05: If exactly one matching student is found, add the student to the selected group.

4.3.2 Student Not Found
FR-06: If no matching student exists:
Record goes to the temporary review table
Record remains unassigned
4.3.3 Multiple Matches (Tyro Only)
FR-07: If more than one student matches:
Show the record in the temporary review screen
Display each possible student with their Student IDs
Allow user to select the correct student
Once selected and submitted, the chosen student will be added to the group


## 5. Temporary Review Screen (Partial Render)
The system must display a temporary screen containing:
Table with same headers as imported file
Status indicator (Not Found / Duplicate / Error)
Checkboxes or selection controls for duplicate resolution
Button to:
Export failed list
Submit selected fixes
Records on this screen are not permanently saved until the user submits.
And these records are saved in session so it is temporary if the user will reload or navigate anywhere the data will be lost.

## 6. Export Failed List
FR-08: The system must allow exporting unresolved/failed records as CSV with:
Original headers

## 7. Error Handling & Messages
The system must clearly inform users of:
Invalid file headers
Malformed rows
No matches found
Duplicate matches requiring user selection
Duplicate group name
Messages should be human-readable and non-technical. And will appear after 15 seconds.


## 8. Success Criteria
This feature is successful when:
Users can upload CSV files reliably
Majority of records import automatically
Unmatched or ambiguous records are clearly shown
Users can manually resolve duplicates
Failed records can be exported
Group creation time is significantly reduced

