from flask_restful import reqparse

PARSER = reqparse.RequestParser()
PARSER.add_argument('name',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('body',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
