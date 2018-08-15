
# -*- coding: utf-8 -*-

"""
test projectmanager
"""

import projectmanager


public_key = '' #添加自己的账户公钥
private_key = '' #添加自己的账户私钥

projectManager = projectmanager.ProjectManager(public_key, private_key)

# res = projectManager.createProject("ai test")
# print(res)

# res = projectManager.describeProject()
# print(res)

# res = projectManager.inviteSubaccount('lixiaojun629@ucloud.cn','lixiaojun@pwd','(86)15012344321','lixiaojun')
# print(res)

# res = projectManager.addMemberToProject('org-l1qefx','lixiaojun629@ucloud.cn')
# print(res)

# res = projectManager.describeMemberList('org-l1qefx')
# print(res)

# res = projectManager.removeMemberFromProject('org-l1qefx','lixiaojun629@ucloud.cn')
# print(res)

# res = projectManager.terminateMember('lixiaojun629@ucloud.cn')
# print(res)

# res = projectManager.removeProject('org-l1qefx')
# print(res)