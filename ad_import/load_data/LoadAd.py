from abc import ABC

from django.db.models import Model, QuerySet

from ad_import.ad import ADObject, ActiveDirectory
from ad_import.models import Directory, Query


class LoadAd(ABC):
    directory: Directory = None
    model = Model

    def __init__(self, object_type):
        self.ad = ActiveDirectory()
        self.object_type = object_type

    def connect(self, directory_name):
        directory = Directory.objects.get(name=directory_name)
        self.directory = directory
        self.ad.connect(dc=directory.dc,
                        username=directory.username,
                        password=directory.password,
                        base_dn=directory.dn,
                        ldaps=directory.ldaps)

    @staticmethod
    def base_dn(query: Query) -> str:
        if query.base_dn:
            return query.base_dn
        else:
            return query.directory.dn

    def get_object(self, entry: ADObject):
        """
        Get django object for a LDAP entry
        Use SID to check for existing objects in database
        :param entry:
        :return:
        """
        try:
            user = self.model.objects.get(directory=self.directory, objectSid=entry.bytes('objectSid'))
            exist = True
        except self.model.DoesNotExist:
            user = self.model(directory=self.directory)
            exist = False

        return user, exist

    @property
    def queries(self) -> QuerySet[Query]:
        """
        Get queries from the current directory
        :return: Queries
        """
        return self.directory.queries.filter(type=self.object_type)

    @staticmethod
    def is_disabled(entry: ADObject):
        if entry.field('userAccountControl') is None:
            return None

        return entry.numeric('userAccountControl') & 2 == 2  # Check if account is disabled