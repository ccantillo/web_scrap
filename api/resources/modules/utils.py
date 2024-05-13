from fastapi import HTTPException

from resources.exceptions.exceptions import InputValidationError


async def gen_response(result=None, errors=None, message=None, error=None, **kwargs):
    d = {'result': result,
         'errors': errors,
         'error': error,
         'message': message
         }

    for k, v in kwargs.items():
        d[k] = v

    return d


async def handle_exception(err):
    if type(err).__name__ != 'ValidationError':
        module = __import__("resources.exceptions.exceptions")
        dir_ = getattr(module, "exceptions")
        fil_e = getattr(dir_, "exceptions")
        class_ = getattr(fil_e, type(err).__name__)
        error_class = class_(error_detailed=str(err))
    else:
        error_class = InputValidationError(error_detailed=str(err))

    raise HTTPException(status_code=error_class.status_code, detail=error_class.to_dict())