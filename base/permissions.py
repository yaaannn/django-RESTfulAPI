from rest_framework import permissions
'''
AllowAny 允许所有用户
IsAuthenticated 仅通过认证的用户
IsAdminUser 仅管理员用户
IsAuthenticatedOrReadOnly 认证的用户可以完全操作，否则只能get读取
'''
'''
.has_permission(self, request, view)
是否可以访问视图， view表示当前视图对象，如果没有设置的话默认的是True，如果设置
False则表示所有的用户都不能访问该视图

.has_object_permission(self, request, view, obj)
是否可以访问数据对象， view表示当前视图， obj为数据对象，控制视图能够访问添加了权限控制类的数据对象
'''
# test
'''
class MyPermission(BasePermission):
	def has_permission(self, request, view)
		"""让所有用户都有权限"""
		return True
    def has_object_permission(self, request, view, obj):
        """用户是否有权限访问添加了权限控制类的数据对象"""
        # 需求：用户能够访问id为1，3的对象，其他的不能够访问
        if obj.id in (1, 3):
        	return True
        else:
        	return False
'''
'''
mixins.CreateModelMixin	    create   POST	  创建数据
mixins.RetrieveModelMixin	retrieve GET	  检索数据
mixins.UpdateModelMixin	    update   PUT	  更新数据
mixins.DestroyModelMixin	destroy  DELETE	  删除数据
mixins.ListModelMixin	    list     GET	  获取数据
'''

# test
class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        # def has_permission(self, request):
        return bool(request.auth)

    # 官方的只有('GET', 'HEAD', 'OPTIONS')会流向这里，还没找出原因
    def has_object_permission(self, request, view, obj):
        print('权限测试模块')
        print('对应表类的名称：',(str(obj).split(' '))[0])
        # 可以在这里做后端权限验证
        print(request.user)
        print(view.action)
        print(permissions.SAFE_METHODS)
        return True


# 重写基本认证类，让所有的请求类型都流向这里，方便后面的动态权限认证
class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print('权限测试模块')
        print(request.user)
        print(view.action)
        return bool(request.auth)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print('权限测试模块')
        print('对应表类的名称：',(str(obj).split(' '))[0])
        # 可以在这里做后端权限验证
        print(request.user)
        print('请求的方法：',view.action)
        return True