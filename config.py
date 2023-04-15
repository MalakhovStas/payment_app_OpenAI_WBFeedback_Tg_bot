""" Конфигурация базы данных """
server_db_path = '/home/OpenAI_WBFeedback_Tg_bot/database/database.db'
dev_db_path = '/home/ms/PycharmProjects/My_GitHub/OpenAI_WBFeedback_Tg_bot/database/database.db'

DATABASE_CONFIG = {'database': server_db_path,
                   'pragmas': (('cache_size', -1024 * 64),
                               ('journal_mode', 'wal'),
                               ('foreign_keys', 1))}

""" Конфигурация логирования """
errors_format = '{time:DD-MM-YYYY at HH:mm:ss} | {level} | {file} | {message}'
debug_format = '{time:DD-MM-YYYY at HH:mm:ss} | {level} | {file} | {function} | line: {line: >3} | {message}'

logger_common_args = {
    'diagnose': True,
    'backtrace': False,
    'rotation': '10 Mb',
    'retention': 1,
    'compression': 'zip'
}

PATH_FILE_DEBUG_LOGS = 'logs/debug.log'
PATH_FILE_ERRORS_LOGS = 'logs/errors.log'

LOGGER_DEBUG = {'sink': PATH_FILE_DEBUG_LOGS, 'level': 'DEBUG', 'format': debug_format} | logger_common_args
LOGGER_ERRORS = {'sink': PATH_FILE_ERRORS_LOGS, 'level': 'WARNING', 'format': errors_format} | logger_common_args
