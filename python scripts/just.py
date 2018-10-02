from firebase import firebase

ref = firebase.reference('https://temp-sensor-94648.firebaseio.com/temperature')

values = ref.child('value')

values.setValue(10)
