""""""
"""
分页组件
使用步骤：
   def num_manage(request):
   # 1.根据实际情况筛选数据
    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        data_list['mobile__contains'] = search_data
    queryset = models.PrettyNum.objects.filter(**data_list).order_by('-status', '-level', )

    # 2.实例化分页对象
    page_obj = Pagination(request, queryset, page_size=16)
    return render(request, 'num_manage.html', {

    'search_data': search_data,   # 搜索框保留的数据，根据实际情况添加

    'num_list': page_obj.page_queryset,  # 分完页的数据
    'page_list_string': page_obj.show_page(),  # 生成的页码
    'page_num': page_obj.page_num,  # 尾页，可根据实际情况添加

})


在html中：
    1.展示数据：循环queryset,大致代码如下：

    <div class="panel panel-default">
        <div class="panel-heading">
            号码列表
        </div>
        <table class="table table-bordered">
            <thead>
            <tr>
                <th>ID</th>
                <th>号码</th>
                <th>价格</th>
                <th>级别</th>
                <th>状态</th>
                <th>操作</th>

            </tr>
            </thead>
            <tbody>
            {% for obj in num_list %}
                <tr>
                    <td>{{ obj.id }}</td>
                    <td>{{ obj.mobile }}</td>
                    <td>{{ obj.price }}</td>
                    <td>{{ obj.get_level_display }}</td>
                    <td>{{ obj.get_status_display }}</td>
                    <td><a href="/num/{{ obj.id }}/edit" class="btn btn-primary btn-xs">编辑</a>&nbsp;&nbsp;<a
                            href="/num/{{ obj.id }}/delete" class="btn btn-danger btn-xs">删除</a></td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    
    2.展示分页框
    <div class="container" style="text-align: center;">
            <ul class="pagination" style="margin: 0 auto">
            <li>
                <a href="?page=1" aria-label="Previous">
                    <span aria-hidden="true">首页</span>
                </a>
            </li>
            {{ page_list_string }}
            <li>
                <a href="?page={{ page_num }}" aria-label="Next">
                    <span aria-hidden="true">尾页</span>
                </a>
            </li>
        </ul>
    </div>
"""

import copy
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=16, page_param='page', page_length=3):
        """
        request:请求的对象
        queryset：符合条件的数据（根据此数据进行分页处理）
        page_size:每页显示的数据
        page_param:获取分页的参数：?page=13
        page_length:显示当前页的前（后）几页
        """
        queryset_dict = copy.deepcopy(request.GET)
        queryset_dict._mutable = True
        self.query_dict = queryset_dict

        page = request.GET.get(page_param, '1')
        page = int(page) if page.isdecimal() else 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        # 分页的queryset
        self.page_queryset = queryset[self.start:self.end]
        # 计算页码
        self.data_count = queryset.count()
        self.page_param = page_param
        page_num, num = divmod(self.data_count, page_size)
        if num:
            page_num += 1
        self.page_num = page_num
        self.page_length = page_length

    def show_page(self, ):
        """
        展示页码，将html代码导入到html文件中
        """
        page_list = []
        start_page = self.page - self.page_length
        end_page = self.page + self.page_length
        # 数据库数据少的时候

        if self.data_count <= self.page_length * 2 + 1:
            start_page = 1
            end_page = self.page_length * 2 + 1
        # 数据库数据太多
        else:
            # 极值处理（前）
            if self.page - self.page_length < 1:
                start_page = 1
                end_page = self.page_length * 2 + 1
            # 极值处理（后）
            if self.page + self.page_length > self.page_num:
                end_page = self.page_num
                start_page = self.page_num - self.page_length * 2

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        ele = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_list.append(ele)
        # 如果默认展示页码数小于总页码数（常规情况）
        if self.page_length * 2 + 1 < self.page_num:
            for i in range(start_page, end_page + 1):
                self.query_dict.setlist(self.page_param, [i])
                if i == self.page:
                    ele = '<li class = "active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                else:
                    ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                page_list.append(ele)
        # 默认展示页码数大于等于总页码数（数据太少时）
        else:
            for i in range(1, self.page_num + 1):
                self.query_dict.setlist(self.page_param, [i])
                if i == self.page:
                    ele = '<li class = "active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                else:
                    ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                page_list.append(ele)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.page_num])
        ele = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_list.append(ele)
        page_list_string = mark_safe("".join(page_list))
        return page_list_string
