import { Category } from "@/api/types/Category";
import { BASE_API_URL } from "@env";
import { useEffect, useState } from "react";
import { StyleSheet, Text, Image, FlatList, View, Platform, ScrollView } from "react-native";
import { useBottomTabBarHeight } from '@react-navigation/bottom-tabs';

const placeholderImage = require('../../assets/images/ImageNotFound.png');

export default function Home() {
  const [homeData, setHomeData] = useState([] as Category[]);
  const bottomTabBarHeight = useBottomTabBarHeight();

  useEffect(() => {
    fetch(`${BASE_API_URL}/rest/search/homepage`)
      .then(async (response) => {
        let _data = await response.json();
        setHomeData(_data);
      });
  }, []);

  return (
    <ScrollView>
      <View style={{ paddingBottom: bottomTabBarHeight + 10, backgroundColor: "#ffffff" }}>
        {homeData.map((category: Category, index: number) => 
        <View key={category.categoryName + index} style={styles.categoryContainer}>
          <Text style={styles.categoryHeader}>{category.categoryName}</Text>
          <FlatList
            horizontal
            showsHorizontalScrollIndicator={Platform.OS === 'web'}
            data={category.products}
            contentContainerStyle={styles.listContainer}
            renderItem={({ item, index }) => (
              <View key={item.name + index} style={styles.productItem}>
                <Image source={item.image ? { uri: item.image } : placeholderImage} style={styles.homeProductImage} />
                <View style={{ display: "flex", flexDirection: "row", alignItems: "flex-start", paddingTop: 4 }}>
                  <Text style={styles.priceRegText}>$</Text>
                  <Text style={styles.priceLargeText}>{Math.floor(item.price)}</Text>
                  <Text style={styles.priceRegText}>{(Math.round(item.price * 100) % 100).toString().padStart(2, "0")}</Text>
                </View>
                <Text numberOfLines={2} ellipsizeMode="tail" style={{ paddingBottom: 2 }}>{item.name}</Text>
                {item.sciPrice && <Text style={styles.scientificPrice}>{item.sciPrice}</Text>}
                <Text>{item.company}</Text>
              </View>
            )}
          />
        </View>)}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  homeProductImage: {
    width: 150,
    height: 150
  },
  categoryContainer: {
    marginTop: 10,
  },
  categoryHeader: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 10,
    paddingLeft: 20,
  },
  listContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    gap: 20
  },
  listColumnWrapper: {
    gap: 10
  },
  productItem: {
    width: 150
  },
  priceRegText: {
    fontSize: 16,
    lineHeight: 16,
    fontWeight: "500"
  },
  priceLargeText: {
    fontSize: 24,
    lineHeight: 24,
    fontWeight: "600"
  },
  scientificPrice: {
    color: "#56595e"
  }
});