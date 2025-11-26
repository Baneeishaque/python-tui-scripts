import gpsoauth

email = 'example@gmail.com'
android_id = '0123456789abcdef'
token = '...' # insert the oauth_token here

master_response = gpsoauth.exchange_token(email, token, android_id)
print('Master response:', master_response)
master_token = master_response['Token']
print('Master token:', master_token)

auth_response = gpsoauth.perform_oauth(
    email, master_token, android_id,
    service='sj', app='com.google.android.music',
    client_sig='...')
print('Auth response:', auth_response)
token = auth_response['Auth']
print('Auth token:', token)
