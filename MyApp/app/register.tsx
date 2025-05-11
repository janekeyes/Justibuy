import { useState } from 'react';
import { TouchableOpacity, View, Text, TextInput, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import globalStyles from '@/src/styles/generalStyles';
//ref: https://reactnative.dev/docs/asyncstorage
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function RegisterScreen() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const isEmailValid = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleRegister = async () => {
    if(!isEmailValid(email)) {
      Alert.alert('Invlaid Email', 'Please enter a valid email address.');
      return;
    }
    try {
      const response = await fetch('http://172.20.10.7:8000/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
  
      const data = await response.json();
      console.log('Response:', data);
  
      if (response.ok) {
        await AsyncStorage.setItem('userId', data.user.id.toString());
        Alert.alert('Success', 'User registered successfully');
        // await AsyncStorage.setItem('userId', data.user.id.toString());
        const seenDemo = await AsyncStorage.getItem(`hasSeenDemo:${data.user.id}`);

        if (!seenDemo) {
          await AsyncStorage.setItem(`hasSeenDemo:${data.user.id}`, 'true');
          router.replace('/demo');
        } else {
          router.replace('/');
        }
      } else {
        Alert.alert('Error', data.error || 'Something went wrong');
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'Something went wrong');
    }
  };
  

  //SCREEN DISPLAY
  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Register</Text>

      <TextInput
        style={globalStyles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />

      <TextInput
        style={globalStyles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />

      <TextInput
        style={globalStyles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <View style={globalStyles.buttonContainer}>
        <TouchableOpacity style={globalStyles.button} onPress={handleRegister}>
          <Text style={globalStyles.buttonText}>Create Account</Text>
        </TouchableOpacity>
      </View>

      <View style={globalStyles.buttonContainer}>
        <TouchableOpacity style={globalStyles.button} onPress={() => router.push('/login')}>
          <Text style={globalStyles.buttonText}>Back to Login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
