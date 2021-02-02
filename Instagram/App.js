import { StatusBar } from 'expo-status-bar';
import * as firebase from 'firebase';
import React, { Component } from 'react'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import rootReducer from './redux/reducers'
import thunk from 'redux-thunk'
const store = createStore(rootReducer, applyMiddleware(thunk))

const firebaseConfig = {
  apiKey: "AIzaSyDKQoiNJ-9FgoI06101_ug2cZjMT7DO3fs",
  authDomain: "instagram-c457c.firebaseapp.com",
  projectId: "instagram-c457c",
  storageBucket: "instagram-c457c.appspot.com",
  messagingSenderId: "1091337235358",
  appId: "1:1091337235358:web:7905e7ba9218f3549d848f",
  measurementId: "G-KCHDP9FNJD"
};

if(firebase.apps.length === 0) {
  firebase.initializeApp(firebaseConfig)
}

import { StyleSheet, Text, View, Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack'

import LandingScreen from './components/auth/Landing';
import RegisterScreen from './components/auth/Register';
import LoginScreen from './components/auth/Login'
import MainScreen from './components/Main'

const Stack = createStackNavigator();

export class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      loaded: false,
    }
  }

  componentDidMount() {
    firebase.auth().onAuthStateChanged(( user ) => {
      if(!user) {
        this.setState({
          loggedIn: false,
          loaded: true,
        })
      }
      else{
        this.setState({
          loggedIn: true,
          loaded: true,
        })
      }
    })
  }

  render() {
    const { loggedIn, loaded } = this.state;
    if(!loaded){
      return(
        <View style = {{ flex: 1, justifyContent: 'center' }}>
          <Text>Loading...</Text>
        </View>
      )
    }
    if(!loggedIn){
      return (
        <NavigationContainer>    
          <Stack.Navigator initialRouteName = "Landing">
            <Stack.Screen name = "Landing" component = { LandingScreen } options = {{ headerShown: false }}/>
            <Stack.Screen name = "Register" component = { RegisterScreen } options = {{ headerShown: false }}/>
            <Stack.Screen name = "Login" component = { LoginScreen } options = {{ headerShown: false }}/>
          </Stack.Navigator>
        </NavigationContainer>
      ); 
    }

    return(
      <Provider store = { store }>
        <MainScreen/>
      </Provider>
    )
  }
}

export default App