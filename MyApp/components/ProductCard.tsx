import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { Link } from 'expo-router';
import globalStyles from '@/src/styles/generalStyles';

interface ProductCardProps {
  id: number;
  name: string;
  image: string;
}

const ProductCard: React.FC<ProductCardProps> = ({ id, name, image }) => {
  return (
    <Link href={`/${id}`} asChild>
      <TouchableOpacity style={globalStyles.itemCard}>
        <Image source={{ uri: image }} style={globalStyles.itemImage} />
        <View style={globalStyles.itemDetails}>
          <Text style={[globalStyles.label, { textAlign: 'center' }]} numberOfLines={2}>
            {name}
          </Text>
        </View>
      </TouchableOpacity>
    </Link>
  );
};

export default ProductCard;
