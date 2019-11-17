import socket
import time
import ast
# from system import Connection


class Role:

    def __init__(self, login, ip, prev_times):
        self.auth_time = time.strftime('%d.%m.%Y %H:%M:%S')
        self.login = login
        if prev_times != '':
            self.prev_times = ast.literal_eval(prev_times)
            if prev_times is None:
                self.prev_times = []
        else:
            self.prev_times = []
        self.ip = ip

    def end(self):
        return str(self.prev_times + [self.ip,
                                      self.auth_time,
                                      time.strftime('%d.%m.%Y %H:%M:%S')])

    def execute(self, text, cn):
        return 'None'


class Admin(Role):

    def execute(self, text, cn):
        params = text.split()
        if params[:1] == ['история'] and len(params):
            try:
                lst = cn.cls.sql.execute(f'SELECT times from users'
                                         f' where login = "{params[1]}"'
                                         ).fetchone()[0]
                lst = ast.literal_eval(lst)
                lst[2::3] = [i + '\n' for i in lst[2::3]]
                return ' '.join(lst)
            except Exception as f:
                return str(f), str
        elif params[:1] == ['?']:
            return '? история'


class Storekeeper(Role):
    pass


class SystemManager(Role):
    pass


class Engineer(Role):
    pass


class Tester(Role):
    pass


class HeadOfSalesDepartment(Role):
    pass


class ProductionManager(Role):
    pass


class HeadOfProcurement(Role):
    pass