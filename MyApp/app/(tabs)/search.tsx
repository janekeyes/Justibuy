//imports
import { useState } from 'react';
import { Link } from 'expo-router';
import { View, Text, TextInput, TouchableOpacity, Alert, Image, FlatList, ActivityIndicator } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import globalStyles from '@/src/styles/generalStyles';
//import { launchImageLibrary } from 'react-native-image-picker';


export default function SearchScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [image, setImage] = useState<string | null>(null);
  const [searchResults, setSearchResults] = useState<any[]>([]); //store search results
  const [loading, setLoading] = useState(false);//loading state
  const handleTakePhoto = async () => {
    //get user permission to use their camera
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Denied', 'Camera access is required to take a photo.');
      return;
    }

    //launch the camera to take a picture
    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImage(uri);
      //upload the image and compare with database items
      await uploadImage(uri);
    }
  };

  //function to open the gallery and pick an image
  const handlePickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Denied', 'Gallery access is required to pick an image.');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImage(uri);
      await uploadImage(uri);
    }
  };


  //method to upload the image and compare it to database items
  const uploadImage = async (uri: string) => {
    setLoading(true);
    const formData = new FormData();
    const fileUri = uri;
    const fileName = fileUri.split('/').pop();
    const fileType = fileUri.split('.').pop();

    formData.append('image', {
      uri: fileUri,
      name: fileName,
      type: `image/${fileType}`,
    } as any); //gets rid of append error for React Native

    try {
      const response = await fetch('http://172.20.10.7:8000/api/search-clothing/', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      console.log('Search result from backend:', result);

      if (response.ok) {
        // Update the search results with the best matches
        setSearchResults(result);
      } else {
        Alert.alert('No Matches', 'Could not find a match for the image.');
      }
    } catch (error) {
      console.error('Upload failed:', error);
      Alert.alert('Error', 'Failed to upload image');
    } finally {
      setLoading(false); //set loading to false once request is finsihed
    }
  };

  //function to search by keyword
  const handleKeywordSearch = async () => {
    if (!searchQuery.trim()) {
      Alert.alert('Empty Search', 'You must enter a vlid search term.');
      return;
    }
  
    setLoading(true);
    //if there is an image already in the search query, it must be cleared to search by keyword
    setImage(null); // Clear image if any
  
    try {
      const response = await fetch(`http://172.20.10.7:8000/api/search-keyword/?q=${encodeURIComponent(searchQuery)}`);
      const result = await response.json();
  
      if (response.ok) {
        setSearchResults(result);
      } else {
        Alert.alert('Search Error', result.error || 'Something went wrong.');
      }
    } catch (error) {
      console.error('Keyword search failed:', error);
      Alert.alert('Error', 'Could not complete the search.');
    } finally {
      setLoading(false);
    }
  };

  //SCREEN DISPLAY
  return (
    <View style={globalStyles.searchScreen}>
      <View style={globalStyles.titleContainer}>
        <Text style={globalStyles.title}>Search</Text>
      </View>

      <View style={globalStyles.formGroup}>
        <TextInput
          style={globalStyles.input}
          placeholder="Search for items by keyword..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
  
        <View style={{ flexDirection: 'row', justifyContent: 'space-around', width: '100%', marginBottom: 10 }}>
          <TouchableOpacity style={globalStyles.miniIconButton} onPress={handleKeywordSearch}>
            <Ionicons name="search-outline" size={24} color="#4B3869" />
          </TouchableOpacity>
          <TouchableOpacity style={globalStyles.miniIconButton} onPress={handleTakePhoto}>
            <Ionicons name="camera-outline" size={24} color="#4B3869" />
          </TouchableOpacity>
          <TouchableOpacity style={globalStyles.miniIconButton} onPress={handlePickImage}>
            <Ionicons name="image-outline" size={24} color="#4B3869" />
          </TouchableOpacity>
        </View>
      </View>
  
      {/* uploaded image */}
      {image && (
        <Image
          source={{ uri: image }}
          style={{ width: 80, height: 80, marginBottom: 10, borderRadius: 8, alignSelf: 'center' }}
        />
      )}
  
      {loading && (
        <ActivityIndicator size="small" color="#4B3869" style={{ marginBottom: 10 }} />
      )}
  
      {/* results */}
      {searchResults.length > 0 && (
        <FlatList
          data={searchResults}
          keyExtractor={(item) => item.id.toString()}
          numColumns={2}
          contentContainerStyle={{ paddingTop: 10, paddingBottom: 100 }}
          columnWrapperStyle={{ justifyContent: 'space-between', paddingHorizontal: 5 }}
          renderItem={({ item }) => (
            <Link href={`/${item.id}`} asChild>
              <TouchableOpacity style={globalStyles.card}>
                <Image
                  source={{ uri: `http://172.20.10.7:8000${item.image}` }}
                  style={globalStyles.image}
                  resizeMode="cover"
                />
                <Text style={globalStyles.label}>{item.name}</Text>
                <Text style={{ fontSize: 14, color: '#7A7A7A', paddingHorizontal: 10 }}>
                  {item.category}
                </Text>
                <Text style={{ paddingHorizontal: 10 }}>{item.description}</Text>
                <Text style={{ paddingHorizontal: 10, fontWeight: '500' }}>{item.price}</Text>
                <Text style={{ paddingHorizontal: 10, fontSize: 12 }}>
                  Match Score: {item.visual_similarity}
                </Text>
                <Text style={{ paddingHorizontal: 10, fontSize: 12, marginBottom: 10 }}>
                  Matched Keypoints: {item.match_count}
                </Text>
              </TouchableOpacity>
            </Link>
          )}
        />
      )}
    </View>
  );
}  