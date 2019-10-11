from invoicing.ui.menu import Menu
from invoicing.ui.pagination import Pagination
from invoicing.ui.style import Style


class Relationship:

    @staticmethod
    def select_foreign_key_relationship(relationship):
        repository = relationship.repository()
        print(Style.create_title('Select %s' % relationship.name))
        paginated_menu = relationship.paginated_menu or Pagination(repository)
        item = paginated_menu()
        if item:
            return item[0]
        else:
            return False

    @staticmethod
    def select_foreign_key_relationship_inverse(relationship):
        foreign_keys = []
        repository = relationship.repository()
        while Menu.yes_no_question('Add %s' % relationship.name):
            print(Style.create_title('Select %s' % relationship.name))
            paginated_menu = relationship.paginated_menu or Pagination(repository)
            item = paginated_menu()
            if item:
                foreign_keys.append(item['id'])
            else:
                print('\nNo relationship added\n')
        return relationship.related_name, foreign_keys
