/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

const UPDATE_FREQ = 300 // in ms

import { SensorManager } from 'NativeModules';

import React, { Component } from 'react';
import {
  AppRegistry,
  DeviceEventEmitter,
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View
} from 'react-native';

import firebase from 'firebase'
import { firebaseConfig } from './secrets'

firebase.initializeApp(firebaseConfig);
//
// Create a reference with .ref() instead of new Firebase(url)
const rootRef = firebase.database().ref();
const accelerometerDataRef = rootRef.child('accelerometerData');

export default class RoboDrop extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOn: false
    };
  }

  componentDidMount() {
    const self = this;
    let lastUpdateTime = Date.now();

    DeviceEventEmitter.addListener('Accelerometer', function (data) {
      const currTime = Date.now()

      if (currTime - lastUpdateTime > UPDATE_FREQ) {
        for (let key in data) {
          data[key] = +data[key].toFixed(3)
        }

        accelerometerDataRef.set(data);
        self.setState(data)
        lastUpdateTime = currTime;
      }
    });
  }

  toggleOnState() {
    if (!this.state.isOn) SensorManager.startAccelerometer(100);
    else {
      SensorManager.stopAccelerometer();
      accelerometerDataRef.set({
        x: null,
        y: null,
        z: null
      });
    }

    this.setState({ isOn: !this.state.isOn });
  }

  triggerStarWarsMode() {
    rootRef.set({ starWarsMode: true });
  }

  render() {
    console.log(this.state)
    const { x, y, isOn } = this.state;

    let coordinates;
    if (isOn) coordinates = (
      <View style={styles.row}>
        <Text style={styles.coordinate}>X: {x}</Text>
        <Text style={styles.coordinate}>Y: {y}</Text>
      </View>
    )

    const logobot = (
      <Image
      source={require('./logobot.png')}
      style={styles.logobot}
    />)

    const logobotActive = (
      <Image
      source={require('./logobot_active.png')}
      style={styles.logobot}
    />)

    return (
      <View style={styles.container}>
        <TouchableOpacity
          activeOpacity={1}
          onPress={this.toggleOnState.bind(this)}
          style={styles.button}
          underlayColor={'transparent'}
        >
          {isOn ? logobotActive : logobot}
          <Text style={styles.btnText}>{ isOn ? "GOGOBOT" : "NONOBOT" }</Text>
          <View style={styles.coordinatesContainer}>
            {coordinates}
          </View>
        </TouchableOpacity>
        <TouchableOpacity
          activeOpacity={1}
          style={[styles.button, styles.swButton]}
          onPress={this.triggerStarWarsMode.bind(this)}
        >
          <Text style={styles.swBtnText}>STAR WARS MODE</Text>
        </TouchableOpacity>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  btnText: {
    fontSize: 48,
    paddingBottom: 20,
  },
  button: {
    alignItems: 'center',
    backgroundColor: 'yellow',
    flex: 4,
    justifyContent: 'center'
  },
  container: {
    flex: 1,
    backgroundColor: '#F5FCFF',
  },
  coordinate: {
    paddingRight: 20,
    paddingLeft: 20,
  },
  coordinatesContainer: {
    height: 100
  },
  logobot: {
    marginBottom: 20,
    marginTop: 150
  },
  row: {
    alignItems: 'center',
    flexDirection: 'row',
  },
  swButton: {
    flex: 1,
    backgroundColor: 'black'
  },
  swButtonActive: {
    backgroundColor: 'white'
  },
  swBtnText: {
    color: '#FFE800',
    fontSize: 36
  },
});

AppRegistry.registerComponent('RoboDrop', () => RoboDrop);
