from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Priority:
    LOW = "low"
    HIGH = "high"

class Status:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class MaintenanceTicket(BaseModel):
    ticket_id: int
    description: str
    issue: str
    priority: str = Priority.LOW
    status: str = Status.OPEN

    def __init__(self, ticket_id: int, description: str, issue: str, priority: str = Priority.LOW, status: str = Status.OPEN):
        self.ticket_id = ticket_id
        self.description = description
        self.issue = issue
        self.priority = priority
        self.status = status

    def get_ticket_info(self):
        return {
            "ticket_id": self.ticket_id,
            "description": self.description,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status
        }

    def get_ticket_ID(self):
        return self.ticket_id

    def get_description(self):
        return self.description

    def get_issue(self):
        return self.issue

    def get_priority(self):
        return self.priority

    def get_status(self):
        return self.status

    def update_description(self, new_description: str):
        self.description = new_description

    def update_issue(self, new_issue: str):
        self.issue = new_issue

    def update_priority(self, new_priority: str):
        if new_priority in (Priority.LOW, Priority.HIGH):
            self.priority = new_priority
        else:
            raise ValueError("Invalid priority value")

    def update_status(self, new_status: str):
        if new_status in (Status.OPEN, Status.IN_PROGRESS, Status.CLOSED):
            self.status = new_status
        else:
            raise ValueError("Invalid status value")

tickets_db = [] #Mock database to store tickets
next_ticket_id = 1

@app.post("/tickets")
async def create_ticket(ticket: MaintenanceTicket):
    try:
        global next_ticket_id
        new_ticket = MaintenanceTicket(
            ticket_id=next_ticket_id, 
            description=ticket.description, 
            issue=ticket.issue, 
            priority=ticket.priority, 
            status=ticket.status
            )
        next_ticket_id += 1
        tickets_db.append(new_ticket)
        return new_ticket
    except Exception as e:
        print(f"Error creating ticket: {e}")
        return None

@app.get("/tickets")
async def get_all_tickets():
    try:
        return tickets_db
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return None

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    try:
        for ticket in tickets_db:
            if ticket.get_ticket_ID() == ticket_id:
                return ticket
        return None
    except Exception as e:
        print(f"Error fetching ticket: {e}")
        return None


@app.get("/")
async def read_root():
    try:
        return {"Hello": "World"}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/health")
async def health_check():
    try:
        # Perform health check logic here (e.g., database connection, external service check)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}