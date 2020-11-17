from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask_login import current_user, login_required
from flask import current_app as app
from .. import forms
from .. import auth
from datetime import datetime, date
from ..models import db, Drives, Clients, User
from flask_login import logout_user
from .. import login_manager

# Blueprint Configuration
drivebay_bp = Blueprint(
    'drivebay_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

print(auth.USER_ID)


@app.context_processor
def insert_user():
    if auth.USER_ID == None:
        return dict(user='No User')
    else:
        id = int(auth.USER_ID)
        user = User.query.get(id)
        return dict(user=user.name)


# Sets User variable to admin
@app.context_processor
def if_admin():
    if auth.USER_ID == None:
        return dict(admin=False)
    else:
        user = User.query.get(auth.USER_ID)
        if user.account_type == 'admin':
            return dict(admin=True)
        else:
            return dict(admin=False)


# Sets User variable
@app.context_processor
def user_type():
    if auth.USER_ID == None:
        return dict(user_type=None)
    else:
        user = User.query.get(auth.USER_ID)

        return dict(user_type=user.account_type)


# Checks if a user has been registered
def check_user():
    user = User.query.get(auth.USER_ID)
    if user.account_type == 'pend':
        return True


# Checks if a user is an Admin
def check_admin():
    user = User.query.get(auth.USER_ID)
    if user.account_type != 'admin':
        return False


@drivebay_bp.route('/', methods=['POST', 'GET'])
@login_required
def dashboard():
    # Check user has permission
    if check_user():
        return redirect(url_for('drivebay_bp.pending'))

    # Create sort by Client drop down
    client_list = [(0, 'All Clients')]
    for client in Clients.query.all():
        client_list.append((client.id, client.client))

    # Create sort by status drop down
    status_list = [(0, 'All Status')]
    for status in User.query.all():
        status_list.append((status.id, status.name))

    form = forms.DashboardSearch()
    form.client.choices = client_list
    form.assigned.choices = status_list

    if request.method == 'POST':

        if request.form.get('search'):
            return redirect(f"/show_drive/{request.form.get('search')}")

        assigned = dict(form.assigned.choices).get(form.assigned.data)
        status = request.form.get('status')
        client_select = dict(form.client.choices).get(form.client.data)
        urgency_filter = ""
        filter_code = 0
        search_filter = ""

        form.client.default = client_select

        if assigned == 'All' and status == 'All' and client_select == 'All Clients':
            return render_template('dashboard.html', all_tickets=Drives.query.all(),
                                   clients=Clients.query.all(), title="Drive Bay", header=f"All", show_status="All",
                                   show_assigned="All", eval=eval,
                                   description="Web interface for HyperDrive App", show_clients=client_select,
                                   now=date.today())

        if assigned == 'All Users':
            filter_code += 1
        else:
            drives = Drives.query.filter(support_ticket.assigned.contains(assigned)).all()
            if len(tickets) > 0:
                assigned = drives[0].assigned
            else:
                assigned = None

        if status == 'All':
            filter_code += 3

        if client_select == 'All Clients':
            filter_code += 5
        else:
            drives = Drives.query.filter(support_ticket.client.contains(client_select)).all()
            if len(tickets) > 0:
                client_select = drives[0].client
            else:
                client_select = None

        if filter_code == 1:
            search_filter = Drives.query.filter_by(client=client_select, status=status).order_by(Drives.logged_in.asc()).all()
        elif filter_code == 3:
            search_filter = Drives.query.filter_by(client=client_select, assigned=assigned).order_by(Drives.logged_in.asc()).all()
        elif filter_code == 4:
            search_filter = Drives.query.filter_by(client=client_select).order_by(Drives.logged_in.asc()).all()
        elif filter_code == 5:
            search_filter = Drives.query.filter_by(assigned=assigned, status=status).order_by(Drives.logged_in.asc()).all()
        elif filter_code == 6:
            search_filter = Drives.query.filter_by(status=status).order_by(Drives.logged_in.asc()).all()
        elif filter_code == 8:
            search_filter = Drives.query.filter_by(assigned=assigned).order_by(Drives.logged_in.asc()).all()
        elif filter_code == 9:
            search_filter = Drives.query.order_by(Drives.logged_in.asc()).all()
        elif filter_code == 0:
            search_filter = Drives.query.filter_by(client=client_select, status=status).order_by(
                Drives.deadline.asc()).order_by(Drives.logged_in.asc()).all()

        return render_template('dashboard.html', all_tickets=search_filter, clients=clients.query.all(),
                               show_clients=client_select,
                               title="Drive Bay", now=date.today(), form=form, eval=eval,
                               description="Web interface for support tickets", header=f"{assigned} : {status}",
                               show_status=f"{status}", show_assigned=f"{assigned}")

    return render_template('dashboard.html', all_tickets=Drives.query.filter_by(status='Open').order_by(
        Drives.deadline.asc()).order_by(support_ticket.urgency.asc()).all(),
                           title="Ticket Support", now=date.today(), form=form, eval=eval,
                           description="Web interface for support tickets", header='All Open',
                           show_clients='All Clients', show_status="Open", show_assigned="All")


@drivebay_bp.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if check_user():
        return redirect(url_for('tickets_bp.pending'))

    client_list = [(client.id, client.client) for client in clients.query.all()]
    assigned_list = [(user.id, user.name) for user in User.query.all()]
    form = forms.AddTicket()
    form.client.choices = client_list
    form.assigned.choices = assigned_list
    if request.method == 'POST':
        if form.validate_on_submit():
            new_ticket = support_ticket(
                # client = dict(form.client.choices).get(form.client.data),
                client=str((request.form.get('client'), dict(form.client.choices).get(form.client.data))),
                client_name=request.form.get('client_name'),
                suite=request.form.get('suite'),
                issue=request.form.get('issue'),
                status=request.form.get('status'),
                assigned=str((request.form.get('assigned'), dict(form.assigned.choices).get(form.assigned.data))),
                log=str(log_input(request.form.get('log'), entry_type=0)),
                deadline=request.form.get('deadline'),
                created=datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                last_update=datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                urgency=request.form.get('urgency'),
                created_by='Bob'  # Replace with user_name varible after user function added

            )
            db.session.add(new_ticket)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={new_ticket.id}")

    return render_template('add.html',
                           title="Add Ticket", form=form)


@drivebay_bp.route('/show_ticket/', methods=['POST', 'GET'])
@login_required
def show_drive():
    if check_user():
        return redirect(url_for('drivebay_bp.pending'))

    id = request.args['drive']
    ticket = drives.query.filter_by(id=id).first()
    log = eval(ticket.log)
    client = eval(ticket.client)
    assigned = eval(ticket.assigned)
    return render_template(
        'show_tickets.html',
        ticket=ticket, id=id, client=client[1], assigned=assigned[1],
        title=f"Ticket | {id}", ticket_log=log)


@drivebay_bp.route('/add_client', methods=['POST', 'GET'])
@login_required
def add_client():
    if check_user():
        return redirect(url_for('drivebay_bp.pending'))

    form = forms.AddClient()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_client = clients(
                client=request.form.get('client'),
            )
            db.session.add(new_client)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return render_template('add_client.html',
                                   title="Add Client", form=form, all_clients=Clients.query.all())

    return render_template('add_client.html',
                           title="Add Client", form=form, all_clients=Clients.query.all())


@drivebay_bp.route('/add_client', methods=['POST', 'GET'])
@login_required
def add_status():

    if check_user():
        return redirect(url_for('drivebay_bp.pending'))

    if check_admin():
        return redirect(url_for('drivebay_bp.not_admin'))

    form = forms.AddClient()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_client = clients(
                client=request.form.get('client'),
            )
            db.session.add(new_client)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return render_template('add_client.html',
                                   title="Add Client", form=form, all_clients=Clients.query.all())

    return render_template('add_client.html',
                           title="Add Client", form=form, all_clients=Clients.query.all())


@drivebay_bp.route('/pending', methods=['POST', 'GET'])
def pending():
    return render_template('pending.html')


@drivebay_bp.route('/access_denied', methods=['POST', 'GET'])
def not_admin():
    return render_template('not_admin.html')


@drivebay_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
