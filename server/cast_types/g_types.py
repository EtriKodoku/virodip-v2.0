from sqlalchemy.orm import Session


# This file is for casting db session type to g.db variable
# so that we can have type hints in our routes
# Usage:
# db: DbSessionType = cast(DbSessionType, g.db)
# db.query(...)
DbSessionType = Session  # g.db
