from google.appengine.ext import webapp

register = webapp.template.create_template_register()


@register.filter('countByte')
def countByte(value):
    value = int(value)
    if value < 1024 :
      return str(value) + "Byte"
    elif ( 1024 <= value ) and ( value < 1024**2 ) :
      return str(value / 1000) + "KB"
    elif ( 1024**2 <= value ) and ( value < 1024**3 ) :
      return str(value / (1000**2)) + "MB"
    elif 1024**3 <= value :
      return str(value / (1000**3)) + "GB"

@register.filter('do_current_time')
def do_current_time(parser, token):
    try:         # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except TemplateSyntaxError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return CurrentTimeNode(format_string[1:-1])