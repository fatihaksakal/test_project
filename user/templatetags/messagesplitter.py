from django import template

register = template.Library()


@register.filter(name="getMessage")
def messagedispatcher(value):
    resultmessage = ''
    if value.message[len(value.message)-1] == 1:
        for i in range(len(value.message) - 1):
            resultmessage += value.message[i].data[0].message
    else:
        resultmessage += value.message
    return resultmessage
