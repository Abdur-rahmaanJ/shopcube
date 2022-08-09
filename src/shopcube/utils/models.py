"""
DB-related helper utilities. Taken from database.py
file at https://github.com/cookiecutter-flask/cookiecutter-flask
"""
from init import db


class CRUDMixin:
    """
    Mixin that adds convenience methods for
    CRUD (create, read, update, delete) operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it in the database.

        Returns:
            DB Class Object: returns the created record
        """
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record

        Args:
            commit (bool, optional): flag whether to commit. Defaults to True.

        Returns:
            Db Class object: returns the updated record if committed,
            None otherwise
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            self.save()
            return self
        return None

    def save(self, commit=True):
        """Save the record.

        Args:
            commit (bool, optional): flag whether to commit. Defaults to True.

        Returns:
            Db Class object: returns the record saved to db session
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database.

        Args:
            commit (bool, optional): flag whether to commit. Defaults to True.

        Returns:
            Db Class object: returns the updated record if committed,
            None otherwise
        """
        db.session.delete(self)
        if commit:
            db.session.commit()
            return self
        return None


class YoModel(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(YoModel):
    """
    Base model class that includes CRUD convenience methods,
    plus adds a 'primary key' column named 'id'.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID.

        Args:
            record_id (int): ID of record to get

        Returns:
            DB Class object: object identified by record_id if any,
            None otherwise
        """
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None
