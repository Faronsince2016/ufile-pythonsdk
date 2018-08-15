# -*- coding: utf-8 -*-

from baseuaccount import BaseUAccount
from ucloud.logger import logger
from ucloud.auth import Auth
from ucloud.util import _check_dict
from ucloud.uaccount.httprequest import _get, _post

class ProjectManager(BaseUAccount):
    """
    UCloud UAccount 项目/账号管理类
    """


    def __init__(self, public_key, private_key):
        """
        初始化 ProjectManager 实例

        @param public_key: string类型， 账户API公私钥的公钥
        @param private_key: string类型，账户API公私钥的私钥
        @return None，如果为非法的公私钥则抛出ValueError异常
        """
        super(ProjectManager, self).__init__(public_key, private_key)


    def createProject(self, projectname):
        """
        创建新的项目

        @param projectname: string 类型，请求参数
        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码，ProjectId:所创建项目的ID（目前返回的不对，已内部沟通，最迟下周二修复（2018.8.20））}
        """

        payload = dict()
        payload['Action'] = 'CreateProject'
        payload['ProjectName'] = projectname
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('create project {0}'.format(projectname))
        print(payload)
        return _post(payload)


    def describeProject(self):
        """
        获取项目列表

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码，ProjectCount: 项目总数，ProjectSet: array, 项目列表}
        PorjectSet: [{
            ProjectId: 项目ID
            ProjectName: 项目名称
            ParentId: 父项目ID
            ParentName: 父项目名称
            CreateTime: 创建时间（unix时间戳)
            IsDefault: 是否为默认项目 bool
            ResourceCount: 项目下资源数量
            MemberCount: 项目下成员数量 
        }...]
        """

        payload = dict()
        payload['Action'] = 'GetProjectList'
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('describe project')
        return _post(payload)

    def removeProject(self, projectId):
        """
        删除项目
        @param projectId string 项目ID

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码}
        """

        payload = dict()
        payload['Action'] = 'TerminateProject'
        payload['ProjectId'] = projectId
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('remove project')
        return _post(payload)


    def inviteSubaccount(self, email, password, phone, userName, isFinance="false"):
        """
        邀请项目成员

        @param email string 用户邮箱
        @param password  string  密码
        @param phone string 手机号 如：(86)15012344321
        @param userName string  用户姓名
        @param isFinance string 是否为财务人员（可以申请开发票等，默认为'false'）

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码}
        """

        payload = dict()
        payload['Action'] = 'InviteSubaccount'
        payload['UserEmail'] = email
        payload['UserPwd'] = password
        payload['UserPhone'] = phone
        payload['UserName'] = userName
        payload['IsFinance'] = isFinance
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('describe project')
        return _post(payload)

    def addMemberToProject(self, projectId, memberEmail, characterId='Admin'):
        """
        把账号添加到特定项目

        @param projectId string 项目ID (来自于GetProjectList)
        @param characterId string  角色ID, 默认Admin  Admin角色默认存在，拥有ucloud所有开放产品权限，可以创建新角色，给角色特定产品权限
        @param memberEmail string 被添加账号的邮箱 

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码}
        """
        payload = dict()
        payload['Action'] = 'AddMemberToProject'
        payload['ProjectId'] = projectId
        payload['CharacterId'] = characterId
        payload['MemberEmail'] = memberEmail
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('add member to project')
        return _post(payload)


    def describeMemberList(self, projectId, offset='0', limit='200'):
        """
        查询某项目成员列表

        @param projectId string 项目ID
        @param offset string 偏移量 默认0
        @param limit string 请求数量 默认200

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码, TotalCount:成员总数，MemberSet: 成员列表}
        MemberSet:[{
            MemberEmail: 成员邮箱
            MemberPhone: 成员手机
            MemberName: 成员名字
            MemberPosition: 成员地址
            MemberQQ：成员QQ
            PublickKey: 公钥
            LastRegionId:机房ID
            DefaultProjectId: 默认项目
            LastLogin: 最近一次登录时间
            Created: 创建时间
            State: 状态
            IsAdmin: 是否主账号
            IfFinance: 是否有财务权限
            ProjectSet: 项目列表 [{ProjectName:项目名，ProjectId:项目ID, CharacterId:角色ID}]
        }]
        """
        payload = dict()
        payload['Action'] = 'DescribeMemberList'
        payload['ProjectId'] = projectId
        payload['Offset'] = offset
        payload['Limit'] = limit
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('describe member list')
        return _post(payload)


    def removeMemberFromProject(self, projectId, memberEmail):
        """
        从项目中移除成员，移除后成员账号还在，但不能访问项目资源，可以添加到另一个项目中

        @param projectId string 项目ID
        @param memberEmail string 被移除账号的邮箱

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码}
        """
        payload = dict()
        payload['Action'] = 'RemoveMemberFromProject'
        payload['ProjectId'] = projectId
        payload['MemberEmail'] = memberEmail
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('remove member from project')
        return _post(payload)


    def terminateMember(self, memberEmail):
        """
        注销账号，注销后，账号消失不存在，原手机号邮箱可注册（或受邀请）成为新账号 

        @param memberEmail string 被注销账号的邮箱

        @return jsonbody: 如果http状态码不为200 或者RetCode不为0，则抛出异常；否则返回dict类型
        @return dict {Action: 操作名称，RetCode: 返回码}
        """
        payload = dict()
        payload['Action'] = 'TerminateMember'
        payload['MemberEmail'] = memberEmail
        payload['PublicKey'] = self.getPublicKey()
        signature = self.signature(payload)
        payload['Signature'] = signature
        logger.info('terminate member')
        return _post(payload)