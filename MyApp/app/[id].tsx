import { useLocalSearchParams, Stack, useNavigation } from 'expo-router';
import { View, Text, Image, ScrollView, Linking, ActivityIndicator, Pressable, Alert, useWindowDimensions } from 'react-native';
import { useEffect, useState } from 'react';
import { Ionicons } from '@expo/vector-icons';
import globalStyles from '@/src/styles/generalStyles';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface ClothingItem {
  id: number;
  image: string;
  name: string;
  category: string;
  size: string;
  price: number;
  description: string;
  url?: string;
}

export default function ClothingDetail() {
  const { id } = useLocalSearchParams();
  const [item, setItem] = useState<ClothingItem | null>(null);
  const [isFavourite, setIsFavourite] = useState(false);
  const [imageRatio, setImageRatio] = useState(1);
  const { width } = useWindowDimensions();
  const navigation = useNavigation();

  useEffect(() => {
    if (!id) return;

    fetch(`http://172.20.10.7:8000/api/clothing/${id}/`)
      .then((res) => res.json())
      .then((data) => {
        setItem(data);
        const imgUrl = data.image || 'https://via.placeholder.com/300';
        Image.getSize(imgUrl, (w, h) => {
          setImageRatio(h / w);
        });
      })
      .catch((err) => console.error('Error fetching clothing item:', err));
  }, [id]);

  useEffect(() => {
    const checkFavouriteStatus = async () => {
      const userId = await AsyncStorage.getItem('userId');
      if (!userId || !id) return;

      try {
        const response = await fetch(`http://192.168.0.52:8000/api/wishlist/${id}/status/?user_id=${userId}`);
        const data = await response.json();
        setIsFavourite(data.is_favourited);
      } catch (error) {
        console.error('Error checking favourite status:', error);
      }
    };

    checkFavouriteStatus();
  }, [id]);

  const toggleFavourite = async () => {
    const userId = await AsyncStorage.getItem('userId');
    if (!userId) {
      Alert.alert('Login Required', 'Please log in to use the wishlist.');
      return;
    }

    const endpoint = isFavourite
      ? 'http://172.20.10.7:8000/api/wishlist/remove/'
      : 'http://172.20.10.7:8000/api/wishlist/add/';

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, item_id: id }),
      });

      if (response.ok) {
        setIsFavourite(!isFavourite);
      } else {
        Alert.alert('Error', 'Failed to update wishlist.');
      }
    } catch (error) {
      console.error('Error toggling favourite:', error);
      Alert.alert('Error', 'Something went wrong.');
    }
  };

  if (!item) {
    return <ActivityIndicator style={{ marginTop: 100 }} size="large" />;
  }

  const imageUrl = item.image || 'https://via.placeholder.com/300';
  const productUrl = item.url || '';

  return (
    <ScrollView contentContainerStyle={[globalStyles.screen, { flexGrow: 1 }]}>
      <View style={globalStyles.backButton}>
        <Pressable onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={28} color="#4B3869" />
        </Pressable>
        <View style={globalStyles.titleContainer}>
          <Text style={[globalStyles.title, { fontSize: 22, marginLeft: 12 }]}>Item Details</Text>
        </View>
      </View>

      <View style={globalStyles.imageWrapper}>
        <Image
          source={{ uri: imageUrl }}
          style={{ width: '100%', height: '100%' }}
          resizeMode="cover"
        />
      </View>

      <View style={globalStyles.itemInfo}>
        <Text style={[globalStyles.title, globalStyles.itemTitle]}>{item.name}</Text>
        <Text style={globalStyles.label}>Category: {item.category}</Text>
        <Text style={globalStyles.label}>Size: {item.size}</Text>
        <Text style={globalStyles.label}>Price: €{item.price}</Text>
        <Text style={[globalStyles.label, globalStyles.itemDescription]}>{item.description}</Text>

        {productUrl ? (
          <Text style={[globalStyles.link, { textAlign: 'left' }]} onPress={() => Linking.openURL(productUrl)}>
            View Product Page
          </Text>
        ) : null}
      </View>

      <View style={globalStyles.favouriteButtonContainer}>
        <Pressable style={globalStyles.button} onPress={toggleFavourite}>
          <Ionicons name={isFavourite ? 'heart' : 'heart-outline'} size={20} color="#4B3869" />
          <Text style={globalStyles.buttonText}>
            {isFavourite ? 'Remove from Wishlist' : 'Add to Wishlist'}
          </Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
