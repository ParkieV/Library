from sqlalchemy.exc import IntegrityError


def sql_validation_error(exception) -> str:
	if isinstance(exception, IntegrityError):
		str_exc = exception.orig.args[0]
		exc_message = str_exc[str_exc.find(': ')+2:]
		return exc_message
