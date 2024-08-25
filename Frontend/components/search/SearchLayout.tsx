import { Feather, MaterialIcons } from '@expo/vector-icons';
import Constants from 'expo-constants';
import { useState } from 'react';
import { Keyboard, Platform, Pressable, StyleSheet, TextInput, View } from 'react-native';
import RabbitLogo from '../../assets/images/RabbitLogo.svg';
import Home from './Home';
import Search from './Search';

export default function SearchLayout() {
  const [searchActive, setSearchActive] = useState(false);
  const [searchText, setSearchText] = useState("");
  
  const cancelSearch = () => {
    Keyboard.dismiss();
    setSearchActive(false);
  }

  const focusSearch = () => {
    setSearchActive(true);
  }

  return (
    <View style={StyleSheet.absoluteFill}>
      <View style={[styles.searchBarHeader, { backgroundColor: searchActive ? "#ffffff" : "#a3d977", justifyContent: searchActive ? "space-evenly" : "flex-start" }]}>
        {searchActive ? <Pressable onPress={cancelSearch}><MaterialIcons name="arrow-back" size={24} color="#252521" /></Pressable> : <RabbitLogo width={40} height={40} />}
        <View style={[styles.searchBar, {borderWidth: searchActive ? 2 : 0}]}>
          <Feather name="search" size={20} color="#252521" />
          <TextInput
            style={styles.searchTextInput}
            placeholder="Search Products..."
            placeholderTextColor="#252521"
            value={searchText}
            onChangeText={setSearchText} /* Update to allow polling for search prompts */
            onFocus={focusSearch}
          />
        </View>
      </View>
      {searchActive ?
        <Search searchText={searchText} />
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