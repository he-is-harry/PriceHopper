import { getAPIData } from "@/api/RESTHelper";
import { Category } from "@/api/types/Category";
import { useEffect, useState } from "react";
import { Dimensions, Image, StyleSheet, Text, View } from "react-native";

const recommendedRowItems = 3;

export default function Search({ searchText }: { searchText: string }) {
  const [recommendedSearches, setRecommendedSearches] = useState([] as Category[]);
  const [promptCategories, setPromptCategories] = useState([] as Category[])

  useEffect(() => {
    getAPIData("/rest/search/recommended")
      .then((_recommendedSearches: Category[]) => {
        console.log((Dimensions.get("window").width - 40 - (recommendedRowItems - 1) * 10 - recommendedRowItems * 16) / recommendedRowItems);
        setRecommendedSearches(_recommendedSearches);
      });
  }, []);

  return (
    <View style={styles.searchContainer}>
      { searchText === "" || promptCategories.length == 0 ?
        <View style={styles.recommendedContainer}>
          <Text style={styles.headerText}>Recommended searches</Text>
          <View style={styles.recommendedList}>
            {recommendedSearches.map((value, index) => 
              <View key={value.categoryName + index}>
                  <View style={styles.recommendedItem}>
                    <Image source={{ uri: value.categoryImage}} style={styles.recommendedImage}/>
                  </View>
                  <Text style={styles.recommendedName}>{value.categoryName}</Text>
              </View>
            )}
          </View>
        </View>
        :
        <></>
      }
    </View>
  );
}

const styles = StyleSheet.create({
  searchContainer: {
    backgroundColor: "#ffffff",
    flex: 1,
    paddingHorizontal: 20
  },
  recommendedContainer: {
    marginTop: 10
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
  }
});