from schematics.transforms import to_native


class AbstractQuerySet(object):
    """
    """

    MSG_OK = 'OK'
    MSG_CREATED = 'Created'
    MSG_READ = 'Read'
    MSG_UPDATED = 'Updated'
    MSG_DELETED = 'Deleted'
    MSG_NOTFOUND = 'Not Found'
    MSG_FAILED = 'Failed'

    def __init__(self, db_conn=None, api_id='id'):
        self.db_conn = db_conn
        self.api_id = api_id

    ### Create

    def create(self, cls, data):
        if isinstance(data, list):
            return self.create_many(cls, data)
        else:
            return self.create_one(cls, data)

    def create_one(self, cls, datum):
        raise NotImplementedError

    def create_many(self, cls, data):
        raise NotImplementedError

    ### Read

    def read(self, cls, ids=None):
        """Returns a list of items that match ids
        """
        if not ids:
            return self.read_all(cls)
        elif isinstance(ids, list):
            return self.read_many(cls, ids)
        else:
            return self.read_one(cls, ids)

    def read_all(self, cls):
        raise NotImplementedError

    def read_one(self, cls, iid):
        raise NotImplementedError

    def read_many(self, cls, ids):
        raise NotImplementedError

    ### Update

    def update(self, cls, data):
        if isinstance(data, list):
            return self.update_many(cls, data)
        else:
            return self.update_one(cls, data)

    def update_one(self, cls, datum):
        raise NotImplementedError

    def update_many(self, cls, data):
        raise NotImplementedError

    ### Destroy

    def destroy(self, cls, ids):
        if isinstance(ids, list):
            return self.destroy_many(cls, ids)
        else:
            return self.destroy_one(cls, ids)

    def destroy_one(self, cls, iid):
        raise NotImplementedError

    def destroy_many(self, cls, ids):
        raise NotImplementedError


class DictQuerySet(AbstractQuerySet):
    """This class exists as an example of how one could implement a Queryset.
    This model is an in-memory dictionary and uses the model's id as the key.

    The data stored is the result of calling `to_native()` on the model.
    """
    def __init__(self, **kw):
        super(DictQuerySet, self).__init__(db_conn=dict(), **kw)

    ### Create

    def create_one(self, cls, datum):
        if datum['id'] in self.db_conn:
            status = self.MSG_UPDATED
        else:
            status = self.MSG_CREATED
        datum_key = str(getattr(datum, self.api_id))
        self.db_conn[datum_key] = to_native(cls, datum)
        return (status, datum)

    def create_many(self, cls, data):
        results = [self.create_one(cls, datum) for datum in data]
        return results

    ### Read

    def read_one(self, cls, iid):
        iid = str(iid)
        if iid in self.db_conn:
            return (self.MSG_READ, self.db_conn[iid])
        else:
            return (self.MSG_NOTFOUND, iid)

    def read_all(self, cls):
        return [self.read_one(cls, iid) for iid in self.db_conn.keys()]

    def read_many(self, cls, ids):
        results = [self.read_one(cls, iid) for iid in ids]
        return results        

    ### Update
    
    def update_one(self, cls, datum):
        datum_key = str(getattr(datum, self.api_id))
        self.db_conn[datum_key] = to_native(cls, datum)
        return (self.MSG_UPDATED, datum)

    def update_many(self, cls, data):
        results = [self.update_one(cls, datum) for datum in data]
        return results

    ### Destroy

    def destroy_one(self, cls, iid):
        try:
            datum = self.db_conn[iid]
            del self.db_conn[iid]
        except KeyError:
            raise FourOhFourException
        return (self.MSG_UPDATED, datum)

    def destroy_many(self, cls, ids):
        results = [self.destroy_one(cls, iid) for iid in ids]
        return results

