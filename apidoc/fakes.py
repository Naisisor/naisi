"""
@Author: Naisisor
"""
import json

from faker import Faker

from apidoc.extensions import db
from apidoc.models import User, Project, System

fake = Faker()


def fake_admin():
    admin = User(
        email=f'admin@{fake.free_email_domain()}',
        username='admin',
        name='admin'
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()


def fake_projects(count=50):
    user = User.query.first()
    for i in range(count):
        project = Project(
            name=fake.name(),
            desc=fake.text(200),
            domains=json.dumps([{'env': fake.domain_word(), 'name': fake.domain_name()}]),
            supporter_id=user.id
        )
        db.session.add(project)
    db.session.commit()


def fake_systems(count=50):
    user = User.query.first()
    for i in range(count):
        system = System(
            name=fake.name(),
            desc=fake.text(200),
            domains=json.dumps([{'env': fake.domain_word(), 'name': fake.domain_name()}]),
            supporter_id=user.id
        )
        db.session.add(system)
    db.session.commit()
