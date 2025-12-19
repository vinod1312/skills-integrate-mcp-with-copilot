"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # ensure members map exists (migrated from participants)
    if "members" not in activity:
        # migrate participants list to members map with role 'participant'
        activity["members"] = {p: ["participant"] for p in activity.get("participants", [])}
        activity.pop("participants", None)

    # Validate student is not already signed up
    if email in activity["members"] and "participant" in activity["members"][email]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student as participant role
    roles = activity["members"].setdefault(email, [])
    if "participant" not in roles:
        roles.append("participant")

    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # ensure members map exists
    if "members" not in activity:
        activity["members"] = {p: ["participant"] for p in activity.get("participants", [])}
        activity.pop("participants", None)

    # Validate student is signed up
    if email not in activity["members"] or "participant" not in activity["members"][email]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove participant role
    roles = activity["members"][email]
    if "participant" in roles:
        roles.remove("participant")

    # if no roles remain, remove member entirely
    if not roles:
        activity["members"].pop(email, None)

    return {"message": f"Unregistered {email} from {activity_name}"}


@app.get("/activities/{activity_name}/members")
def list_members(activity_name: str):
    """List members and their roles for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if "members" not in activity:
        activity["members"] = {p: ["participant"] for p in activity.get("participants", [])}
        activity.pop("participants", None)

    return activity["members"]


def _has_organizer(activity: dict) -> bool:
    return any("organizer" in roles for roles in activity.get("members", {}).values())


def _is_organizer(activity: dict, actor_email: str) -> bool:
    return actor_email in activity.get("members", {}) and "organizer" in activity["members"][actor_email]


@app.post("/activities/{activity_name}/roles/assign")
def assign_role(activity_name: str, email: str, role: str, x_actor_email: str | None = Header(None)):
    """Assign a role to a member. If no organizer exists, allow the acting user to bootstrap themself as organizer."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if "members" not in activity:
        activity["members"] = {p: ["participant"] for p in activity.get("participants", [])}
        activity.pop("participants", None)

    # Authorization: if organizers exist, only organizers may assign roles
    if _has_organizer(activity):
        if not x_actor_email or not _is_organizer(activity, x_actor_email):
            raise HTTPException(status_code=403, detail="Only organizers can assign roles")
    else:
        # no organizers yet: allow actor to assign themselves as organizer
        if role == "organizer":
            if not x_actor_email or x_actor_email != email:
                raise HTTPException(status_code=403, detail="Bootstrap organizer must assign themself")

    roles = activity["members"].setdefault(email, [])
    if role not in roles:
        roles.append(role)

    return {"message": f"Assigned role '{role}' to {email} in {activity_name}"}


@app.post("/activities/{activity_name}/roles/remove")
def remove_role(activity_name: str, email: str, role: str, x_actor_email: str | None = Header(None)):
    """Remove a role from a member."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if "members" not in activity:
        activity["members"] = {p: ["participant"] for p in activity.get("participants", [])}
        activity.pop("participants", None)

    # Authorization: only organizers can remove roles (if organizers exist)
    if _has_organizer(activity) and (not x_actor_email or not _is_organizer(activity, x_actor_email)):
        raise HTTPException(status_code=403, detail="Only organizers can remove roles")

    if email not in activity["members"] or role not in activity["members"][email]:
        raise HTTPException(status_code=400, detail="Member does not have this role")

    activity["members"][email].remove(role)
    if not activity["members"][email]:
        activity["members"].pop(email, None)

    return {"message": f"Removed role '{role}' from {email} in {activity_name}"}
