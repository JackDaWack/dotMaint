from fastapi import FastAPI
from models import MaintenanceTicket, Priority, Status
import database

app = FastAPI()
db = database.Tickets()

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
        db.insert_ticket(new_ticket)
        return new_ticket
    except Exception as e:
        print(f"Error creating ticket: {e}")
        return None

@app.get("/tickets")
async def get_all_tickets():
    try:
        return db.get_all_tickets()
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return None

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    try:
        return db.get_ticket_by_id(ticket_id)
    except Exception as e:
        print(f"Error fetching ticket: {e}")
        return None

@app.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, updated_ticket: MaintenanceTicket):
    try:
        return db.update_ticket(ticket_id, updated_ticket)
    except Exception as e:
        print(f"Error updating ticket: {e}")
        return None
    except Exception as e:
        print(f"Error updating ticket: {e}")
        return None

@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    try:
        return db.delete_ticket(ticket_id)
    except Exception as e:
        print(f"Error deleting ticket: {e}")
        return False
    except Exception as e:
        print(f"Error deleting ticket: {e}")
        return False

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