"""
帮助文档
"""
"""
1.钩子方法校验后还可在if form.is_valid():中使用：
form.add_error('字段','错误信息')
手动抛出错误。
2.layout布局模板可多使用{{}}/{% %}等语法，自由度较高
3.写登录表单时用form就行了，没必要在去model里新建一个类
4.声明数据库时如：
model = models.Admin
Admin类不可调用，不需要加括号
"""