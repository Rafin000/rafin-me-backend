# def send_async_email(msg , app):
#     with app.app_context():
#         mail = app.extensions.get('mail')
#         if mail is None:
#             raise RuntimeError("Mail instance not found in current application context.")
#         try:
#             app.mail.send(msg)
#         except Exception as e:
#             app.logger.error(f"Unable to Send Mail: {str(e)}")
#             raise