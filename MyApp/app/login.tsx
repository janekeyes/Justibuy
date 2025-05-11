import { useState } from 'react';
import { TouchableOpacity, View, Text, TextInput, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import globalStyles from '@/src/styles/generalStyles';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function LoginScreen() {
  const router = useRouter();
  const [identifier, setIdentifier] = useState(''); 
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!identifier.trim() || !password.trim()) {
      setError('Please fill in both fields.');
      return;
    }
  
    setError('');
    try {
      const response = await fetch('http://172.20.10.7:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: identifier, password }),
      });

      const data = await response.json();

      if (response.ok) {
        await AsyncStorage.setItem('userId', data.user.id.toString());
        Alert.alert('Success', 'Login successful');
        router.push('/');
      } else {
        Alert.alert('Error', data.error || 'Invalid login credentials');
      }
    } catch (error) {
      Alert.alert('Error', 'Something went wrong');
    }
  };

  //SCREEN DISPLAY
  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Login</Text>

      <TextInput
        style={globalStyles.input}
        placeholder="Username or Email"
        value={identifier}
        onChangeText={setIdentifier}
        autoCapitalize="none"
      />

      <TextInput
        style={globalStyles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      {error ? (
        <Text style={{ color: 'red', marginBottom: 10 }}>{error}</Text>
      ) : null}

      <View style={globalStyles.buttonContainer}>
        <TouchableOpacity style={globalStyles.button} onPress={handleLogin}>
          <Text style={globalStyles.buttonText}>Login</Text>
        </TouchableOpacity>
      </View>

      <View style={globalStyles.buttonContainer}>
        <TouchableOpacity style={globalStyles.button} onPress={() => router.push('/')}>
          <Text style={globalStyles.buttonText}>Continue as Guest</Text>
        </TouchableOpacity>
      </View>

      <View style={globalStyles.buttonContainer}>
        <TouchableOpacity style={globalStyles.button} onPress={() => router.push('/register')}>
          <Text style={globalStyles.buttonText}>Create an Account</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
