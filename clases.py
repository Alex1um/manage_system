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
                if lst:
                    lst = ast.literal_eval(lst)
                    lst[2::3] = [" Вышел: " + i + '\n' for i in lst[2::3]]
                    lst[0::3] = ["Был выполнен вход с ip: " + i for i in lst[0::3]]
                    lst[1::3] = [" Вошел: " + i for i in lst[1::3]]
                    return ' '.join(lst)
                return 'None'
            except Exception as f:
                return str(f)
        elif params[:1] == ['пользователи']:
            try:
                lst = tuple(*zip(*cn.cls.sql.execute(f'SELECT login from users').fetchall()))
                return '\n'.join(lst)
            except Exception as f:
                return str(f)
        elif params[:1] == ['?']:
            return '''история {пользователь} - Просмотр активности пользователя; пример: история admin
пользователи - список пользователей'''


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