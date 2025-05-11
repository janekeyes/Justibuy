import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Image, TouchableOpacity, Dimensions } from 'react-native';
import { Link } from 'expo-router';
import globalStyles from '@/src/styles/generalStyles';
import ProductCard from '@/components/ProductCard';

type ClothingItem = {
  id: number;
  name: string;
  image: string;
  category: string;
};

// const screenWidth = Dimensions.get('window').width;

export default function HomeScreen() {
  const [clothingItems, setClothingItems] = useState<ClothingItem[]>([]);

  useEffect(() => {
    fetch('http://172.20.10.7:8000/api/clothing/')
      .then(response => response.json())
      .then(data => setClothingItems(data))
      .catch(error => console.error('Error fetching clothing:', error));
  }, []);

  // Group clothing items by category
  const groupedByCategory: Record<string, ClothingItem[]> = clothingItems.reduce((groups, item) => {
    if (!groups[item.category]) {
      groups[item.category] = [];
    }
    groups[item.category].push(item);
    return groups;
  }, {} as Record<string, ClothingItem[]>);


  //SCREEN DISPLAY
  return (
    <ScrollView style={globalStyles.screen} contentContainerStyle={{ paddingBottom: 80 }}>
      <View style={globalStyles.titleContainer}>
        <Text style={globalStyles.title}>Welcome to Justibuy</Text>
      </View>

      {Object.entries(groupedByCategory).map(([category, items]) => (
        <View key={category} style={{ marginBottom: 30 }}>
          <Text style={[globalStyles.subtitle, { marginLeft: 20, marginBottom: 10 }]}>
            {category}
          </Text>

          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={{ paddingHorizontal: 20 }}>
            {items.map((item) => (
              <ProductCard
                key={item.id}
                id={item.id}
                name={item.name}
                image={`http://172.20.10.7:8000${item.image}`}
              />
            ))}
          </ScrollView>
        </View>
      ))}
    </ScrollView>
  );
}
