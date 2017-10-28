# -*- coding:utf-8 -*-

# author: songjincheng


import ldap
import hashlib
import os
from ldap import modlist




class LdapApi(object):

    """LDAP 接口"""
    # 初始化一个 ldap 连接实例
    def __init__(self, ldap_host=None, base_dn=None, user=None, password=None):

        if not ldap_host:
            self.ldap_host = ldap_host
        self.base_dn = base_dn
        if not user:
            self.user = user
        if not password:
            self.password = password
        base_user = "cn=%s,%s" % (user, base_dn)
        try:
            self.ldapconn = ldap.initialize(ldap_host)
            self.ldapconn.set_option(ldap.OPT_REFERRALS, 0)
            self.ldapconn.protocal_version = ldap.VERSION3
            self.ldapconn.simple_bind(base_user, password)
        except Exception, e:
            print 'error:'+str(e)




    def make_secret(self,password):

        # Encodes the given password as a base64 SSHA hash+salt buffer

        salt = os.urandom(4)

        # hash the password and append the salt
        sha = hashlib.sha1(password)
        sha.update(salt)

        # create a base64 encoded string of the concatenated digest + salt
        digest_salt_b64 = '{}{}'.format(sha.digest(), salt).encode('base64').strip()

        # now tag the digest above with the {SSHA} tag
        tagged_digest_salt = '{{SSHA}}{}'.format(digest_salt_b64)

        return tagged_digest_salt

    def all_search_dn(self, uid=None):

        # 根据用户检索出相关dn 之后查找dn下所有用户 uid=None 默认查找所有
        obj = self.ldapconn
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        if uid == None or uid == '':
            searchFilter = "uid=*"
        else:
            searchFilter = "uid=" + "*" + uid + "*"
        print searchFilter
        ldap_result_id = obj.search(self.base_dn, searchScope, searchFilter, retrieveAttributes)
        result_set = []
        try:
            while obj:
                result_type, result_data = obj.result(ldap_result_id, 0)
                if result_data == []:
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
            return result_set
        except ldap.LDAPError, e:
            print 'error:'+str(e)

    def search_dn(self, uid=None):

        # 根据用户获取对应dn

        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "uid=" + uid
        try:
            ldap_result_id = obj.search(self.base_dn, searchScope, searchFilter, retrieveAttributes)
            result_type, result_data = obj.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                return result_data[0][0]
            else:
                return None
        except ldap.LDAPError, e:
            print'error-search_dn:' + str(e)

    def search_user(self, uid=None):

        # 获取用户对应信息

        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "uid=" + uid
        try:
            ldap_result_id = obj.search(self.base_dn, searchScope, searchFilter, retrieveAttributes)
            result_type, result_data = obj.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                return result_data
            else:
                return None
        except ldap.LDAPError, e:
            print 'error:' + str(e)

    def ldap_add_user(self, username=None, password=None, ou_name=None, lastname=None, firstname=None):

        # 创建用户

        result = {}
        if username is None or password is None or ou_name is None:
            result['error'] = 'Check the transfer parameters, user name, password, ouname can not be empty.'
            return result

        if self.search_dn(username) is not None:
            result['error'] = 'User %s already exists' % username
            print result
        else:
            try:
                obj = self.ldapconn
                obj.protocal_version = ldap.VERSION3
                uidNumber = self.__get_max_uidNumber()
                addDN = "cn=%s,ou=%s,dc=xianlai,dc=com" % (username, ou_name)
                attrs = {}
                attrs['objectclass'] = [
                    'inetOrgPerson',
                    'posixAccount',
                    'top',
                    'shadowAccount']
                attrs['gecos'] = str(username)
                attrs['shadowMax'] = '99999'
                attrs['shadowWarning'] = '7'
                attrs['mail'] = "%s@xianlai.com" % username
                attrs['cn'] = str(username)
                attrs['givenName'] = str(firstname)
                attrs['homeDirectory'] = '/home/ldap/%s' % username
                attrs['loginShell'] = '/bin/bash'
                attrs['sn'] = str(lastname)
                attrs['uid'] = str(username)
                attrs['uidNumber'] = str(uidNumber)
                attrs['gidNumber'] = '10002'
                attrs['shadowLastChange'] = '16183'
                attrs['userPassword'] = str(self.make_secret(password))

                ldif = modlist.addModlist(attrs)
                obj.add_s(addDN, ldif)
                # obj.unbind_s()
                result = 0
            except ldap.LDAPError, e:
                result['error'] = str(e)
        return result

    def ldap_get_vaild(self, uid=None, passwd=None):

        # 用户验证，根据传递来的用户名和密码，搜索LDAP，返回boolean值

        obj = self.ldapconn
        target_cn = self.search_dn(uid)
        if target_cn is None:
            return None
        else:
            try:
                if obj.simple_bind_s(target_cn, passwd):
                    return True
                else:
                    print "1"
                    return False
            except ldap.LDAPError, e:
                print 'error-ldap_get_vaild:' + str(e) + uid

    def ldap_update_user_password(self, uid, newpass):
        # 修改ldap用户密码
        result = {}
        if uid is None or uid == '' or newpass is None or newpass == '':
            result['error'] = 'Check the transfer parameters, username, password can not be empty.'
        else:
            try:
                obj = self.ldapconn
                obj.protocal_version = ldap.VERSION3
                modifyDN = self.search_dn(uid)
                obj.modify_s(modifyDN, [(ldap.MOD_REPLACE, 'userPassword', [str(self.make_secret(newpass))])])
                result = 0
            except ldap.LDAPError, e:
                result['error'] = str(e)
        return result

    def ldap_delete_user(self,uid=None):
        # 删除ldap用户
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        result = {}
        if uid is None or uid == '':
            result['error'] = 'Check the transfer parameters, username can not be empty.'
        else:
            try:
                deleteDN = self.search_dn(uid)
                print deleteDN
                obj.delete_s(deleteDN)
                result = 0
            except ldap.LDAPError, e:
                result['error'] = u'用户删除失败，原因为: %s' % str(e)
        return result

    def __get_max_uidNumber(self):
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = ['uidNumber']
        searchFilter = "uid=*"

        try:
            ldap_result_id = obj.search(self.base_dn, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while True:
                result_type, result_data = obj.result(ldap_result_id, 0)
                if not result_data:
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(int(result_data[0][1].get('uidNumber')[0]))
            if len(result_set) == 0:
                return 10000
            return max(result_set) + 1
        except ldap.LDAPError, e:
            print u'获取最大uid失败，原因为: %s' % str(e)

    def __get_all_ou(self):
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = ['uidNumber']
        searchFilter = "uid=*"

        try:
            ldap_result_id = obj.search(self.base_dn, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while True:
                result_type, result_data = obj.result(ldap_result_id, 0)
                if not result_data:
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data[0][0].split(',')[1])
            return list(set(result_set))
        except ldap.LDAPError, e:
            print u'获取最大uid失败，原因为: %s' % str(e)

    def get_all_ou(self):
        return self.__get_all_ou()

    def ladp_update_ou(self, uid, new_ou):
        result = {}
        uid_info = self.all_search_dn(uid)
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        try:
            if uid_info:
                attrs = uid_info[0][0][1]
                old_dn = uid_info[0][0][0]
                new_dn = "cn=%s,ou=%s,dc=ixianlai,dc=com" % (uid, new_ou)
                if not self.ldap_delete_user(uid):
                    ldif = modlist.addModlist(attrs)
                    obj.add_s(new_dn, ldif)
                result = 0
            else:
                result['error'] = "error"
        except ldap.LDAPError, e:
            result['error'] = str(e)
        # return result

    def search_uid_ou(self, uid=None,ou=None):

        # 根据用户获取对应dn

        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "uid=" + uid
        try:
            ldap_result_id = obj.search(self.base_dn, searchScope, searchFilter, retrieveAttributes)
            result_type, result_data = obj.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                return result_data[0][0]
            else:
                return None
        except ldap.LDAPError, e:
            print'error-search_dn:' + str(e)

ldap_config = {
    'ldap_host':'ldap://192.168.10.8:389',
    'base_dn':'dc=ixianlai,dc=com',   # dc=ixianlai,dc=com
    'user':'root',                    # root
    'password':'devops!@#xianlai',    # devops!@#xianlai
}







# 创建一个ldap-连接实例
ldap_obj = LdapApi(ldap_config['ldap_host'],ldap_config['base_dn'],ldap_config['user'],ldap_config['password'])

if __name__ == '__main__':
    '''
    CN=Common Name 为用户名或服务器名，最长可以到80个字符，可以为中文；
    OU=Organization Unit为组织单元，最多可以有四级，每级最长32个字符，可以为中文；
    O=Organization 为组织名，可以3—64个字符长
    C=Country为国家名，可选，为2个字符长
    '''
    # 获取用户的信息
    # user_info = ldap_obj.search_user('')
    # 向ldap创建一个用户
    # add_user=ldap_obj.ldap_add_user('songjincheng','123456','devops','宋','小')
    # print(add_user)
    # 验证用户账户和密码
    auth_status=ldap_obj.ldap_get_vaild('xiaosong','xiaosong')
    # print ldap_obj.all_search_dn('songjincheng')
    # print(u'user_info:：',user_info)
    print(u'auth_user_status:',auth_status,11111111,222222,33333333)
    # 获取所有的分组信息
    # print(u'all_ou',ldap_obj.get_all_ou())
    # print(u'获取用户分组信息',ldap_obj.search_uid_ou('songjincheng'))
    # print(u'search_uid_ou',ldap_obj.search_uid_ou('songjincheng','test'))
