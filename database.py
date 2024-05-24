import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.load()


    def load(self):
        self.users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(';')
                    if len(parts) >= 4:
                        email, password, name, date = parts[:4]
                        fridge_items = parts[4:]
                        self.users[email] = {'password': password, 'name': name, 'date': date, 'fridge_items': fridge_items}
                    else:
                        print(f"Ignoring line: {line.strip()} - Insufficient data.")
        except FileNotFoundError:
            print("File not found or empty.")








    def save(self):
        with open(self.filename, "w") as f:
            for email, data in self.users.items():
                password = data['password']
                name = data['name']
                date = data['date']
                fridge_items = data['fridge_items']
                f.write(f"{email};{password};{name};{date};{';'.join(fridge_items)}\n")


    def get_user(self, email):
        return self.users.get(email, {})


    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = {'password': password.strip(), 'name': name.strip(), 'date': self.get_date(), 'fridge_items': []}
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1


    def validate(self, email, password):
        user_data = self.get_user(email)
        return user_data.get('password') == password if user_data else False
   
    def email_exists(self, email):
        with open(self.filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == email:
                    return True
        return False


    def get_fridge_items(self, user_email):
        user_data = self.get_user(user_email)
        return user_data.get('fridge_items', []) if user_data else []


    def add_item_to_fridge(self, email, item):
        user_data = self.get_user(email)
        if user_data:
            fridge_items = user_data['fridge_items']
            fridge_items.append(item)
            user_data['fridge_items'] = fridge_items
            self.save()
            return True
        else:
            return False
       
    def remove_item_from_fridge(self, email, item):
        user_data = self.get_user(email)
        if user_data:
            fridge_items = user_data['fridge_items']
            if item in fridge_items:
                fridge_items.remove(item)
                user_data['fridge_items'] = fridge_items
                self.save()
                return True
            else:
                print("Item not found in fridge.")
                return False
        else:
            print("User not found.")
            return False


    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
