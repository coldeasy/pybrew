from storm.locals import Unicode, DateTime, Int
from zappa.core import repo


class MetricsModel(object):
    __storm_table__ = 'metrics'
    __storm_primary__ = '_id'
    _id = Int()
    key = Unicode()
    value = Unicode()
    timestamp = DateTime()


class MetricsRepo(repo.Repo):
    @repo.db_operation()
    def store_metric(self, key, value):
        store = self._get_db_store()
        model = MetricsModel()
        model.key = key
        model.value = value
        store.add(model)
        self.commit()
