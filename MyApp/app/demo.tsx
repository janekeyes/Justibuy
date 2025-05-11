import { View, Text, ScrollView, Alert, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import globalStyles from '@/src/styles/generalStyles';
import { useEffect } from 'react';

export default function DemoScreen() {
  const router = useRouter();

  useEffect(() => {
    console.log('Demo screen loaded');
  }, []);

  const completeDemo = async () => {
    try {
      await AsyncStorage.setItem('hasSeenDemo', 'true');
      router.replace('/'); // Go to Home
    } catch (error) {
      Alert.alert('Error', 'Could not save demo flag. Proceeding to home screen.');
      router.replace('/');
    }
  };

  //SCREEN DISPLAY
  return (
    <ScrollView contentContainerStyle={globalStyles.container}>
      <Text style={[globalStyles.title, { textAlign: 'center', marginBottom: 20 }]}>
        Welcome to Justibuy!
      </Text>

      <Text style={[globalStyles.subtitle, { textAlign: 'center', marginBottom: 20 }]}>
        Your one-stop shopping assistant.
      </Text>

      <Text style={[globalStyles.label, { textAlign: 'center', marginBottom: 20 }]}>
        {'\n\n'}With Justibuy, you can:
      </Text>
      <Text style={[globalStyles.label, { textAlign: 'center', fontSize: 18, marginBottom: 30 }]}>
        - Use your camera or gallery to search for clothing items instantly.
        {'\n'}- Find the cheapest options available online and save money!
        {'\n'}- Keep track of your favorite items with the wishlist feature (login required).
      </Text>

      <Text style={[globalStyles.label, { textAlign: 'center', marginBottom: 40, fontSize: 16 }]}>
        Ready to explore and start saving? Log in to get started!
      </Text>

      <View style={globalStyles.buttonContainer}>
        <TouchableOpacity 
          style={[globalStyles.button, { backgroundColor: '#4B3869', paddingVertical: 15 }]} 
          onPress={completeDemo}
        >
          <Text style={[globalStyles.buttonText, { color: '#fff', fontWeight: '700' }]}>
            Got it! Let’s get started
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}
