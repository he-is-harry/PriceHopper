import { getAPIData } from "@/api/RESTHelper";
import { BasicCategory, Category } from "@/api/types/Category";
import { Product } from "@/api/types/Product";
import { Feather } from "@expo/vector-icons";
import { useBottomTabBarHeight } from "@react-navigation/bottom-tabs";
import React from "react";
import { useEffect, useState } from "react";
import { Dimensions, FlatList, Image, Pressable, StyleSheet, Text, View } from "react-native";

const placeholderImage = require('../../assets/images/ImageNotFound.png');
const recommendedRowItems = 3;

export default function Search({ searchActive, searchText, setSearchText, searchProductsByName, searchProductsByCategory, categorySuggestions, results }: { searchActive: boolean, searchText: string, setSearchText: React.Dispatch<React.SetStateAction<string>>,searchProductsByName: (search: string) => void, searchProductsByCategory: (categoryId: number) => void, categorySuggestions: BasicCategory[], results: Product[] }) {
  const bottomTabBarHeight = useBottomTabBarHeight();
  const [recommendedSearches, setRecommendedSearches] = useState([] as Category[]);

  useEffect(() => {
    getAPIData("/rest/search/recommended")
      .then((_recommendedSearches: Category[]) => {
        setRecommendedSearches(_recommendedSearches);
      });
  }, []);

  return (
    <View style={[styles.searchContainer, { paddingBottom: bottomTabBarHeight + 10 }]}>
      { searchActive ? 
        <>
          { searchText === "" || categorySuggestions.length == 0 ?
            <View style={[styles.bodyContainer, styles.recommendedBodyContainer]}>
              <Text style={styles.headerText}>Recommended searches</Text>
              <View style={styles.recommendedList}>
                {recommendedSearches.map((value, index) => 
                  <View key={value.categoryName + index}>
                      <Pressable onPress={() => searchProductsByCategory(value.categoryId)}>
                        <View style={styles.recommendedItem}>
                          <Image source={{ uri: value.categoryImage}} style={styles.recommendedImage}/>
                        </View>
                        <Text style={styles.recommendedName}>{value.categoryName}</Text>
                      </Pressable>
                  </View>
                )}
              </View>
            </View>
            :
            <View style={[styles.bodyContainer]}>
              <FlatList
                key="suggestions-flat-list"
                data={categorySuggestions}
                contentContainerStyle={styles.productList}
                renderItem={({ item }) => (
                  <Pressable onPress={() => {
                    if (item.categoryId == 0) {
                      searchProductsByName(item.categoryName);
                    } else {
                      setSearchText(item.categoryName);
                      searchProductsByCategory(item.categoryId);
                    }
                  }}>
                    <View style={styles.suggestionContainer}>
                      <View style={styles.suggestionContainer}>
                        <Image source={item.categoryImage ? { uri: item.categoryImage} : placeholderImage} style={styles.suggestionImage}/>
                        <Text>{item.categoryName}</Text>
                      </View>
                      <Feather name="search" size={20} color="#56595e" />
                    </View>
                  </Pressable>
                )}
              />
            </View>
          }
        </>
        :
        <View style={styles.bodyContainer}>
          {results.length > 0 ? 
            <FlatList 
              key="results-flat-list"
              data={results}
              numColumns={2}
              contentContainerStyle={styles.productList}
              columnWrapperStyle={styles.productListRow}
              renderItem={({ item }) => (
                <View style={styles.productItem}>
                  <Image source={item.image ? { uri: item.image } : placeholderImage} style={styles.productImage}/>
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
          :
            <View style={styles.noResultsContainer}>
              <Text style={styles.noResultsText}>No results found for "{searchText}"</Text>
              <Text style={styles.noResultsSuggestionText}>Suggestions: </Text>
              <View>
                <Text>{'\u2022 Make sure all words are spelled correctly.'}</Text>
                <Text>{'\u2022 Try different keywords.'}</Text>
                <Text>{'\u2022 Try more general keywords.'}</Text>
              </View>
            </View>}
        </View>
        }
      
    </View>
  );
}

const styles = StyleSheet.create({
  searchContainer: {
    backgroundColor: "#ffffff",
    flex: 1
  },
  bodyContainer: {
    marginTop: 10,
    flex: 1
  },
  recommendedBodyContainer: {
    paddingHorizontal: 20
  },
  headerText: {
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 15
  },
  recommendedList: {
    flexDirection: "row",
    columnGap: 10,
    flexWrap: "wrap"
  },
  recommendedItem: {
    borderRadius: 5,
    borderWidth: 1,
    borderColor: "#56595e",
    alignItems: "center",
    justifyContent: "center",
    padding: 8,
  },
  recommendedImage: {
    // Compute width and height as (window width - horizontal padding - (# items - 1) * gap - (# items) * item padding * 2 - (# items) * item border * 2) / (# items)
    // Here we use 4 items per row
    width: (Dimensions.get("window").width - 40 - (recommendedRowItems - 1) * 10 - recommendedRowItems * 16 - recommendedRowItems * 2) / recommendedRowItems,
    height: (Dimensions.get("window").width - 40 - (recommendedRowItems - 1) * 10 - recommendedRowItems * 16 - recommendedRowItems * 2) / recommendedRowItems,
  },
  recommendedName: {
    fontWeight: "600",
    textAlign: "center",
    marginTop: 5
  },
  suggestionContainer: {
    flexDirection: "row",
    flex: 1,
    alignItems: "center"
  },
  suggestionList: {
    rowGap: 10
  },
  innerSuggestionContainer: {
    flexDirection: "row",
    flex: 1,
    alignItems: "center"
  },
  suggestionImage: {
    width: 40,
    height: 40,
    marginRight: 10
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
  },
  productList: {
    paddingHorizontal: 20,
    gap: 10
  },
  productListRow: {
    justifyContent: "space-between"
  },
  productItem: {
    // Compute width as (window width - horizontal padding - (# items - 1) * gap) / (# items)
    // We assume 2 items per row
    width: (Dimensions.get("window").width - 40 - 1 * 10) / 2
  },
  productImage: {
    // Compute width and height as (window width - horizontal padding - (# items - 1) * gap) / (# items)
    // We assume 2 items per row
    width: (Dimensions.get("window").width - 40 - 1 * 10) / 2,
    height: (Dimensions.get("window").width - 40 - 1 * 10) / 2
  },
  noResultsContainer: {
    paddingHorizontal: 20,
    justifyContent: "center"
  },
  noResultsText: {
    fontSize: 18
  },
  noResultsSuggestionText: {
    marginTop: 10,
    marginBottom: 5,
    fontSize: 16
  }
});