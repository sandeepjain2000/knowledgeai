# Attendance Management System – Functional Overview

Source: :contentReference[oaicite:0]{index=0}

---

# Core Idea

Attendance management is handled through the **Attendance Overview / Year Head Dashboard**, with the **Digital Sign-In/Out device (DSI)** acting as the real-world timestamp source for students arriving late, leaving early, or returning.

The system combines:

- Parent-submitted notes
- Staff approval/action
- Student DSI activity
- External attendance system data, such as Tyro, VSware, or Compass
- Follow-up workflows like:
  - Late Requests
  - Absence Requests
  - Please Checks
  - Anomalies

---

# Main Attendance Areas

Attendance Overview includes:

- **Absences**
  - Absent notes
  - Absence requests

- **Lates**
  - Late notes
  - Late requests
  - DSI late sign-ins

- **PTL (Permission to Leave)**
  - Early leave requests

- **Please Checks**
  - Parent disputes where they believe the student should be present

- **Anomalies**
  - Mismatches between parent notes and the attendance system

- **Attendance Alerts**
  - Cumulative absence threshold notifications

---

# Access by Role

| Role | Access |
|---|---|
| Year Heads / Tutors | Assigned year groups only |
| Principal | All students |
| Deputy Principal | All students |
| Attendance Officer | All students |
| Office Staff | All students |

---

# DSI – Digital Sign-In/Out Device

The DSI device is central to accurate attendance because it records the actual time a student signs in or out.

Students use it for three main actions:

1. **Late**
   - Student signs in late

2. **Leaving**
   - Student signs out early using an approved PTL

3. **Returning**
   - Student signs back in after leaving earlier the same day

When a student uses DSI:

- Parents are notified of the actual arrival/departure time
- Dashboard records are updated

> Important: Students should use the DSI device even if a parent already submitted a note.  
> The note explains the reason; the DSI confirms the actual movement.

---

# Late Management Process

A student is treated as late when they arrive after roll call or the expected attendance time.

## Standard Late Flow

1. Student arrives late
2. Student taps **Late** on DSI
3. Student selects:
   - Year
   - Class
   - Name
4. System checks whether a parent note exists
5. If note exists:
   - Parent receives confirmation that student arrived
6. If no note exists:
   - Parent receives a late notification/request
7. Staff review the late in:
   - Attendance Overview → Lates
8. Late is classified as:
   - Authorised
   - Unauthorised
   - Pending

---

# Late Statuses

| Status | Meaning |
|---|---|
| Authorised | Parent gave a valid reason |
| Unauthorised | No valid reason |
| Pending | Waiting for parent note |
| Note Received | Parent submitted the late note |
| Requested | System/school requested note because student arrived late without one |

---

# Staff Actions for Lates

Staff can:

- Filter lates by:
  - Date
  - Year
  - Class
  - Authorisation status
  - Note status
  - Sign-in status

- Add manual Late Requests
- Delete incorrect late records
- Send Personal Notifications to parents
- Add students to detention for repeated unauthorised lates
- Export late data

> Dashboard is preferred because it remains live.

---

# PTL – Permission to Leave Process

PTL is used when a parent wants a student to leave school early.

## Standard PTL Flow

1. Parent submits PTL through the app
2. Staff open:
   - Attendance Overview → PTL
3. Pending PTLs for today appear by default
4. Staff review request
5. Staff approve PTL individually or in bulk
6. Student taps **Leaving** on DSI
7. Parent receives confirmation student has left
8. System records actual sign-out time

> Important: Approval alone does not mean the student has left.  
> Departure is only recorded when the student signs out through DSI or office staff manually signs them out.

---

# PTL Settings

Schools can configure:

- Popup message if PTL submitted after a certain time
- Allowed sign-out interval

Example:

- PTL requested for **1:30 PM**
- Buffer = **10 minutes**

Student may sign out between:

- **1:20 PM**
- **1:40 PM**

---

# Use Cases and Edge Cases

---

## 1. Parent submits PTL, student leaves correctly

### Flow

1. Parent submits PTL for 1:30 PM
2. Staff approve
3. Student taps **Leaving** on DSI
4. Parent gets notification
5. Departure logged

> Ideal flow.

---

## 2. PTL submitted but not approved

### Result

- Student attempts sign-out
- DSI may block sign-out
- Student directed to office

### Operational Recommendation

- Staff should approve PTLs promptly to avoid queues/delays

---

## 3. PTL approved but student never signs out

### Situation

- PTL approved
- No departure timestamp exists

### Staff Action

Verify whether:

- Student remained in school
- Student left without DSI
- Office manually signed student out

---

## 4. Student comes late and also has PTL

### Example

- PTL for 2:00 PM
- Student arrives at 9:45 AM

### Correct Handling

#### Morning Arrival

- Student signs in using **Late**
- Parent may receive Late Request

#### Afternoon Departure

- PTL reviewed separately
- Student signs out using **Leaving**

### Result

Two attendance events recorded:

- Late arrival
- Early departure

> PTL should not automatically explain the late arrival unless specifically stated in the note.

---

## 5. Parent submits Late note in advance

### Result

- Student signs in late on DSI
- Parent receives arrival confirmation
- No unnecessary late request generated

---

## 6. Parent submits Late note but student never arrives

### Situation

- Note says student will be late
- No DSI sign-in occurs

### Staff Action

Check:

- Roll calls
- Attendance system

Possible outcome:

- Convert to absence case
- May appear under anomalies

---

## 7. Student bypasses DSI

### Common Issue

Student arrives late but skips sign-in device.

### Possible Actions

- Staff manually add Late Request
- Please Check can mark student as Late
- Tyro may auto-detect late presence later

### Best Practice

Always send student back to DSI where possible because:

- Actual timestamp captured
- Parent communication triggered

---

## 8. Parent says “Student is in school”

This is the **Please Check** workflow.

### Staff Verify

- Is student in class?
- Did they arrive late?
- Are they on activity/trip?
- Are they absent?

### Possible Outcomes

| Outcome | Meaning |
|---|---|
| Mark Present | Roll call incorrect |
| Mark Late | Student arrived late |
| Mark School Activity | Student on activity/trip |
| Not In Class - Confirmed | Student genuinely absent |

---

## 9. Parent selects “Mark as Late”

### Meaning

Parent expects student to arrive later.

### System Behaviour

- Absence request held until end of day

#### If student signs in late

- Absence request cancelled

#### If student never arrives

- Absence request re-sent next morning

---

## 10. PTL exists but no DSI sign-out

### Concern

Safeguarding issue because actual departure time missing.

### Recommended Practice

Do not only update external attendance system.

Instead:

- Sign student out via:
  - Unique Schools
  - DSI
  - Office staff process

This ensures:

- Parent notification
- Timestamp captured

---

## 11. Student tries leaving without PTL

### DSI Behaviour

- Student taps Leaving
- No PTL exists
- Popup directs student to office

### Office Staff Then

- Contact parent/guardian
- Follow manual process

---

## 12. Student leaves and later returns

Student should use:

| Action | DSI Option |
|---|---|
| Leaving school | Leaving |
| Returning to school | Returning |

This creates a complete movement record.

---

## 13. Parent submits wrong note type

### Examples

- Absent note submitted but student present
- Late note submitted but student absent
- PTL submitted but full-day absence recorded

### Result

Appears under **Anomalies**

### Staff Action

1. Review mismatch
2. Correct attendance system if needed
3. Mark anomaly acknowledged

> Acknowledging anomaly does not:
> - Update attendance system
> - Notify parents

It only removes the anomaly from the list.

---

# Integration Impact

---

# Tyro

Most automated integration.

## Features

- Immediate late/PTL syncing
- AM/PM and class roll access
- Smart late detection
- Automatic PTL push
- Can convert AM absence to late
- Can suppress unnecessary absence requests

---

# VSware

Partially automated.

## Characteristics

- Uses Wonde API
- Up to 1-hour delay
- Session roll calls only
- Lates sync at session level
- PTL handled manually by AFM team
- No smart class-roll late detection

---

# Compass

Manual integration.

## Characteristics

- No API access
- AFM team manually handles:
  - Absences
  - Lates
  - PTL
  - Write-backs
  - Corrections

---

# Practical Daily Routine

Recommended operational flow:

1. Check Absences after AM roll
2. Review Please Checks urgently
3. Monitor Lates throughout morning
4. Approve PTLs before leaving times
5. Ensure students use DSI for:
   - Late arrival
   - Leaving
   - Returning
6. Check Anomalies daily/weekly
7. Identify repeated unauthorised lates
8. Send Personal Notifications or detention notices
9. Avoid directly updating external attendance system where DSI should capture movement
10. Review unresolved end-of-day cases:
    - Pending late notes
    - Unsigned-out PTLs
    - Attendance mismatches