from django.db import models 

class UserManager(models.Manager):
    def get_is_user_administrator(self, chat_id):
        return self.filter(chat_id=chat_id).values_list('administrator', flat=True).first()

    def user_exists(self, chat_id):
        return self.filter(chat_id=chat_id).exists()

    def add_user(self, last_name, first_name, patronymic, us_group, username, chat_id):
        self.create(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            us_group=us_group,
            username=username,
            chat_id=chat_id
        )

    def get_full_user_info(self, chat_id):
        return self.filter(chat_id=chat_id).values(
            'last_name', 'first_name', 'patronymic', 'us_group', 'administrator'
        ).first()
    
 
class StaticQuestionManager(models.Manager):
    def get_all_static_question_by_category(self, category_name):
        return self.filter(category__name=category_name).select_related('category')
    
 

class DynamicQuestionManager(models.Manager):
    def add_dynamic_question(self, user_id, description, category_id):
        self.create(
            user_id=user_id,
            description=description,
            category_id=category_id
        )

    def get_dynamic_question_by_category(self, category_name):
        return self.filter(
            category__name=category_name,
            answer=False
        ).select_related('user', 'category').values(
            'user__last_name',
            'user__first_name',
            'user__patronymic',
            'user__us_group',
            'user__username',
            'category__name',
            'description'
        )
     

class QuestionCategoryManager(models.Manager):
    def get_categories(self):
        return self.all().values_list('name', flat=True)

    def get_category_id_by_name(self, category_name):
        return self.filter(name=category_name).values_list('id', flat=True).first()

    def get_name_by_category_id(self, category_id):
        return self.filter(id=category_id).values_list('name', flat=True).first()
    
 

class QuestionSubcategoryManager(models.Manager):
    def get_subcategories_by_category_id(self, category_id):
        return self.filter(
            category_id=category_id
        ).values_list('id', 'name')

    def get_subcategories_description_by_subcategory_id(self, subcategory_id):
        return self.filter(
            id=subcategory_id
        ).values_list('name', 'description').first()
