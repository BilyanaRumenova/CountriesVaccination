import os


class Config:
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

    @staticmethod
    def get_database_file():
        if os.environ.get('ENVIRONMENT') == 'testing':
            return 'testing.db'
        else:
            return 'countries.db'
