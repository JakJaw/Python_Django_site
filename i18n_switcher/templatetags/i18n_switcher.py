from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings


def switch_lang_code(path, language):
 
    # Get lang codes
    lang_codes = [c for (c, name) in settings.LANGUAGES]
 
    # Validate the inputs
    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)
 
    # Split the parts of the url
    parts = path.split('/')
 
    # add language prefix
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
 
    # Return the new path
    return '/'.join(parts)


register = template.Library()
 
@register.filter
@stringfilter
def switch_i18n_prefix(path, language):
    return switch_lang_code(path, language)
 
@register.filter
def switch_i18n(request, language):
    return switch_lang_code(request.get_full_path(), language)