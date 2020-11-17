"""Data models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    account_type = db.Column(
        db.String(6),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Drives(db.Model):
    """Data model for drive entries."""

    __tablename__ = 'drives'
    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )
    tag = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )
    drive_name = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )
    client = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )
    drive_serial = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    location = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    status = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    assigned = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    notes = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )

    logged_in = db.Column(
        db.String(20),
        index=False,
        unique=False,
        nullable=False
    )

    last_update = db.Column(
        db.String(20),
        index=False,
        unique=False,
        nullable=False
    )


    def __repr__(self):
        return '<drive {}>'.format(self.id)


class Clients(db.Model):
    """Data model for client profiles."""

    __tablename__ = 'clients'
    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )
    client = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '{}'.format(self.client)

    def __str__(self):
        return '{}'.format(self.client)


class Status(db.Model):
    """Data model for status values."""

    __tablename__ = 'status'
    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )
    status = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '{}'.format(self.client)

    def __str__(self):
        return '{}'.format(self.client)