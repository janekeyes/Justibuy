import { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import globalStyles from '@/src/styles/generalStyles';

interface User {
  id: number;
  username: string;
  email: string;
}

export default function ProfileScreen() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const userId = await AsyncStorage.getItem('userId');
      if (!userId) {
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(`http://172.20.10.7:8000/api/user/${userId}/`);
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error('Failed to fetch user info:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const handleLogout = async () => {
    await AsyncStorage.removeItem('userId');
    setUser(null);
    router.replace('/');
  };

  if (loading) {
    return <Text style={globalStyles.title}>Loading...</Text>;
  }

  //SCREEN DISPLAY
  return (
    <View style={globalStyles.container}>
      {user ? (
        <>
        
        <View style={globalStyles.titleContainer}>
          <Text style={globalStyles.title}>Welcome, {user.username}!</Text>
        </View>
          <View style={[globalStyles.card, { width: '100%', padding: 16 }]}>
            <Text style={globalStyles.label}>Email: {user.email}</Text>
          </View>

          <View style={globalStyles.buttonContainer}>
            <TouchableOpacity style={globalStyles.button} onPress={handleLogout}>
              <Text style={globalStyles.buttonText}>Logout</Text>
            </TouchableOpacity>
          </View>
        </>
      ) : (
        <>
          <Text style={globalStyles.title}>Welcome to Justibuy</Text>
          <Text style={[globalStyles.label, { textAlign: 'center', marginBottom: 20 }]}>
            Log in to enjoy a personalised experience and access all our services.
          </Text>

          <View style={{ width: '100%' }}>
            <TouchableOpacity style={globalStyles.button} onPress={() => router.push('/login')}>
              <Text style={globalStyles.buttonText}>Login</Text>
            </TouchableOpacity>

            <TouchableOpacity style={globalStyles.button} onPress={() => router.push('/register')}>
              <Text style={globalStyles.buttonText}>Register</Text>
            </TouchableOpacity>

            <TouchableOpacity style={globalStyles.button} onPress={() => router.push('/demo')}>
              <Text style={globalStyles.buttonText}>View Demo</Text>
            </TouchableOpacity>
          </View>
        </>
      )}
    </View>
  );
}
