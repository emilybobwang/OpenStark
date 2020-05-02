# 路由配置
from handlers.api import *

handlers = [(r'/api/msg/(\w+)/(\w+)', messages.MessagesHandler),
            (r'/api/payment/(\w+)/(\w+)', payment.PaymentHandler),
            (r'/api/ifcert/(\w+)/test', ifcert.Ifcert)]
