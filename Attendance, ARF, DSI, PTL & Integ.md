# Attendance, ARF, DSI, PTL & Integration Use Cases and Edge Cases

## Core Principle

Attendance is not one workflow. It is four workflows constantly reconciling with each other:

| Perspective | What it answers |
|---|---|
| Roll / attendance system | What is the official attendance mark? |
| ARF | Why is the student absent or apparently absent? |
| DSI | What physical movement actually happened? |
| Parent notes / PTL / Late notes | What did the parent request or explain? |

### Safest Rule

- Parent note = intention or explanation
- DSI = actual movement timestamp
- Attendance system = official record
- ARF = parent communication and absence-resolution workflow

---

# 1. Normal Attendance Flow

1. Teacher/staff mark AM or PM roll
2. System identifies unexplained absences
3. If a student is marked absent without a valid note, an ARF / Absence Request Form may be sent to parent
4. Parent responds by:
   - approving/explaining absence
   - saying the student will be late
   - selecting Please Check because they believe the student is in school
5. Student movement is captured through DSI:
   - Late = arrived late
   - Leaving = leaving school
   - Returning = came back after leaving
6. Staff reconcile mismatches through:
   - Attendance Overview
   - Please Checks
   - Lates
   - PTL
   - Anomalies

---

# 2. ARF Perspective

ARF is triggered from the attendance system, not simply from parent intention.

Example:
If AM roll says student is absent and no valid note exists, ARF is sent.

## Parent Response Options

| Parent response | Meaning | Staff/System Action |
|---|---|---|
| Approve / complete absence | Student is absent | Absence is explained and may be written back |
| Mark as Late | Student is expected to arrive late | ARF is held; if student signs in late, ARF is cancelled |
| Please Check | Parent believes student is present | Staff must verify and correct attendance |

## Important ARF Rules

- If student signs in late after parent marked “will be late”, ARF should be cancelled
- If student never arrives, ARF may be sent again the next morning
- If valid PTL/late note exists around roll-call timing, ARF may be suppressed
- If roll changes from absent to present/school activity, ARF should be cancelled
- If roll changes from present to unexplained absent, ARF may be created later

### Key Principle

ARF is not only an “absence form”.

It is the workflow for resolving:
- unexplained absence
- disputed attendance
- reconciliation mismatches

---

# 3. Late Process

## Normal Late Flow

1. Student arrives late
2. Student uses DSI > Late
3. If parent already submitted late note:
   - parent gets arrival confirmation
4. If no note exists:
   - parent receives late request
5. Staff review in Attendance Overview > Lates
6. Late becomes:
   - authorised
   - unauthorised
   - pending
   - requested

## Critical Rule

Even if parent submitted a late note:

- student must still use DSI
- note explains reason
- DSI proves arrival time

---

# 4. PTL / Leave Process

PTL = Permission To Leave

## Normal PTL Flow

1. Parent submits PTL
2. Staff review and approve
3. Student goes to DSI and selects Leaving
4. DSI records actual departure time
5. Parent receives confirmation
6. Attendance system updates automatically or manually

## Critical Rule

Approved PTL does NOT mean student has left.

Student has only left when:
- DSI sign-out exists
- office sign-out exists

---

# 5. DSI Process

## DSI Actions

| DSI Action | Meaning |
|---|---|
| Late | Student arrived late |
| Leaving | Student left school |
| Returning | Student returned after leaving |

## Key Principle

DSI is the actual movement log.

It becomes operational evidence during disputes:
- parent says child left at 1:30
- student signed out at 1:47
- office updated attendance at 2:00
- sync happened later

In such cases:
- DSI timestamp is authoritative movement evidence

---

# 6. Key Combined Use Cases

## Parent submits PTL, but student comes in late

This is TWO events.

### Correct Handling

- Student arrives late → DSI Late
- If no late note exists → parent receives late request
- PTL remains separate
- Later student uses DSI Leaving

Final record should show:
- late arrival
- early leave

---

## Parent submits Late note, but student later wants to leave

Also TWO events.

### Correct Handling

- Late note explains arrival
- Student signs in using DSI Late
- Separate PTL required for leaving
- If no PTL exists → office intervention required

Late note ≠ permission to leave

---

## Parent submits absence note, then drops child to school

### Correct Handling

- Student signs in via DSI Late
- ARF/absence cancelled or corrected
- Attendance should no longer show full-day absence
- Anomaly may exist because parent note conflicts with attendance

---

## Parent submits PTL while student already absent at home

### Correct Handling

- Treated as conflict
- Student cannot leave school if not in school
- Resolve absence first
- PTL may be blocked or reviewed

---

## Parent marks “student will be late” but student never arrives

### Correct Handling

- ARF temporarily held
- Staff wait for DSI Late
- If no DSI sign-in:
  - student remains absent
  - ARF resent or followed up

Late note/request ≠ proof of attendance

---

## Student marked absent, but parent says student is present

This is Please Check.

### Staff should:

- Check later class rolls
- Check DSI
- Physically verify if required
- Correct attendance appropriately
- Cancel or continue ARF

---

# 7. Important Edge Case Categories

# Parent Communication Issues

| Scenario | Correct Principle |
|---|---|
| Wrong pickup time | Edit/cancel/recreate PTL |
| Wrong child selected | Cancel incorrect PTL |
| Duplicate PTLs | Keep one valid record |
| Parent updates PTL after student left | Preserve original departure timestamp |
| Parent cancels PTL after sign-out | Do not erase movement history |
| Verbal phone instruction only | Create audit-trail note |
| Parent says note submitted but no record exists | Check logs |
| Parent assumes approval means auto sign-out | Clarify DSI requirement |
| Conflicting parents/custody issue | Escalate |

---

# Student Behaviour Issues

| Scenario | Correct Principle |
|---|---|
| Student bypasses DSI | Staff manual follow-up |
| Student signs in as friend | Identity/audit issue |
| Student signs out another student | Safeguarding issue |
| Student leaves through alternate gate | Manual reconciliation |
| Student signs out but stays on campus | Investigate |
| Student leaves and returns without Returning | Correct movement log |
| Student signs out then immediately signs back in | Preserve timestamps |
| Student leaves with sibling | Separate sign-out required |
| Student refuses DSI | Office process required |

---

# Staff Operational Issues

| Scenario | Correct Principle |
|---|---|
| PTL approved without identity verification | Risky |
| Bulk approval mistakes | Reverse with audit trail |
| Manual late while DSI already exists | Avoid duplicates |
| Present mark while DSI shows leaving | Reconcile immediately |
| Please Checks ignored | Parent dispute unresolved |
| Attendance edited during sync | Risk of overwrite |
| Returning students forgotten | Incorrect off-campus status |
| Boarding vs school disagreement | Use timestamps and ownership rules |

---

# DSI / Technical Issues

| Scenario | Correct Principle |
|---|---|
| DSI offline | Use fallback log |
| DSI clock wrong | Review affected timestamps |
| Duplicate DSI submission | Keep earliest valid |
| Partial transaction save | Verify dashboard and notifications |
| Stale sync allows sign-out | Manual reconciliation required |
| Parent notified before commit | Verify final saved record |
| Multiple kiosk conflict | Central record authoritative |

---

# Integration Issues

| Scenario | Correct Principle |
|---|---|
| Tyro absent before late sync | Later DSI may correct |
| VSware ARF before sync | Reconcile later |
| Compass manual process | Manual reconciliation required |
| Write-back partially fails | Verify student-by-student |
| Bulk PTL partial sync | Review failures |
| Student ID mismatch | Stop automation |
| Timezone mismatch | Use school local time |
| Parent app differs from office dashboard | Dashboard authoritative |

---

# 8. Boarding / Residential Perspective

Boarding introduces another layer:

| School Attendance | Boarding Status |
|---|---|
| Present / absent / late | On-campus / off-campus |
| PTL | Leave from school/campus |
| DSI Leaving | Physical departure |
| DSI Returning | Physical return |

## Boarding Edge Cases

- Boarder signs out from hostel but not school
- Boarder marked present while off-campus
- Weekend leave overlaps Monday attendance
- Housemaster says on-campus but PTL says off-campus
- Travel delay prevents timely return
- Temporary guardian submits leave

---

# 9. Integration Summary

| System | Impact |
|---|---|
| Tyro | Best automation and smart late detection |
| VSware | Partial automation |
| Compass | Mostly manual |

---

# 10. Practical Decision Framework

For confusing cases, staff should ask:

1. What does the roll say?
2. Was ARF sent?
3. What parent note exists?
4. What did DSI record?
5. Does attendance match DSI and parent note?
6. Is there safeguarding/custody concern?

---

# 11. Most Important Rule

Do NOT merge:
- Absence
- Late
- PTL

into one assumption.

A student may legitimately have multiple attendance events in one day:

- absent in AM but later late
- late arrival and early PTL
- PTL departure and later return
- parent absence note but student arrives
- ARF sent but later cancelled
- boarder off-campus but still marked present

---

# Recommended Timeline Model

System should preserve chronological sequence:

1. Parent submitted note/request
2. Roll marked attendance
3. ARF sent/responded
4. DSI movement occurred
5. Staff approved/corrected
6. External system synced/wrote back
7. Anomaly reviewed
