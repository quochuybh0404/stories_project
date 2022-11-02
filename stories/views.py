from django.shortcuts import render
from stories.models import Category, Stories, Contact
from stories.forms import FormContact
from django.core.paginator import Paginator
import re

# Create your views here.


def index(request):
    newest_1 = Stories.objects.order_by('-public_day')[0]
    newest_4 =  Stories.objects.order_by('-public_day')[1:5]
    videos = Stories.objects.order_by('-public_day')

    c1 = Category.objects.get(pk = 1)
    young_children = Stories.objects.filter(Category = c1).order_by('-public_day')

    c2 = Category.objects.get(pk = 2)
    older_children = Stories.objects.filter(Category = c2).order_by('-public_day')

    # Đọc cookies
    value = 0
    if request.COOKIES.get('visit'):
        value = int(request.COOKIES.get('visit')) # Giá trị nhận được ở lần đầu tiên truy cập là: 1
    visit_string = 'You have visited this page ' + str(value) + ' times.'


    reponse = render(request, 'stories/index.html',{
        'newest_1': newest_1,
        'newest_4' : newest_4,
        'young_children': young_children,
        'older_children': older_children,
        'videos': videos,
        'visit_string': visit_string,
        })

    # lưu cookies
    reponse.set_cookie('visit', value + 1) # visit là tên của cookies do mình tự đặt

    return reponse

def category(request, pk):
    stories = Stories.objects.filter(Category = pk)
    title = Category.objects.get(id = pk)

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(stories, 3) # Biến thứ 1: tổng  số cuốn truyện, biến thứ 2: 3 cuốn trên 1 trang
                                      # 6/3 = 2 trang
    stories_pager = paginator.page(page)

    return render(request, 'stories/category.html',{
        'stories':stories_pager,
        'title': title,
    })

def search(request):
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')

        stories = Stories.objects.all().values() # Danh sách chứa các dict. Mỗi cuốn truyện là một dict
        id_stories = []
        for story in stories: # story --> dictionary
            story['content'] = re.sub(r'<[^<]+?>', '', story['content']) # Loại bỏ tag html
            if keyword.lower() in story['name'].lower() or keyword.lower() in story['content']:
                id_stories.append(story['id'])
        else:
            stories_search = Stories.objects.filter(id__in = id_stories).order_by('-public_day')
            title_search = 'Searched'
    return render(request, 'stories/category.html', {
        'stories': stories_search,  # vẫn sử dụng chung biến stories để nhờ vòng lặp duyệt dùm khi mình tìm kiếm
        'title_search': title_search,
        'keyword': keyword
    })

def contact(request):
    result = ''
    if request.POST.get("btnSend"): # Khi tôi click vào cái nút tên là "btnSend" thì:
        # Gán biến
        name = request.POST.get("name") # thì tôi sẽ có giá trị của cái ô tên là name
        email = request.POST.get("email") # và giá trị của cái ô tên là email, các ô còn lại tương tự
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        
        # Khởi tạo class Contact
        contact = Contact(name = name, email = email, subject = subject, message = message)
        contact.save()
        
        result = '''
                <div class="alert alert-success" role="alert">
                    Gửi thông tin thành công
                </div>
            '''

    return render(request, 'stories/contact.html',{
        'result': result
    })

def contact_2(request):
    form = FormContact()
    result = ''
    if request.POST.get('btnSend'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            request.POST._mutable = True
            post = form.save(commit = False) # lưu tạm trên RAM chưa có ghi vào cơ sở dữ liệu
            post.name = form.cleaned_data['name'] 
            # post.name là những giá trị nằm trong model còn clean_data['name'] là nằm trong forms (name)
            # Nó sẽ so với model trong csdl và cái bạn nhập trong form nếu hợp lệ thì thì nó sẽ gán dự liệu từ form vô model
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save() # Ghi vào cơ sở dữ liệu

            result = '''
                <div class="alert alert-success" role="alert">
                    Gửi thông tin thành công
                </div>
            '''

    return render(request, 'stories/contact_2.html',{
        'form': form,
        'result': result,
    })

def story(request, pk):
    story = Stories.objects.get(id = pk)  # Hàm get chỉ trả ra cho mình 1 giá trị trong danh sách thôi
    return render(request, 'stories/story.html',{
        'story':story,
    })

