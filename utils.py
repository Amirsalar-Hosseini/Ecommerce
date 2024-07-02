from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('7A4E58793048316637327645392F6A4351752B4D4A4C4E5973717A47594172307A65566831624C456334633D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'your verify code is {code}'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)