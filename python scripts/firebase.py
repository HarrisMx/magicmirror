import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('magicmirror-52b3f-firebase-adminsdk-oa09x-84946bee47.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://magicmirror-52b3f.firebaseio.com'
})

ref = db.reference('temperature/')
users_ref = ref.child('alcohol_sensor')

users_ref.set({
    'test':  'Drunk'
})