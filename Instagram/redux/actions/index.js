import firebase from 'firebase'
import { USER_STATE_CHANGE } from '../constants/index'

export function fetchUser() {
    return((dispatch) => {
        firebase.firestore()
            .collection("user")
            .doc(firebase.auth().currentUser.uid)
            .get()
            .then((snapshot) => {
                if(snapshot.exists)
                {
                    dispatchEvent({type: USER_STATE_CHANGE, currentUser: snapshot.data})
                }
                else{
                    console.log('does not exist')
                }
            })
    })
}