from db.conn import DbConnection
import typer


app = typer.Typer()


@app.command()
def gettasks(tablename: str):
    conn = DbConnection()


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    conn = DbConnection()
    print(conn.execute("SELECT * FROM users;", get="one"))
