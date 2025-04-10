import { Feather, MaterialIcons } from '@expo/vector-icons';
import Constants from 'expo-constants';
import { useState } from 'react';
import { Keyboard, Platform, Pressable, StyleSheet, TextInput, View } from 'react-native';
import RabbitLogo from '../../assets/images/RabbitLogo.svg';
import Home from './Home';
import Search from './Search';
import { getAPIData } from '@/api/RESTHelper';
import { Product } from '@/api/types/Product';
import { BasicCategory } from '@/api/types/Category';

export default function SearchLayout() {
  const [searchActive, setSearchActive] = useState(false);
  const [searchText, setSearchText] = useState("");
  const [categorySuggestions, setCategorySuggestions] = useState([] as BasicCategory[]);
  const [results, setResults] = useState([] as Product[]);
  const [showResults, setShowResults] = useState(false);
  const [suggestTimeoutId, setSuggestTimeoutId] = useState<NodeJS.Timeout | undefined>(undefined);

  const searchProductsByName = (search: string) => {
    getAPIData("/rest/search/products?search=" + search)
      .then((_results: Product[]) => {
        setResults(_results);
        setShowResults(true);
        Keyboard.dismiss();
        setSearchActive(false);
      });
  }

  const searchProductsByCategory = (categoryId: number) => {
    getAPIData("/rest/search/products?categoryId=" + categoryId)
      .then((_results: Product[]) => {
        setResults(_results);
        setShowResults(true);
        Keyboard.dismiss();
        setSearchActive(false);
      });
  }

  const searchCategorySuggestions = (search: string) => {
    getAPIData("/rest/search/categories?search=" + search)
      .then((_categorySuggestions: BasicCategory[]) => {
        // Add default search option with the text entered
        _categorySuggestions.push(new BasicCategory(0, "\"" + search + "\"", undefined));
        setCategorySuggestions(_categorySuggestions);
      });
  }

  const updateSearchText = (_searchText: string) => {
    setSearchText(_searchText);
    if (suggestTimeoutId) {
      clearTimeout(suggestTimeoutId);
    }

    // Trigger the suggestion search after 500 ms
    const timeoutId = setTimeout(() => {
      searchCategorySuggestions(_searchText);
    }, 500);

    setSuggestTimeoutId(timeoutId);
  }
  
  const cancelSearch = () => {
    Keyboard.dismiss();
    setSearchActive(false);
    // Show home
    setShowResults(false);
  }

  const focusSearch = () => {
    setSearchActive(true);
  }

  return (
    <View style={StyleSheet.absoluteFill}>
      <View style={[styles.searchBarHeader, { backgroundColor: searchActive || showResults ? "#ffffff" : "#a3d977", justifyContent: searchActive ? "space-evenly" : "flex-start" }]}>
        {searchActive || showResults ? <Pressable onPress={cancelSearch}><MaterialIcons name="arrow-back" size={24} color="#252521" /></Pressable> : <RabbitLogo width={40} height={40} />}
        <View style={[styles.searchBar, {borderWidth: searchActive || showResults ? 2 : 0}]}>
          <Feather name="search" size={20} color="#252521" />
          <TextInput
            style={styles.searchTextInput}
            placeholder="Search Products..."
            placeholderTextColor="#252521"
            value={searchText}
            onChangeText={updateSearchText}
            onSubmitEditing={() => searchProductsByName(searchText)}
            onFocus={focusSearch}
            autoCapitalize="none"
            clearButtonMode="always"
          />
        </View>
      </View>
      {searchActive || showResults ?
        <Search searchActive={searchActive} searchText={searchText} setSearchText={setSearchText} searchProductsByName={searchProductsByName} searchProductsByCategory={searchProductsByCategory} categorySuggestions={categorySuggestions} results={results} />
        :
        <Home />
      }
    </View>
  );
}

const styles = StyleSheet.create({
  searchBarHeader: {
    display: "flex",
    flexDirection: "row",
    paddingTop: Constants.statusBarHeight + (Platform.OS === 'web' ? 10 : 2),
    paddingHorizontal: 15,
    paddingBottom: 10,
    alignItems: "center",
    gap: 10
  },
  searchBar: {
    display: "flex",
    flexDirection: "row",
    borderRadius: 25,
    backgroundColor: "#ffffff",
    borderColor: "#252521",
    alignItems: "center",
    flex: 1,
    padding: 10
  },
  searchTextInput: {
    color: "black",
    fontSize: 16,
    marginLeft: 10,
    flex: 1
  }
});