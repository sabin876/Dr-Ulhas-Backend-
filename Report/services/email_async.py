import threading
import logging

logger = logging.getLogger(__name__)


def _send_email(email_msg):
    """
    Internal function that actually sends email
    """
    try:
        email_msg.send(fail_silently=False)
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")


def send_email_async(email_msg):
    """
    Non-blocking async email sender using threading
    """
    thread = threading.Thread(target=_send_email, args=(email_msg,))
    thread.daemon = True
    thread.start()