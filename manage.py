import typer

from scripts.reset_db import reset_db
from scripts.seed import seed

app = typer.Typer()


@app.command()
def seed_database(product_count: int = 100, order_count: int = 1000):
    return seed(product_count, order_count)


@app.command()
def reset_database():
    return reset_db()


if __name__ == "__main__":
    app()
