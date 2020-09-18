from pprint import pprint

from ad_import.ad import ADObject
from . import LoadAd
from ad_import.models import Query, User


class LoadUsers(LoadAd):
    fields = ['accountExpires',
              'cn',
              'company',
              'department',
              'departmentNumber',
              'description',
              'displayName',
              'distinguishedName',
              'employeeID',
              'employeeNumber',
              'givenName',
              'homeDirectory',
              'homeDrive',
              'ipPhone',
              'lastLogon',
              'logonCount',
              'mail',
              'manager',
              'middleName',
              'mobile',
              'name',
              'objectGUID',
              'objectSid',
              'physicalDeliveryOfficeName',
              'pwdLastSet',
              'sAMAccountName',
              'scriptPath',
              'sn',
              'telephoneNumber',
              'title',
              'userAccountControl',
              'userPrincipalName',
              'whenChanged',
              'whenCreated',
              ]
    model = User

    def __init__(self):
        super().__init__('user')

    def load(self, query: Query):
        base_dn = self.base_dn(query)
        entries = self.ad.ldap_query(query.query,
                                     base_dn,
                                     single_result=False,
                                     subtree=True,
                                     pagination=True,
                                     attributes=self.fields,
                                     result_class=ADObject)

        for user_data in entries:
            user, exist = self.get_object(user_data)

            if user_data.field('userAccountControl') is None:
                pprint(user_data.object)
                continue

            if user_data.numeric('userAccountControl') & 2 == 2:  # Check if account is disabled
                if not exist:
                    print('%s is disabled' % user_data.string('displayName'))
                    continue

            # user.accountExpires = user_data.date('accountExpires')
            user.cn = user_data.string('cn')
            user.company = user_data.string('company')
            user.department = user_data.string('department')
            user.departmentNumber = user_data.string('departmentNumber')
            user.description = user_data.string('description')
            user.displayName = user_data.string('displayName')
            user.distinguishedName = user_data.string('distinguishedName')
            user.employeeID = user_data.string('employeeID')
            user.employeeNumber = user_data.string('employeeNumber')
            user.givenName = user_data.string('givenName')
            user.homeDirectory = user_data.string('homeDirectory')
            user.homeDrive = user_data.string('homeDrive')
            user.ipPhone = user_data.string('ipPhone')
            user.lastLogon = user_data.date('lastLogon')
            user.logonCount = user_data.numeric('logonCount')
            user.mail = user_data.string('mail')
            manager = user_data.string('manager')
            if manager:
                try:
                    user.manager = User.objects.get(directory=self.directory, distinguishedName=manager)
                except User.DoesNotExist:
                    print('Manager %s does not exist' % manager)

            user.middleName = user_data.string('middleName')
            user.mobile = user_data.string('mobile')
            user.name = user_data.string('name')
            user.objectGUID = user_data.bytes('objectGUID')
            user.objectSid = user_data.bytes('objectSid')
            user.physicalDeliveryOfficeName = user_data.string('physicalDeliveryOfficeName')
            user.pwdLastSet = user_data.date('pwdLastSet')
            user.sAMAccountName = user_data.string('sAMAccountName')
            user.scriptPath = user_data.string('scriptPath')
            user.sn = user_data.string('sn')
            user.telephoneNumber = user_data.string('telephoneNumber')
            user.title = user_data.string('title')
            user.userAccountControl = user_data.numeric('userAccountControl')
            user.userPrincipalName = user_data.string('userPrincipalName')
            user.whenChanged = user_data.date_string('whenChanged')
            user.whenCreated = user_data.date_string('whenCreated')

            user.save()
