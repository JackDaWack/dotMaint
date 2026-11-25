import sqlalchemy as sa
from models import MaintenanceTicket, Priority, Status

class Tickets(sa.Table):
    __tablename__ = "tickets"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    issue = sa.Column(sa.String(255), nullable=False)
    priority = sa.Column(sa.Enum("low", "high", name="priority_enum"), nullable=False)
    status = sa.Column(sa.Enum("open", "in_progress", "closed", name="status_enum"), nullable=False)
    session = sa.orm.sessionmaker(bind=sa.create_engine("sqlite:///tickets.db"))()

    def insert_ticket(self, ticket: MaintenanceTicket):
        new_ticket = Tickets(
            title=ticket.description,
            description=ticket.description,
            issue=ticket.issue,
            priority=ticket.priority,
            status=ticket.status
        )
        self.session.add(new_ticket)
        self.session.commit()
        return new_ticket

    def get_all_tickets(self):
        return self.session.query(Tickets).all()

    def get_ticket_by_id(self, ticket_id: int):
        return self.session.query(Tickets).filter(Tickets.id == ticket_id).first()

    def update_ticket(self, ticket_id: int, updated_ticket: MaintenanceTicket):
        ticket = self.session.query(Tickets).filter(Tickets.id == ticket_id).first()
        if ticket:
            ticket.title = updated_ticket.description
            ticket.description = updated_ticket.description
            ticket.issue = updated_ticket.issue
            ticket.priority = updated_ticket.priority
            ticket.status = updated_ticket.status
            self.session.commit()
            return ticket
        return None

    def delete_ticket(self, ticket_id: int):
        ticket = self.session.query(Tickets).filter(Tickets.id == ticket_id).first()
        if ticket and ticket.status == Status.CLOSED:
            self.session.delete(ticket)
            self.session.commit()
            return True
        return False