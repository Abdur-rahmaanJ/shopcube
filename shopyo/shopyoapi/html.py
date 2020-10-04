'''
Used on flash
flash(notify_success('mail sent!'))
'''
def notify(message, alert_type="primary"):
    '''
    secondary, success, danger, warning, info, light
    dark
    '''
    alert = """
    <div class="alert alert-{alert_type} alert-dismissible fade show" role="alert"
        style="opacity: 0.98;">
      {message}

      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    """.format(message=message, alert_type=alert_type)
    return alert

def notify_success(message):
    return notify(message, alert_type='success')

def notify_danger(message):
    return notify(message, alert_type='danger')

def notify_warning(message):
    return notify(message, alert_type='warning')

def notify_info(message):
    return notify(message, alert_type='info')