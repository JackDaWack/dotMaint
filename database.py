import sqlite3
import models

def initialize_database():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (ticket_id INTEGER PRIMARY KEY, 
                 description TEXT, 
                 issue TEXT, 
                 priority TEXT, 
                 status TEXT)''')
    conn.commit()
    conn.close()

def insert_ticket(ticket: models.MaintenanceTicket):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''INSERT INTO tickets (ticket_id, description, issue, priority, status) 
                 VALUES (?, ?, ?, ?, ?)''', 
                 (ticket.ticket_id, ticket.description, ticket.issue, ticket.priority, ticket.status))
    conn.commit()
    conn.close()

def get_ticket_by_id(ticket_id: int):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets WHERE ticket_id=?', (ticket_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return models.MaintenanceTicket(ticket_id=row[0], description=row[1], issue=row[2], priority=models.Priority(row[3]), status=models.Status(row[4]))
    return None

def get_all_tickets():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets')
    rows = c.fetchall()
    conn.close()
    tickets = []
    for row in rows:
        tickets.append(models.MaintenanceTicket(ticket_id=row[0], description=row[1], issue=row[2], priority=models.Priority(row[3]), status=models.Status(row[4])))
    return tickets

def update_ticket(ticket_id: int, updated_ticket: models.MaintenanceTicket):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''UPDATE tickets 
                 SET description=?, issue=?, priority=?, status=? 
                 WHERE ticket_id=?''', 
                 (updated_ticket.description, updated_ticket.issue, updated_ticket.priority.value, updated_ticket.status.value, ticket_id))
    conn.commit()
    conn.close()

def delete_ticket(ticket_id: int):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('DELETE FROM tickets WHERE ticket_id=?', (ticket_id,))
    conn.commit()
    conn.close()