import click
from flask.cli import FlaskGroup
from project.server import create_app, db, bcrypt

app = create_app()
cli = FlaskGroup(create_app=create_app)


@app.cli.command("set-admin-password")
@click.option("--username", required=True, help="Username to set the password for")
@click.password_option()
def set_admin_password(username, password):
    """Set or update the password for a user (creates a bcrypt hash)."""
    from project.server.models.models import Users
    user = Users.query.filter_by(username=username).first()
    if not user:
        click.echo(f"ERROR: user '{username}' not found")
        raise SystemExit(1)
    user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.commit()
    click.echo(f"OK: password updated for '{username}'")


if __name__ == "__main__":
    cli()
