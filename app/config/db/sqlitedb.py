from pydantic import BaseModel


class SqliteDB(BaseModel):
    path: str = "app.db"
    timezone: str = "Europe/Moscow"
    dialect: str = "aiosqlite"
    database: str = "app"

    def __str__(self):
        return f"{self.path}"

    @property
    def url(self):
        return (f"sqlite+{self.dialect}:///"
                f"{self.path}")

    @property
    def sync_url(self):
        return (f"sqlite://"
                f"{self.path}")
    