import configparser


def email_notice(subj, body):
    config = configparser.ConfigParser()
    config.sections()
    config.read('whims.ini')
    to = config['Email']['email']

    # TODO: Finish email service mailx
    return True
