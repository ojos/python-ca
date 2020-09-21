from ojos_ca.infra.kvs.redis import Redis
from ojos_ca.interface.repo.kvs.redis import (
    SeqRedisRepo, SysVarRedisRepo
)
from ojos_ca.usecase.serializer.sys import (
    SeqJsonSerializer, SysVarJsonSerializer
)


class SeqRedisRepoFactory(object):
    @staticmethod
    def get(host: str='localhost', port: int=6379, db: int=0) -> SeqRedisRepo:
        return SeqRedisRepo(Redis.get(host, port, db), SeqJsonSerializer)


class SysVarRedisRepoFactory(object):
    @staticmethod
    def get(host: str='localhost', port: int=6379, db: int=0) -> SysVarRedisRepo:
        return SysVarRedisRepo(Redis.get(host, port, db), SysVarJsonSerializer)


# class SystemVariableYamlRepoFactory(object):
#     @staticmethod
#     def get() -> SystemVariableYamlRepo:
#         for dir_path in settings.FIXTURE_DIRS:
#             client = LocalFile('{}system_variable.yml'.format(dir_path))
#             if client.exists():
#                 break
#         return SystemVariableYamlRepo(client, SystemVariableSerializer)


# class SystemVariableRepoFactory(object):
#     @staticmethod
#     def get() -> SystemVariableRepo:
#         db_repo    = SystemVariableDatabaseRepoFactory.get()
#         cache_repo = SystemVariableRedisRepoFactory.get()
#         file_repo  = SystemVariableYamlRepoFactory.get()
#         return SystemVariableRepo(db_repo, cache_repo, file_repo)