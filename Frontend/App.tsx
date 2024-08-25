import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer, NavigationContainerEventMap } from '@react-navigation/native';
import { BottomTabNavigationOptions, createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import SearchLayout from './components/search/SearchLayout';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';

export default function App() {
  const Tabs = createBottomTabNavigator();
  const screenOptions = {
    tabBarShowLabel: false,
    headerShown: false,
    tabBarStyle: {
      position: "absolute",
      bottom: 0,
      right: 0,
      left: 0,
    }
  } as BottomTabNavigationOptions

  return (
    <NavigationContainer>
      <Tabs.Navigator screenOptions={screenOptions} >
        <Tabs.Screen
          name="Search"
          component={SearchLayout}
          options={{
            tabBarIcon: ({focused}) => {
              return (
                <View style={{ alignItems: "center", justifyContent: "center" }}>
                  <MaterialIcons name="search" size={24} color={focused ? "#252521" : "#56595e" } />
                  <Text style={{ color: focused ? "#252521" : "#56595e"}}>Search</Text>
                </View>
              )
            }
          }}/>
      </Tabs.Navigator>
    </NavigationContainer>
  );
}

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: '#25292e',
//     alignItems: 'center',
//     justifyContent: 'center',
//   },
//   imageContainer: {
//     flex: 1,
//     paddingTop: 58,
//   },
//   footerContainer: {
//     flex: 1 / 3,
//     alignItems: 'center',
//   },
// });
