import yaml
import sys

class Session:

    def __init__(self):
        self.load_yamls()
        self.add_commands()
        self.cart = []       

    def load_yamls(self):
        with open('c:/temp/menu.yaml', encoding='utf-8', mode='r') as file:
            self.menu = yaml.load(file.read(), Loader=yaml.FullLoader)
        
        with open('c:/temp/customer.yaml', encoding='utf-8', mode='r') as file:
            self.customer = yaml.load(file.read(), Loader=yaml.FullLoader)
        
        with open('c:/temp/options.yaml', encoding='utf-8', mode='r') as file:
            self.options = yaml.load(file.read(), Loader=yaml.FullLoader)
        
        #with open('c:/temp/cart.yaml', encoding='utf-8', mode='r') as file:
            #self.cart = yaml.load(file.read(), Loader=yaml.FullLoader)
        
        with open('c:/temp/welcome.yaml', encoding='utf-8', mode='r') as file:
            self.welcome = yaml.load(file.read(), Loader=yaml.FullLoader)
        
        with open('c:/temp/bye.yaml', encoding='utf-8', mode='r') as file:
            self.bye = yaml.load(file.read(), Loader=yaml.FullLoader)

        with open('c:/temp/nl.yaml', encoding='utf-8', mode='r') as file:
            self.nl = yaml.load(file.read(), Loader=yaml.FullLoader)
   
    def add_commands(self):
        commands = {}
        commands['p'] = self.show_cart
        commands['m'] = self.show_menu
        commands['f'] = self.show_bye
        commands['s'] = sys.exit
        self.commands = commands
   
    def get_menu_items(self, message, menu_items):
        for id, item in message.items():
            if str(id).isnumeric():
                equal_position = len(item)+1 if item.find('=')==-1 else item.find('=')
                item_name = item[:equal_position-1]
                item_price = item[equal_position+4:] or 0.0
                menu_items.append({id:{"name": item_name, "price": item_price}})
            if type(item) is dict:
                self.get_menu_items(item, menu_items)
        return menu_items

    def render(self, message):
        if type(message) is dict:
            for id, item in message.items():

                if type(item) is not dict:
                    print(f'{id}:', item)
                else:
                    print(f'\n{id.upper()}:')

                if type(item) not in (list, dict):
                    pass
                else:
                    self.render(item)

        elif type(message) is list:
            for item in message:
                if type(item) not in (list, dict):
                    pass
                else:
                    render(item)
        else:
            print(message)       

    def show_linebreak(self):
        self.render(self.nl)
    
    def show_welcome(self):
        self.render(self.welcome)
    
    def show_customer(self):
        self.render(self.customer)
    
    def show_cart(self):
        for n, item in enumerate(self.cart):
            cart_item = self.get_menu_items(self.menu, [])[item]
            print(cart_item, '-', item)
            #print(f"{n+1}- {cart_item['name']} - {cart_item['price']}")
    
    def show_menu(self):
        self.render(self.menu)

    def show_options(self):
        self.render(self.options)
    
    def show_bye(self):
        self.render(self.bye)
        sys.exit(0)
    
    def exit(self):
        sys.exit(0)
    
    def repl(self):
        nl = self.show_linebreak
        self.show_customer()
        nl()
        self.show_welcome()
        nl()
        self.show_cart()
        nl()
        self.show_menu()
        nl()
        self.show_options()
        entry = ''
        while True:
            entry = input('?').lower()
            if entry[0].isnumeric(): 
                entry = int(entry[0])
                # adding item to the cart
                self.cart.append(entry)
            else:
                # a letter option was choosen
                self.show_linebreak()
                self.commands[entry]()
                self.show_options()
        self.show_bye()

if __name__ == '__main__':
    s = Session()
    s.repl()
