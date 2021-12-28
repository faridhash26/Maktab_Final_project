from django.urls import path
from .views import PostPage, HomePage, AboutPage, ContactPage, Category_filter, adding_new_category, admin_dashbord, all_category, all_tags, category_edit, createTag, delete_category_form, delete_tag, edit_tag, login_view, logout_view, myRegister, new_comment, new_post, post_delete, post_edit, search_page

# the urls
app_name = 'post'
urlpatterns = [
    path('', HomePage, name='home'),
    path('posts/<str:category>/', Category_filter),
    path('about/', AboutPage, name='about'),
    path('contact/', ContactPage, name='contact'),
    path('post/<slug:slug>/', PostPage.as_view(), name='post_detail'),
    path('login/', login_view, name="login"),
    path('register/', myRegister, name="register"),
    path('logout/', logout_view, name='logout'),
    path('categorys/', all_category, name='category'),
    path('categoryedit/<int:cat_id>', category_edit, name='category_edit'),
    path('newcategory/', adding_new_category, name='newcategory'),
    path('deletecategory/<int:cat_id>',
         delete_category_form, name="deletecategory"),
    path('userdashbord/', admin_dashbord, name="userdashbord"),
    path('newpost/', new_post, name="newpost"),
    path('deletepost/<int:postid>', post_delete, name="deletepost"),
    path('editpost/<int:postid>', post_edit, name='editpost'),
    path('newcomment/<int:postid>', new_comment, name="newcomment"),
    path('search/', search_page, name='search'),
    path('tags/', all_tags, name="alltags"),
    path('newtag/', createTag, name="newtag"),
    path('edittag/<int:tagid>', edit_tag, name='tag_edit'),
    path('deletetag/<int:tagid>', delete_tag, name="deletetag")

]
