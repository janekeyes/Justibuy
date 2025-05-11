import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Image, TouchableOpacity, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
// import { Link } from 'expo-router';
import globalStyles from '@/src/styles/generalStyles';
import ProductCard from '@/components/ProductCard';
//add import for refreshing the wishlist
import { useIsFocused } from '@react-navigation/native';

interface ClothingItem {
  id: number;
  name: string;
  image: string;
}

export default function WishlistScreen() {
  const [items, setItems] = useState<ClothingItem[]>([]);
  const [isGuest, setIsGuest] = useState(false);
  const [loading, setLoading] = useState(true);
  const isFocused = useIsFocused();

  useEffect(() => {

    if (isFocused) {
      const fetchWishlist = async () => {
        const userId = await AsyncStorage.getItem('userId');
        if (!userId) {
            //determine if the user is a guest
            setIsGuest(true);
            setLoading(false);
            return;
        }

        try {
          const response = await fetch(`http://172.20.10.7:8000/api/wishlist/?user_id=${userId}`);
          const data = await response.json();
          setItems(data);
        } catch (error) {
          console.error('Error fetching wishlist:', error);
        } finally {
          setLoading(false);
        }
      };

      fetchWishlist();
    }
  }, [isFocused]);

  if (loading) {
    return <ActivityIndicator style={{ marginTop: 100 }} size="large" />;
  }

  //SCREEN DISPLAY
  return (
    <ScrollView contentContainerStyle={globalStyles.container}>
      <View style={globalStyles.titleContainer}>
        <Text style={globalStyles.title}>Your Wishlist</Text>
      </View>  
      {/* if the user is not logged in, tell them to log in to use wishlist features */}
      {isGuest ? (
        <Text>Please log in to view your wishlist.</Text>
      ) : items.length === 0 ? (
        <Text>No items in your wishlist.</Text>
      ) : (
        <View style={{ gap: 20 }}>
          {items.map((item) => (
            <ProductCard
              key={item.id}
              id={item.id}
              name={item.name}
              image={`http://172.20.10.7:8000${item.image}`}
            />
          ))}
        </View>
      )}
    </ScrollView>
  );
  
}
