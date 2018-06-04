from flask_restful import reqparse

CURRENCY = "MXN"
PAYMENT_COUNTRY = "MEX"

HEADERS = {'content-type': 'application/json'}
URL = 'https://api.etomin.com/API/v1.0/kount/auth'
URL_CHARGE = 'https://api.etomin.com/API/v1.0/payment'

PARSER = reqparse.RequestParser()
PARSER.add_argument('id_card',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('status',
                    type=str,
                    required=False
                    )
PARSER.add_argument('payment_method',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('amount',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('date',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
